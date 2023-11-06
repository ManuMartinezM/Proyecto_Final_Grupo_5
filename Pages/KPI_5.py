import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

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


