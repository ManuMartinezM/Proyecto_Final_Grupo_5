import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import warnings

st.set_page_config(page_title="KPI 2", page_icon=":taxi:", layout="wide")

st.header("KPI: 5% increase in demand for shared rides between 2022 and 2023")
st.markdown("***")

data_reports_monthly = pd.read_csv('data_reports_monthly.csv')

# Replace '-' with 0 in 'Trips Per Day Shared' column and convert it to numeric
data_reports_monthly['Trips Per Day Shared'] = data_reports_monthly['Trips Per Day Shared'].str.replace(',', '', regex=True).replace('-', 0).astype(float)

# Calculate the percentage increase in shared trips between 2022 and 2023
shared_trips_2022 = data_reports_monthly[data_reports_monthly['Month/Year'].str.contains('2022')]['Trips Per Day Shared'].sum()
shared_trips_2023 = data_reports_monthly[data_reports_monthly['Month/Year'].str.contains('2023')]['Trips Per Day Shared'].sum()
demand_increase = ((shared_trips_2023 - shared_trips_2022) / shared_trips_2022) * 100

# Define the KPI objective
kpi_objective = 5  # Adjust this value as needed

# Define CSS styles based on KPI status (met or not met)
kpi_style = f"""
    padding: 10px;
    font-size: 20px;
    border-radius: 10px;
    color: white;
    display: flex;
    justify-content: space-between;
    background-color: {"#4CAF50" if demand_increase >= kpi_objective else "#FF5733"};
"""

# Display the KPI banner with custom styling
st.markdown(f'<div style="{kpi_style}">Goal: {kpi_objective}%<div>{"KPI goal met!" if demand_increase >= kpi_objective else "KPI not met"}</div></div>', unsafe_allow_html=True)

# Display the KPI banner
if demand_increase >= 5:
    st.success('Demand for shared taxi rides increased by {:.2f}%.'.format(demand_increase))
elif demand_increase >= 0:
    st.error('Demand for shared taxi rides increased by only {:.2f}%.'.format(demand_increase))
else:
    st.error('Demand for shared taxi rides decreased by {:.2f}%.'.format(demand_increase))

# Define a consistent figure size
fig_width = 300
fig_height = 300

color_palette = ['#ADD8E6', '#90EE90', '#808080']

# Filter the data for the years 2020 to 2023
data_filtered = data_reports_monthly[data_reports_monthly['Month/Year'].str.contains('2021|2022|2023')]

# Create a bar chart with Plotly
fig1 = px.bar(data_filtered, x='Month/Year', y='Trips Per Day Shared', title='Trend of Shared Trips (2021-2023)')

# Customize the figure layout
fig1.update_layout(
    xaxis_title='Month/Year',
    yaxis_title='Trips Per Day Shared',
    xaxis=dict(tickangle=-45),
    plot_bgcolor='white',  # Background color
)

# Set figure dimensions
fig1.update_layout(
    width=fig_width,
    height=fig_height
)

# Apply the custom color palette
fig1.update_traces(marker_color=color_palette[0])  # Update the bar color

# Create columns to display figures and titles side by side
col1, col2, col3 = st.columns(3)

# Display the figure using st.plotly_chart within the specified column
with col1:
    st.plotly_chart(fig1)


# Group the license classes into two categories
for_hire_classes = ["FHV - Black Car", "FHV - High Volume", "FHV - Livery", "FHV - Lux Limo"]
not_for_hire_classes = ["Green", "Yellow"]

data_filtered['Category'] = data_filtered['License Class'].apply(lambda x: 'For Hire Vehicles' if x in for_hire_classes else 'Not For Hire Vehicles')

# Convert 'Month/Year' column to string type to avoid tick boxes
data_filtered['Month/Year'] = data_filtered['Month/Year'].astype(str)

# Create a bar chart with Plotly
fig2 = px.bar(data_filtered, x='Category', y='Trips Per Day Shared', color='Month/Year', barmode='group',
              title='Total Shared Trips Comparison (2022-2023)')

# Customize the figure layout
fig2.update_layout(
    xaxis_title='Category',
    yaxis_title='Total Trips Per Day Shared',
    xaxis=dict(tickangle=-45),
    plot_bgcolor='white',  # Background color
)

# Set figure dimensions
fig2.update_layout(
    width=fig_width,
    height=fig_height
)

# Apply the custom color palette
fig2.update_traces(marker_color=color_palette)  # Update the bar colors

# Create columns to display figures and titles side by side
col1, col2, col3 = st.columns(3)

# Display the figure using st.plotly_chart within the specified column
with col1:
    st.write("Bar Chart: Total Shared Trips Comparison (2022-2023)")
    st.plotly_chart(fig2)
