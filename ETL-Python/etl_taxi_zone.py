import pandas as pd 
from dbfread import DBF
import warnings
warnings.filterwarnings("ignore")
path_file = '/taxi_zones.dbf'

registros = []
with DBF(path_file) as dbf:
    for registro in dbf:
        registros.append(dict(registro))

df = pd.DataFrame(registros)

df = df[['OBJECTID','zone','borough']]

df=df.rename(columns={'OBJECTID':'Location_id','zone':'Location_name','borough':'Borough'})
df=df.drop_duplicates(subset=['Location_name','Borough'])
df.to_csv('clean_data/clean_taxi_zone.parquet',index=False, sep=';')
