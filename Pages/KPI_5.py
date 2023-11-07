import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

def display_KPI_5_page():

    st.title("KPI: 5% reduction in carbon emissions")
    st.markdown("***")

    top_10_electric = pd.read_csv('merged_top_10_electric.csv')
    top_10_hybrid = pd.read_csv('merged_top_10_hybrid.csv')

    # Load your datasets (merged_top_10_hybrid and merged_top_10_electric)

    # Calculate the total emissions for each group (electric and hybrid)
    total_emissions_hybrid = top_10_hybrid['Annual Emissions (lbs CO2)'].sum()
    total_emissions_electric = top_10_electric['Annual Emissions (lbs CO2)'].sum()

    # Create a DataFrame for the emissions data
    emissions_data = pd.DataFrame({
        'Category': ['Hybrid', 'Electric'],
        'Total Emissions (lbs CO2)': [total_emissions_hybrid, total_emissions_electric]
    })

    # Create a Plotly bar chart
    fig1 = px.bar(emissions_data, x='Category', y='Total Emissions (lbs CO2)',
                labels={'Total Emissions (lbs CO2)': 'Total Emissions (lbs CO2)'},
                title='Total Carbon Emissions for Hybrid vs. Electric Cars')

    # Show the chart
    fig1.show()


# Create a sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", ["KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5", "Model Intro", "Data Analysis", "ML Models"])

# Import and run the code for the selected KPI
if selected_page == "KPI 1":
    from Pages import KPI_1
    KPI_1.show_page()
elif selected_page == "KPI 2":
    from Pages import KPI_2
    KPI_2.show_page()
elif selected_page == "KPI 3":
    from Pages import KPI_3
    KPI_3.show_page()
elif selected_page == "KPI 4":
    from Pages import KPI_4
    KPI_4.show_page()
elif selected_page == "KPI 5":
    from Pages import KPI_5
    KPI_5.show_page()
elif selected_page == "Model Intro":
    from Pages import Model_Intro
    Model_Intro.show_page()
elif selected_page == "Data Analysis":
    from Pages import Data_Analysis_for_ML
    Data_Analysis_for_ML.show_page()
elif selected_page == "ML Models":
    from Pages import ML_Models_Results
    ML_Models_Results.show_page()


