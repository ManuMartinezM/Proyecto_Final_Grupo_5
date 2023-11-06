import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Final Project - HENRY (Group 5)", page_icon=":taxi:", layout="wide")

st.title(":bar_chart: HENRY: Final Project - Group 5")
st.markdown("***")

st.image("Cover.jpg", caption="SmartANALYTICS")

from Pages import (
    KPI_1, KPI_2, KPI_3, KPI_4, KPI_5,
    Model_Intro, Data_Analysis_for_ML, ML_Models_Results
)

# Create a sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", ["KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5", "Model Intro", "Data Analysis", "ML Models"])

# Display the content of the selected page
if selected_page == "KPI 1":
    KPI_1.show_page()
elif selected_page == "KPI 2":
    KPI_2.show_page()
elif selected_page == "KPI 3":
    KPI_3.show_page()
elif selected_page == "KPI 4":
    KPI_4.show_page()
elif selected_page == "KPI 5":
    KPI_5.show_page()
elif selected_page == "Model Intro":
    ML_1_Intro.show_page()
elif selected_page == "Data Analysis":
    ML_2_Data_Analysis_for_ML.show_page()
elif selected_page == "ML Models":
    ML_3_Models_Results.show_page()