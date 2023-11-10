import os
from dotenv import load_dotenv
import s3fs
import datetime
import csv
import argparse
from tqdm import tqdm
import pandas as pd
import sqlalchemy as db


def log(message):
    now = datetime.datetime.now()
    print(f'[{now.strftime("%Y/%m/%d %H:%M:%S")}] {message}')


def insert_file(filename, table, use_s3, bucket, s3_key, s3_secret, db_host, db_user, db_password, db_name, batch_size):
    log(f'Opening file {filename}')
    if use_s3:
        s3 = s3fs.S3FileSystem(key=s3_key, secret=s3_secret)
        f = s3.open(f"s3://{bucket}/{filename}", 'r')
    else:
        f = open(filename, 'r')

    first_line = f.readline()
    delimiter = ';' if ';' in first_line else ','

    log('Got file, parsing as CSV')
    f.seek(0)
    df = pd.read_csv(f, delimiter=delimiter, header=0, names=[
                     'PU_location_id', 'DO_location_id', 'Trip_distance', 'Total_amount', 'Year', 'Month', 'Day', 'Hour', 'Trip_time', 'Service_type_id'])
    f.close()

    log('Beginning insert')
    engine = db.create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')
    insert_data(df, table, engine, batch_size)

    log('Done')


def insert_data(df, table, engine, batch_size):
    with tqdm(total=len(df)) as pbar:
        for cdf in chunker(df, batch_size):
            cdf.to_sql(table, engine, if_exists='append', index=False, method='multi')
            pbar.update(batch_size)

    log('Inserts complete, committing')
    db.commit()


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def log(message):
    now = datetime.datetime.now()
    print(f'[{now.strftime("%Y/%m/%d %H:%M:%S")}] {message}')


if __name__ == '__main__':
    load_dotenv()

    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    bucket = os.getenv('AWS_S3_BUCKET')
    s3_key = os.getenv('AWS_ACCESS_KEY_ID')
    s3_secret = os.getenv('AWS_SECRET_ACCESS_KEY')

    parser = argparse.ArgumentParser(description='Insersion de CSV a una tabla SQL')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--filename', help='nombre del archivo csv fuente')
    group.add_argument('--directory', help='nombre del directorio')
    parser.add_argument('--table', help='nombre de la tabla', required=True)
    parser.add_argument('--batch-size', default=20000, type=int)
    parser.add_argument('--s3', action='store_true')
    args = parser.parse_args()

    if args.directory is not None:
        files = os.listdir(args.directory)
        for file in files:
            insert_file(f'{args.directory}/{file}', args.table, args.s3, bucket, s3_key, s3_secret,
                        db_host, db_user, db_password, db_name, args.batch_size)
    else:
        insert_file(args.filename, args.table, args.s3, bucket, s3_key, s3_secret,
                    db_host, db_user, db_password, db_name, args.batch_size)
