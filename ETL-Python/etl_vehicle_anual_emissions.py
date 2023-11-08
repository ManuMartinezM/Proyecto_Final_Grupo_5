import pandas as pd

df=pd.read_csv('Datasets/file.csv')
df[['Year','Brand','Model','Fuel']]=df['vehicle'].str.extract('(\d{4}) (Land Rover|(?:\w+-\w+)|(?:\w+)) (.*) (EV|Gasoline|Hybrid)', expand=True)
df.drop(columns=['vehicle'], inplace=True)