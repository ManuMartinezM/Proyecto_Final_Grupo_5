import os
from dotenv import load_dotenv
import datetime
import pandas as pd
from etl_tripdata import clean_df
import argparse
from pathlib import Path


def find_files_to_clean(directory):
    log('Looking for new raw files to clean')

    service_types = os.listdir(directory)

    for service_type in service_types:
        log(f'Processing service type {service_type}')

        files = os.listdir(f'{directory}/{service_type}')

        for file in files:
            log(f"Cleaning file {file} for service type {service_type}")

            if os.path.exists(f'{directory}-clean/{service_type}/{file}'):
                log('Already cleaned, skipping')
                continue

            df = clean_file(f'{directory}/{service_type}/{file}', service_type)

            Path(f'{directory}-clean/{service_type}').mkdir(parents=True, exist_ok=True)
            df.to_csv(f'{directory}-clean/{service_type}/{file}', index=False)

    log(f'Done processing all service types for new raw data')


def clean_file(filename, service_type):
    df = pd.read_parquet(filename)
    df = clean_df(df, service_type)
    return df


def log(message):
    now = datetime.datetime.now()
    print(f'[{now.strftime("%Y/%m/%d %H:%M:%S")}] {message}')


if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(description='Extraccion de datos de un CSV de viajes')
    parser.add_argument('--directory', help='nombre del directorio donde cargar archivos', required=True)
    args = parser.parse_args()

    find_files_to_clean(args.directory)
