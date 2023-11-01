import pandas as pd 
from dbfread import DBF
import warnings
warnings.filterwarnings("ignore")
path_file = './Datasets/taxi_zones.dbf'

registros = []
with DBF(path_file) as dbf:
    for registro in dbf:
        registros.append(dict(registro))

df = pd.DataFrame(registros)

df = df[['OBJECTID','LocationID','borough','zone']]

df.to_csv('./clean_data/clean_taxi_zone.csv',index=False, sep=';')
