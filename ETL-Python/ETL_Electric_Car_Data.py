import pandas as pd

electric_car_data = pd.read_csv('Datasets/ElectricCarData_Clean.csv')

selected_columns = ['Brand', 'Model', 'PriceEuro']
filtered_electric_car_data = electric_car_data[selected_columns]

exchange_rate = 1.06  # 1 EUR = 1.06 USD
filtered_electric_car_data['PriceUSD'] = filtered_electric_car_data['PriceEuro'] * exchange_rate
filtered_electric_car_data = filtered_electric_car_data.drop(columns=['PriceEuro'])

filtered_electric_car_data.to_csv('filtered_electric_car_data.csv', index=False)