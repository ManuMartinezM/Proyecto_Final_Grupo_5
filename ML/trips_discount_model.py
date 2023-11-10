import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
import argparse


APPLY_DISCOUNT = 1  # 1 significa bla, 0 significa ble


def train():
    df = pd.read_csv('../../Datasets/samples/merged_sample.csv')

    # Codificar la variable categórica 'classification' en valores numéricos
    label_encoder = LabelEncoder()
    df['Discount'] = label_encoder.fit_transform(df['Discount'])

    X = df[['PULocationID',	'DOLocationID', 'hour', 'day', 'year', 'month']]  # Características
    y = df['Discount']  # Etiquetas

    # Crear y entrenar el modelo KNN
    k = 2  # Valor de k (número de vecinos)
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X, y)

    def analyze_for_discount(pu_location, do_location, year, month, day, hour):
        X_test = pd.DataFrame({'PULocationID': [pu_location], 'DOLocationID': [do_location], 'hour': [
                              hour], 'day': [day], 'year': [year], 'month': [month]})
        [result] = model.predict(X_test)

        if result == APPLY_DISCOUNT:
            return True
        else:
            return False

    return analyze_for_discount


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modelo de ML')
    parser.add_argument('--pu-location', help='id de ubicacion de pickup', required=True, type=int)
    parser.add_argument('--do-location', help='id de ubicacion de dropoff', required=True, type=int)
    parser.add_argument('--year', help='año', default=2023, type=int)
    parser.add_argument('--month', help='mes', default=6, type=int)
    parser.add_argument('--day', help='dia', required=True, type=int)
    parser.add_argument('--hour', help='hora', required=True, type=int)
    args = parser.parse_args()

    analyze_for_discount = train()
    result = analyze_for_discount(args.pu_location, args.do_location, args.year, args.month, args.day, args.hour)
    print("Resultado:", result)
