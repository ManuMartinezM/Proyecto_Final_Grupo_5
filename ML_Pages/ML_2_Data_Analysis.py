import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def display_ML_2_Data_Analysis_page():

    st.title('DataFrame Analysis and Tranformation')
    if st.checkbox('Display source datasets'):
        st.write('- clean_yellow_2022-06.csv')
        st.write('- clean_fhvhv_2022-06.csv')
        st.write('- clean_green_2022-06.csv')


    #Creo/defino el df merged:
    yellow_tripdata = pd.read_csv('clean_yellow_2022-06.csv')
    fhvhv_tripdata = pd.read_csv('clean_fhvhv_2022-06.csv')
    green_tripdata = pd.read_csv('clean_green_2022-06.csv')

    # Unir los DataFrames relevantes
    merged_data = pd.concat([yellow_tripdata, fhvhv_tripdata, green_tripdata], ignore_index=True)
    def get_relation(amount, distance):
        if distance == 0:
            relation = amount
        else:
            relation = amount / distance
        return relation
    df= merged_data
    # Aplicar la transformación
    df['rel_amount_dist'] = df.apply(lambda f: get_relation(f['total_amount'],f['trip_distance']), axis=1)
    umbral = 4.52
    etiquetas = ['Y', 'N']
    # Aplicar la transformación
    df['Discount'] = pd.cut(df['rel_amount_dist'], bins=[-float('inf'), umbral, float('inf')], labels=etiquetas)
    st.write('## DataFrame')
    #DataFrame
    if st.checkbox('See Complete DataFrame'):
        st.dataframe(df)

    if st.checkbox("See Dataframe's head or Tail"):
        if st.button('Head'):
            st.write(df.head())
        if st.button('Tail'):
            st.write(df.tail())

    dim = st.radio('Dimensions:',('Rows','Columns'),horizontal=True)

    if dim == 'Rows':
        st.write('Rows Quantity:',df.shape[0])
    else:
        st.write('Columns Quantity:',df.shape[1])


    #The df.describe()
    if st.button('Statics Summary'):
        st.write(df.describe())
        st.write('#### Description:')
        st.write('We are examining the relationship between cost and distance (this would be the cost per mile) to assess the distribution of this variable, taking into account that higher values of this variable correspond to trips with more traffic, while lower values correspond to times with less traffic. For this purpose, we analyze the distribution with the following histogram and the description based on the mean, standard deviation, and quartile values.')

    #The df Histogram
    st.write('### Histogram:')
    if st.button('Graph'):
        data =  df['rel_amount_dist']
        fig, ax = plt.subplots()
        ax.hist(data,bins=40, color='lightblue', edgecolor='blue', range=(0,50))
        ax.set_title('Data Histogram')
        ax.set_xlabel('Values')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
    if st.checkbox('Histogram Analysis'):
        st.write(''' We define the threshold value for classifying trips with and without discounts as the limit value of the first quartile. In this way, the 25% of trips with the lowest cost per mile will be classified as "Y" (positive for the discount), and for these trips, we will offer a lower cost to incentivize mobility during off-peak traffic hours. On the other hand, the remaining 75% of trips will be classified as "N" (negative for the discount), and the fare amount will not be affected. Taking this column as our target variable, we will train different machine learning models: 
            
            1.Logistic Ression
        2.K-Nearest Neighbors
        3.Decision Tree

    The goal is to determine the optimal model for predicting which trips should receive discounts, considering the features trip distance ('trip_distance'), day ('day'), and travel time ('trip_time'). Finally, we will prioritize the model with the lowest false positive rate (recall) since we are concerned about the economic viability of the company, especially in its early stages.''')