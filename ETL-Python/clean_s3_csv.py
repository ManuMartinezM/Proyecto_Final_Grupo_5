import os
from dotenv import load_dotenv
import pandas as pd
from etl_tripdata import clean_df
import s3fs
import datetime


def find_files_to_clean(bucket, key, secret):
    s3 = s3fs.S3FileSystem(key=key, secret=secret)

    service_types = get_s3_elements(s3, f'{bucket}/raw/')

    for service_type in service_types:
        log(f'Processing service type {service_type}')

        raw_files = get_s3_elements(s3, f'{bucket}/raw/{service_type}/')
        clean_files = get_s3_elements(s3, f'{bucket}/clean/{service_type}/')

        to_clean = [raw_file for raw_file in raw_files if raw_file not in clean_files]

        if len(to_clean) == 0:
            log(f"No new raw files to clean for service type {service_type}")
        else:
            for file in to_clean:
                log(f"Cleaning file {file} for service type {service_type}")
                clean_s3_file(file, service_type, bucket, key, secret)

    log(f'Done processing all service types')


def get_s3_elements(s3, dir):
    try:
        return [os.path.split(subdir)[-1] for subdir in s3.ls(dir) if subdir != dir]
    except FileNotFoundError:
        return []


def clean_s3_file(filename, service_type, bucket, key, secret):
    df = pd.read_csv(f"s3://{bucket}/raw/{service_type}/{filename}", storage_options={'key': key, 'secret': secret})

    clean_df(df, service_type)

    df.to_csv(f"s3://{bucket}/clean/{service_type}/{filename}", storage_options={'key': key, 'secret': secret})


def log(message):
    now = datetime.datetime.now()
    print(f'[{now.strftime("%Y/%m/%d %H:%M:%S")}] {message}')


if __name__ == '__main__':
    load_dotenv()

    bucket = os.getenv('AWS_S3_BUCKET')
    key = os.getenv('AWS_ACCESS_KEY_ID')
    secret = os.getenv('AWS_SECRET_ACCESS_KEY')

    find_files_to_clean(bucket, key, secret)
