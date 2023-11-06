import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

st.title('Machine Learning Models')
st.markdown('***')

st.write('''Below there are three Clasification Models options to select. Choosing each of them you will be able to see the following metrics of the Machine learning models:

    - Acuracy
    - Confusion Matrix
    - Clasiffication Report''')



# DataFrame creation:
yellow_tripdata = pd.read_csv('clean_yellow_2022-06.csv')
fhvhv_tripdata = pd.read_csv('clean_fhvhv_2022-06.csv')
green_tripdata = pd.read_csv('clean_green_2022-06.csv')
merged_data = pd.concat([yellow_tripdata, fhvhv_tripdata, green_tripdata], ignore_index=True)
def get_relation(amount, distance):
    if distance == 0:
        relation = amount
    else:
        relation = amount / distance
    return relation
df= merged_data
df['rel_amount_dist'] = df.apply(lambda f: get_relation(f['total_amount'],f['trip_distance']), axis=1)
umbral = 4.52
etiquetas = ['Y', 'N']
df['Discount'] = pd.cut(df['rel_amount_dist'], bins=[-float('inf'), umbral, float('inf')], labels=etiquetas)
df.head()


st.write('## Select the model:')

dim = st.radio('Model:',('Logistic Regression','K-Nearest Neighbors','Decision Tree'),horizontal=True)

if dim == 'Logistic Regression':
    st.write('## Logistic Regression Model Classifier')
    y=  df['Discount']#--> v objetivo
    X= df[['trip_distance', 'day','trip_time']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    st.write('- Accuracy:', round(accuracy,5))
    st.write('- Confusion Matrix:', conf_matrix)
    st.write('- Classification Report:', [classification_rep])
    if st.checkbox('Conclution:'):
        st.write('In conclution, this model has a decent accuracy but may need improvements, especially in terms of recall for the positive class to reduce false negatives')

elif dim == ('K-Nearest Neighbors'):
    k = st.slider(label='K number:',min_value=2,max_value=4)
    st.write('## K-Nearest Neighbors Model Classifier')
    y=  df['Discount']#--> v objetivo
    X= df[['trip_distance', 'day','trip_time']]
    label_encoder = LabelEncoder()
    df['Discount'] = label_encoder.fit_transform(df['Discount'])
    X = df[['trip_distance', 'day','trip_time']] # Características
    y = df['Discount']  # Etiquetas
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    st.write('- Accuracy:', round(accuracy,5))
    st.write('- Confusion Matrix:',conf_matrix)
    st.write('- Classification Report:',[classification_rep])
    if st.checkbox('Conclution:'):
        st.write('In summary, this model also performs well, with a high accuracy and strong performance in predicting class "0," and reasonably good performance in predicting class "1." . As it has a better recall for both, When K is 2 or 3, negative and positive results, this model is a stronger and better with 3 clusters.')

elif dim == ('Decision Tree'):
    st.write('## Decision Tree Model Classifier')
    label_encoder = LabelEncoder()
    df['Discount'] = label_encoder.fit_transform(df['Discount'])
    X = df[['trip_distance', 'day','trip_time']] # Características
    y = df['Discount']  # Etiquetas
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    st.write('- Accuracy:',round(accuracy,5))
    st.write('- Confusion Matrix:',conf_matrix)
    st.write('- Classification Report:',[classification_rep])
    if st.checkbox('Conclution:'):
        st.write('In summary, this model performs reasonably well with a good accuracy. It has strong performance in predicting class "0" and moderate performance in predicting class "1.". Howerver, this model has a good presition at predicting true positivies and avoiding false positivies, the previuos model has an overall better performance in every metric.')

