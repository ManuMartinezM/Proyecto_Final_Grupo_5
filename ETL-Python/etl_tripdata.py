import pandas as pd
import argparse


def clean_df(df, service_type):
    standardize_df_fields(df, service_type)

    df.dropna(how='any', inplace=True)

    df['year'] = df['pickup_datetime'].dt.year
    df['month'] = df['pickup_datetime'].dt.month
    df['day'] = df['pickup_datetime'].dt.day

    hours = (df['pickup_datetime'].dt.hour).astype(str).str.zfill(2)
    minutes = (df['pickup_datetime'].dt.minute).astype(str).str.zfill(2)

    df['pu_time'] = hours.str.cat(minutes, sep=':')

    if not 'trip_time' in df.columns:
        # Some service types do not include the trip_time field so we need to compute it
        df['trip_time'] = df['dropoff_datetime'] - df['pickup_datetime']

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
