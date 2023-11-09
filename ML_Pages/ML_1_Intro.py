import streamlit as st

def display_ML_1_Intro_page():

    st.title('MVP - Machine Learning Model')

    st.markdown('***')
    st.write('Welcome to the interactive streamlit, here you can see and examinate the diferentes reason why we decided to use a K-Nearest Neighbors Model to our MVP Machine')
    st.write('## Index:')
    st.write(''''
    - Introduction: The actual tap
    - Data Analysis: in this tab it can be observe the complete DataFrame, with their shape, a superficial analisis of the diferents columns, and a histogram. All with a written description and conclution from the analysis.
    - Model Results: this Tab shows the performance, of the three types of model we decided to examninate, Logistic Regression- K-Nearest Neighbors - Decision Tree. Thanks to that observations we decided which one mached better with our MVP Machine Learning Model''')

    st.write('From the whole Smart-Analitics team, Thanks for reading and for your interest in our project.')

    st.sidebar.markdown('Welcome :)')
