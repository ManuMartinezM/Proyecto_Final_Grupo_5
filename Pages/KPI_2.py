import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import warnings

def display_KPI_2_page():

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

    # Define a custom color palette
    color_palette = ['#ADD8E6', '#90EE90', '#808080']

    # Create a sidebar slider to select the year range
    year_range = st.sidebar.slider("Select a year range:", 2015, 2023, (2021, 2023))

    # Filter the data based on the selected year range
    data_filtered = data_reports_monthly[data_reports_monthly['Month/Year'].str.contains('|'.join(map(str, range(year_range[0], year_range[1] + 1))))]

    # Define distinct colors for "For Hire" and "Not For Hire" categories
    category_colors = ['#ADD8E6', '#90EE90']

    # Create a bar chart with Plotly
    fig1 = px.bar(data_filtered, x='Month/Year', y='Trips Per Day Shared', title=f'Trend of Shared Trips ({year_range[0]}-{year_range[1]})')

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

    data_filtered['Category'] = data_filtered['License Class'].apply(lambda x: 'For Hire' if x in for_hire_classes else 'Not For Hire')

    # Group the data by 'Category' and 'Month/Year' and sum the shared trips
    grouped_data = data_filtered.groupby(['Category', 'Month/Year'])['Trips Per Day Shared'].sum().reset_index()

    # Create a pie chart with Plotly
    fig2 = px.pie(data_filtered, names='Category', title=f'Category Distribution ({year_range[0]}-{year_range[1]})',
                color_discrete_sequence=category_colors)

    # Set figure dimensions
    fig2.update_layout(
        width=fig_width,
        height=fig_height
    )

    # Display the figure using st.plotly_chart
    with col2:
        st.plotly_chart(fig2)

    # Create a stacked area chart with Plotly
    fig3 = px.area(data_filtered, x='Month/Year', y='Trips Per Day Shared', color='Category',
                title=f'Stacked Area Chart ({year_range[0]}-{year_range[1]})',
                labels={'Month/Year': 'Month/Year', 'Trips Per Day Shared': 'Total Trips Per Day Shared'},
                color_discrete_sequence=category_colors)

    # Customize the figure layout
    fig3.update_layout(
        xaxis_title='Month/Year',
        yaxis_title='Total Trips Per Day Shared',
        xaxis=dict(tickangle=-45),
        plot_bgcolor='white',  # Background color
    )

    # Set figure dimensions
    fig3.update_layout(
        width=fig_width,
        height=fig_height
    )

    # Display the figure using st.plotly_chart within the specified column
    with col3:
        st.plotly_chart(fig3)