import pandas as pd

light_duty_vehicles = pd.read_csv('Datasets/Light Duty Vehicles.csv')

selected_columns = ['Model', 'Model Year', 'Manufacturer', 'Fuel']
filtered_light_duty_vehicles = light_duty_vehicles[selected_columns]
filtered_light_duty_vehicles.drop_duplicates(inplace=True,ignore_index=True)
filtered_light_duty_vehicles.rename(columns={'Model Year':'Year','Manufacturer':'Brand'},inplace=True)

filtered_light_duty_vehicles.to_csv('clean_data/clean_light_duty_vehicles.csv', index=False)
