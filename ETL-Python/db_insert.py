import os
from dotenv import load_dotenv
import s3fs
import datetime
import pandas as pd
from etl_tripdata import clean_df
import csv
import pymysql

INSERT_BATCH_SIZE = 2000


def find_files_to_clean(bucket, key, secret):
    log('Looking for new raw files to clean')

    s3 = s3fs.S3FileSystem(key=key, secret=secret)

    service_types = get_s3_elements(s3, f'{bucket}/raw/')

    for service_type in service_types:
        log(f'Processing service type {service_type}')

        raw_files = get_s3_elements(s3, f'{bucket}/raw/{service_type}/')
        clean_files = get_s3_elements(s3, f'{bucket}/clean/{service_type}/')

        to_clean = [
            raw_file for raw_file in raw_files if raw_file not in clean_files
        ]

        if len(to_clean) == 0:
            log(f"No new raw files to clean for service type {service_type}")
        else:
            for file in to_clean:
                log(f"Cleaning file {file} for service type {service_type}")
                clean_s3_file(file, service_type, bucket, key, secret)

    log(f'Done processing all service types for new raw data')


def clean_s3_file(filename, service_type, bucket, key, secret):
    (_, extension) = os.path.splitext(filename)
    if extension == '.csv':
        df = pd.read_csv(f"s3://{bucket}/raw/{service_type}/{filename}", storage_options={'key': key, 'secret': secret})
    elif extension == '.parquet':
        df = pd.read_parquet(f"s3://{bucket}/raw/{service_type}/{filename}",
                             storage_options={'key': key, 'secret': secret})
    else:
        raise Exception(f'Unkown extension {extension}')

    clean_df(df, service_type)

    df.to_csv(f"s3://{bucket}/clean/{service_type}/{filename}",
              index=False, storage_options={'key': key, 'secret': secret})


def find_files_to_insert(bucket, s3_key, s3_secret, db_host, db_user,
                         db_password, db_name):
    log('Looking for new clean files to insert to the database')

    s3 = s3fs.S3FileSystem(key=s3_key, secret=s3_secret)
    db = pymysql.connect(host=db_host,
                         user=db_user,
                         passwd=db_password,
                         db=db_name)

    service_types = get_s3_elements(s3, f'{bucket}/clean/')

    for service_type in service_types[::-1]:
        log(f'Processing service type {service_type}')

        clean_files = get_s3_elements(s3, f'{bucket}/clean/{service_type}/')
        inserted_files = get_s3_elements(s3,
                                         f'{bucket}/inserted/{service_type}/')

        to_insert = [
            clean_file for clean_file in clean_files
            if clean_file not in inserted_files
        ]

        if len(to_insert) == 0:
            log(f"No new clean files to insert for service type {service_type}"
                )
        else:
            for file in to_insert:
                log(f"Inserting file {file} for service type {service_type}")
                insert_s3_file(file, service_type, bucket, s3, db)

    log(f'Done processing all service types for new clean data')


def insert_s3_file(filename, service_type, bucket, s3, db):
    with s3.open(f"s3://{bucket}/clean/{service_type}/{filename}", 'r') as f:
        data = list(csv.reader(f))[1:]
        insert_data(data, db)

    s3.touch(f"s3://{bucket}/inserted/{service_type}/{filename}")


def insert_data(data, db):
    cursor = db.cursor()
    for n in range(0, len(data), INSERT_BATCH_SIZE):
        cursor.executemany(
            f'''
            INSERT INTO trips_data 
                (trip_distance, PULocationID, DOLocationID, total_amount, year, month, day, PU_time, DO_time, trip_time, type_service) 
                VALUES ({', '.join(['%s'] * len(data[0]))})''', data[n: n + INSERT_BATCH_SIZE])
    db.commit()


def get_s3_elements(s3, dir):
    try:
        return [os.path.split(subdir)[-1] for subdir in s3.ls(dir) if subdir != dir]
    except FileNotFoundError:
        return []


def log(message):
    now = datetime.datetime.now()
    print(f'[{now.strftime("%Y/%m/%d %H:%M:%S")}] {message}')


if __name__ == '__main__':
    load_dotenv()

    bucket = os.getenv('AWS_S3_BUCKET')
    s3_key = os.getenv('AWS_ACCESS_KEY_ID')
    s3_secret = os.getenv('AWS_SECRET_ACCESS_KEY')

    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    find_files_to_clean(bucket, s3_key, s3_secret)
    find_files_to_insert(bucket, s3_key, s3_secret, db_host, db_user,
                         db_password, db_name)
