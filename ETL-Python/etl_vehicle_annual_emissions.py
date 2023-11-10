import pandas as pd

df = pd.read_csv('file.csv')


# The column 'vehicle' has the year, brand, model an dtype of fuel of each vechicle, so we'll split this information in 4 different columns using a regular expression.
df[['Year', 'Brand', 'Model', 'Fuel']] = df['vehicle'].str.extract(
    '(\d{4}) (Land Rover|(?:\w+-\w+)|(?:\w+)) (.*) (EV|Gasoline|Hybrid)', expand=True)
df.drop(columns=['vehicle'], inplace=True)

# We'll replace the commas in each row in wich there's a thousand separator.
df['annual_operating_cost'] = df['annual_operating_cost'].str.replace(',', '')
df['annual_electricity_use'] = df['annual_electricity_use'].str.replace(',', '')
df['annual_fuel_elec_cost'] = df['annual_fuel_elec_cost'].str.replace(',', '')
df['Precio'] = df['Precio'].str.replace(',', '')

# We use the extract function to only keep the number in each column.
df['annual_fuel_use'] = df['annual_fuel_use'].str.extract('(\d+)').astype(int)
df['annual_electricity_use'] = df['annual_electricity_use'].str.extract('(\d+)').astype(int)
df['annual_fuel_elec_cost'] = df['annual_fuel_elec_cost'].str.extract('(\d+)').astype(int)
df['annual_operating_cost'] = df['annual_operating_cost'].str.extract('(\d+)').astype(int)
df['cost_per_mile'] = df['cost_per_mile'].str.extract('(\d+.\d+)').astype(float)

# We rename the columns for consistency and change the order, so it's clearer that we have one vehicle per row.
df = df.rename(columns={'annual_fuel_use': 'Fuel_use', 'annual_electricity_use': 'Electricity_use', 'annual_fuel_elec_cost': 'Fuel_elec_cost',
                        'annual_operating_cost': 'Operating_cost', 'cost_per_mile': 'Cost_per_mile', 'annual_emissions_lbs_CO2': 'Annual_emissions_lbs_co2', 'Precio': 'Vehicle_price'})

df = df[['Year', 'Brand', 'Model', 'Fuel', 'Vehicle_price', 'Fuel_use', 'Electricity_use',
         'Fuel_elec_cost', 'Operating_cost', 'Cost_per_mile', 'Annual_emissions_lbs_co2']]

df.to_csv('../clean_data/clean_vehicle_annual_emissions.parquet', index=False)
