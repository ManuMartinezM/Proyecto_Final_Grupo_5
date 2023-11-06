import pandas as pd
from datetime import datetime
import argparse


def clean_df(df, service_type):
    standardize_df_fields(df, service_type)

    df.dropna(how='any', inplace=True)

    df['year'] = df.apply(
        lambda f: get_year(str(f['pickup_datetime'])), axis=1)
    df['month'] = df.apply(
        lambda f: get_month(str(f['pickup_datetime'])), axis=1)
    df['day'] = df.apply(
        lambda f: get_day(str(f['pickup_datetime'])), axis=1)
    df['pu_time'] = df.apply(
        lambda f: get_PU_time(str(f['pickup_datetime'])), axis=1)
    df['do_time'] = df.apply(
        lambda f: get_DO_time(str(f['dropoff_datetime'])), axis=1)

    if not 'trip_time' in df.columns:
        # Some service types do not include the trip_time field so we need to compute it
        df['trip_time'] = df.apply(lambda f: get_triptime(
            str(f['pickup_datetime']), str(f['dropoff_datetime'])), axis=1)

    df['type_service'] = 1 if service_type == 'fhvhv' else 0  # 0 stands for 'not for hire vehicle'

    # We no longer need the datetimes since we've extracted them into year, month, day and time
    to_drop = ['pickup_datetime', 'dropoff_datetime']
    df.drop(columns=to_drop, inplace=True)


def standardize_df_fields(df, service_type):
    PU_DATETIME_FIELDNAMES = {
        'green': 'lpep_pickup_datetime',
        'yellow': 'tpep_pickup_datetime',
        'fhvhv': 'pickup_datetime',
    }

    DO_DATETIME_FIELDNAMES = {
        'green': 'lpep_dropoff_datetime',
        'yellow': 'tpep_dropoff_datetime',
        'fhvhv': 'dropoff_datetime',
    }

    TRIP_DISTANCE_FIELDNAMES = {
        'green': 'trip_distance',
        'yellow': 'trip_distance',
        'fhvhv': 'trip_miles',
    }

    TOTAL_AMOUNT_FIELDNAMES = {
        'green': 'total_amount',
        'yellow': 'total_amount',
        'fhvhv': 'base_passenger_fare',
    }

    PU_DATETIME_FIELDNAME = PU_DATETIME_FIELDNAMES[service_type]
    DO_DATETIME_FIELDNAME = DO_DATETIME_FIELDNAMES[service_type]
    TRIP_DISTANCE_FIELDNAME = TRIP_DISTANCE_FIELDNAMES[service_type]
    TOTAL_AMOUNT_FIELDNAME = TOTAL_AMOUNT_FIELDNAMES[service_type]

    to_extract = [PU_DATETIME_FIELDNAME, DO_DATETIME_FIELDNAME, 'PULocationID', 'DOLocationID', TRIP_DISTANCE_FIELDNAME,
                  TOTAL_AMOUNT_FIELDNAME]

    if service_type == 'fhvhv':
        to_extract.append('trip_time')

    to_drop = [column for column in df.columns if not column in to_extract]
    df.drop(columns=to_drop, inplace=True)

    df.rename(mapper={PU_DATETIME_FIELDNAME: 'pickup_datetime', DO_DATETIME_FIELDNAME: 'dropoff_datetime',
              TRIP_DISTANCE_FIELDNAME: 'trip_distance', TOTAL_AMOUNT_FIELDNAME: 'total_amount'}, axis=1, inplace=True)


def get_year(pu_iso_datetime):
    return datetime.fromisoformat(pu_iso_datetime).year


def get_month(pu_iso_datetime):
    return datetime.fromisoformat(pu_iso_datetime).month


def get_day(pu_iso_datetime):
    return datetime.fromisoformat(pu_iso_datetime).day


def get_PU_time(pu_iso_datetime):
    return datetime.fromisoformat(pu_iso_datetime).strftime('%H:%M')


def get_DO_time(do_iso_datetime):
    return datetime.fromisoformat(do_iso_datetime).strftime('%H:%M')


def get_triptime(pu_iso_datetime, do_iso_datetime):
    pu = datetime.fromisoformat(pu_iso_datetime)
    do = datetime.fromisoformat(do_iso_datetime)
    triptime = do - pu
    return int(triptime.total_seconds())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extraccion de datos de un CSV de viajes')
    parser.add_argument('--source', help='nombre del archivo csv fuente', required=True)
    parser.add_argument('--destination', help='nombre del archivo csv a crear', required=True)
    parser.add_argument('--service-type', choices=['green', 'yellow', 'fhvhv'], required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.source)

    clean_df(df, args.service_type)

    df.to_csv(args.destination, index=False)
    print("Resultados guardados en", args.destination)
