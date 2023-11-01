# ETL Vehicle Fuel Economy Data
import pandas as pd 
import warnings
warnings.filterwarnings("ignore")
df = pd.read_csv('./Datasets/Vehicle Fuel Economy Data.csv')
df = df[['Model','co2','co2TailpipeGpm']]
df.drop_duplicates()
df['Model'] = df['Model'].astype(str)
df['co2'].fillna(0, inplace=True)
df['co2TailpipeGpm'].fillna(0, inplace=True)
def replace_co2(row):
    if row['co2'] == -1.0:
        return round(row['co2TailpipeGpm'], 2)
    else:
        return round(row['co2'], 2)
    
df['co2'] = df.apply(replace_co2, axis=1)    
df= df[['Model','co2']].reset_index(drop=True)
df.to_csv('./clean_data/clean_Vehicle Fuel Economy Data.csv', index=False, sep=';')
