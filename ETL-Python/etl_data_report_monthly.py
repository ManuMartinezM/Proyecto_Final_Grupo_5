import pandas as pd
import numpy as np

df = pd.read_csv('Datasets\data_reports_monthly.csv')

# Split the 'Month/Year' column into 'Month' and 'Year' columns
df[['Year', 'Month']] = df['Month/Year'].str.split('-', expand=True)
df['Year'] = df['Year'].astype(int)  # Convert 'Year' and 'Month' columns to integers
df['Month'] = df['Month'].astype(int)
df['Trips Per Day'] = df['Trips Per Day'].str.replace(',', '', regex=True).astype(int)
df = df.drop('Month/Year', axis=1)  # Drop the original 'Month/Year' column
df['Trips Per Day Shared'] = df['Trips Per Day Shared'].replace('-', np.nan)  # Replace '-' for NaN
df['Trips Per Day Shared'] = df['Trips Per Day Shared'].str.replace(
    ',', '', regex=True).astype(float).astype('Int64')  # change the dtype to int
df['Unique Vehicles'] = df['Unique Vehicles'].str.replace(',', '', regex=True).astype(int)  # change the dtype to int

filtered_df = df[(df['Year'] == 2023) | (df['Year'] == 2022)]
dfKPI2 = filtered_df.groupby(['License Class', 'Year', 'Month']).agg(
    {'Trips Per Day': 'sum', 'Trips Per Day Shared': 'sum', 'Unique Vehicles': 'sum'}).reset_index()

dfKPI2 = dfKPI2.rename(columns={'Unnamed: 0': 'Report_id', 'License Class': 'Service_type_id',
                       'Trips Per Day': 'Trips_per_day', 'Trips Per Day Shared': 'Shared_trips_per_day', 'Unique Vehicles': 'Unique_vehicles'})
dfKPI2.to_csv('monthly_reports.parquet', sep=';')
