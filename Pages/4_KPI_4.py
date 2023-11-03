import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import warnings

st.set_page_config(page_title="KPI 4", page_icon=":taxi:", layout="wide")

st.title("KPI: 10% increase in the average utility")
st.markdown("***")

# Load your data
fhv_2022 = pd.read_csv('clean_fhvhv_2022-06.csv')
fhv_2023 = pd.read_csv('clean_fhvhv_2023-06.csv')

green_2022 = pd.read_csv('clean_green_2022-06.csv')
green_2023 = pd.read_csv('clean_green_2023-06.csv')

yellow_2022 = pd.read_csv('clean_yellow_2022-06.csv')
yellow_2023 = pd.read_csv('clean_yellow_2023-06.csv')

# Combine data for June 2022 and June 2023
fhv_data = pd.concat([fhv_2022, fhv_2023])
green_data = pd.concat([green_2022, green_2023])
yellow_data = pd.concat([yellow_2022, yellow_2023])

kpi_objective = 5  # Adjust this value as needed

# Filter data for relevant airport locations
airport_ids = [1, 132, 138]
filtered_fhv_data = fhv_data[fhv_data['PULocationID'].isin(airport_ids) | fhv_data['DOLocationID'].isin(airport_ids)]
filtered_green_data = green_data[green_data['PULocationID'].isin(airport_ids) | green_data['DOLocationID'].isin(airport_ids)]
filtered_yellow_data = yellow_data[yellow_data['PULocationID'].isin(airport_ids) | yellow_data['DOLocationID'].isin(airport_ids)]

# Calculate the total revenue, number of passengers, and trips for June 2022 and June 2023
total_revenue_2022 = (
    filtered_fhv_data[filtered_fhv_data['year'] == 2022]['total_amount'].sum()
    + filtered_green_data[filtered_green_data['year'] == 2022]['total_amount'].sum()
    + filtered_yellow_data[filtered_yellow_data['year'] == 2022]['total_amount'].sum()
)
total_revenue_2023 = (
    filtered_fhv_data[filtered_fhv_data['year'] == 2023]['total_amount'].sum()
    + filtered_green_data[filtered_green_data['year'] == 2023]['total_amount'].sum()
    + filtered_yellow_data[filtered_yellow_data['year'] == 2023]['total_amount'].sum()
)
total_passengers_2022 = (
    filtered_fhv_data[filtered_fhv_data['year'] == 2022]['passenger_count'].sum()
    + filtered_green_data[filtered_green_data['year'] == 2022]['passenger_count'].sum()
    + filtered_yellow_data[filtered_yellow_data['year'] == 2022]['passenger_count'].sum()
)
total_passengers_2023 = (
    filtered_fhv_data[filtered_fhv_data['year'] == 2023]['passenger_count'].sum()
    + filtered_green_data[filtered_green_data['year'] == 2023]['passenger_count'].sum()
    + filtered_yellow_data[filtered_yellow_data['year'] == 2023]['passenger_count'].sum()
)
total_trips_2022 = (
    filtered_fhv_data[filtered_fhv_data['year'] == 2022]['PULocationID'].count()
    + filtered_green_data[filtered_green_data['year'] == 2022]['PULocationID'].count()
    + filtered_yellow_data[filtered_yellow_data['year'] == 2022]['PULocationID'].count()
)
total_trips_2023 = (
    filtered_fhv_data[filtered_fhv_data['year'] == 2023]['PULocationID'].count()
    + filtered_green_data[filtered_green_data['year'] == 2023]['PULocationID'].count()
    + filtered_yellow_data[filtered_yellow_data['year'] == 2023]['PULocationID'].count()
)

# Calculate the percentage change in revenue, number of passengers, and trips between June 2022 and June 2023
revenue_growth = ((total_revenue_2023 - total_revenue_2022) / total_revenue_2022) * 100
passenger_growth = ((total_passengers_2023 - total_passengers_2022) / total_passengers_2022) * 100
trip_growth = ((total_trips_2023 - total_trips_2022) / total_trips_2022) * 100

# Define CSS styles based on KPI status (met or not met)
kpi_style = f"""
    padding: 10px;
    font-size: 20px;
    border-radius: 10px;
    color: white;
    display: flex;
    justify-content: space-between;
    background-color: {"#4CAF50" if revenue_growth >= kpi_objective or passenger_growth >= kpi_objective or trip_growth >= kpi_objective else "#FF5733"};
"""

# Display the KPI banner with custom styling
st.markdown(f'<div style="{kpi_style}">Goal: {kpi_objective}%<div>{"KPI goal met!" if revenue_growth >= kpi_objective or passenger_growth >= kpi_objective or trip_growth >= kpi_objective else "KPI not met"}</div></div>', unsafe_allow_html=True)

# Display the KPI banner
if revenue_growth >= kpi_objective or passenger_growth >= kpi_objective or trip_growth >= kpi_objective:
    st.success(f'Demand for airport taxi services increased by {max(revenue_growth, passenger_growth, trip_growth):.2f}%.')
else:
    st.error(f'Demand for airport taxi services did not increase by 5% in terms of revenue, passengers, or trips.')

color_palette = ['#ADD8E6', '#90EE90']

# Create columns to display figures and titles side by side
col1, col2, col3 = st.columns(3)

# Define a consistent figure size
fig_width = 300
fig_height = 300

# Create a bar chart for Total Revenue
fig1, ax1 = plt.subplots(figsize=(fig_width, fig_height))
ax1.bar(['June 2022', 'June 2023'], [total_revenue_2022, total_revenue_2023], color=color_palette[0])
ax1.set_title('Total Revenue Comparison')
ax1.set_ylabel('Revenue')
col1.pyplot(fig1)