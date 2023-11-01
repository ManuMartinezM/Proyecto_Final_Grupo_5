import pandas as pd
from datetime import datetime
import argparse


def main(source, destination, service_type):
    PU_DATETIME_FIELDNAME = 'lpep_pickup_datetime' if service_type == 'green' else 'tpep_pickup_datetime'
    DO_DATETIME_FIELDNAME = 'lpep_dropoff_datetime' if service_type == 'green' else 'tpep_dropoff_datetime'

    df = get_clean_df(source, PU_DATETIME_FIELDNAME, DO_DATETIME_FIELDNAME)

    df['year'] = df.apply(
        lambda f: get_year(f[PU_DATETIME_FIELDNAME]), axis=1)
    df['month'] = df.apply(
        lambda f: get_month(f[PU_DATETIME_FIELDNAME]), axis=1)
    df['day'] = df.apply(
        lambda f: get_day(f[PU_DATETIME_FIELDNAME]), axis=1)
    df['pu_time'] = df.apply(
        lambda f: get_PU_time(f[PU_DATETIME_FIELDNAME]), axis=1)
    df['do_time'] = df.apply(
        lambda f: get_DO_time(f[DO_DATETIME_FIELDNAME]), axis=1)

    df['triptime'] = df.apply(lambda f: get_triptime(
        f[PU_DATETIME_FIELDNAME], f[DO_DATETIME_FIELDNAME]), axis=1)

    df['type_service'] = 0  # 0 stands for 'not for hire vehicle'

    # We no longer need the datetimes since we've extracted them into year, month, day and time
    to_drop = [PU_DATETIME_FIELDNAME, DO_DATETIME_FIELDNAME]
    df.drop(columns=to_drop, inplace=True)

    df.to_csv(destination, index=False)
    print("Resultados guardados en", destination)


def get_clean_df(source, pu_datetime_fieldname, do_datetime_fieldname):
    df = pd.read_csv(source)

    to_extract = [pu_datetime_fieldname, do_datetime_fieldname, 'PULocationID', 'DOLocationID', 'passenger_count', 'trip_distance',
                  'total_amount']
    df = df[to_extract]

    df['passenger_count'].fillna(1, inplace=True)
    df.dropna(how='any', inplace=True)

    return df


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
    parser.add_argument('--service-type', choices=['green', 'yellow'], required=True)
    args = parser.parse_args()

    main(args.source, args.destination, args.service_type)
