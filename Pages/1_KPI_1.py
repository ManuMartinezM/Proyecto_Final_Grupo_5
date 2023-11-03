import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import warnings


st.set_page_config(page_title="KPI 1", page_icon=":taxi:", layout="wide")

st.header("KPI: 5% increase in demand in For-Hire service")
st.markdown("***")

fhv_2022 = pd.read_csv('clean_fhvhv_2022-06.csv')
fhv_2023 = pd.read_csv('clean_fhvhv_2023-06.csv')

green_2022 = pd.read_csv('clean_green_2022-06.csv')
green_2023 = pd.read_csv('clean_green_2023-06.csv')

yellow_2022 = pd.read_csv('clean_yellow_2022-06.csv')
yellow_2023 = pd.read_csv('clean_yellow_2023-06.csv')

# Create a Streamlit sidebar with a filter option for year
selected_year = st.sidebar.selectbox('Select Year', [2022, 2023, 'Both'], index=2)

# Define a function to retrieve the data based on the selected year
def get_data(year):
    if year == 2022:
        return (fhv_2022, green_2022, yellow_2022)
    elif year == 2023:
        return (fhv_2023, green_2023, yellow_2023)
    elif year == 'Both':
        return (pd.concat([fhv_2022, fhv_2023]), pd.concat([green_2022, green_2023]), pd.concat([yellow_2022, yellow_2023]))

fhv_data, green_data, yellow_data = get_data(selected_year)

# Create a Streamlit sidebar with a filter option
service_type = st.sidebar.selectbox('Select Service Type', ['For Hire', 'Not For Hire', 'Both'], index=2)  

# Combine the data for June 2022 and June 2023 based on the selected service type
if service_type == 'For Hire':
    combined_data = pd.concat([fhv_2022, fhv_2023])
    title_suffix = 'For Hire'
elif service_type == 'Not For Hire':
    combined_data = pd.concat([green_2022, green_2023, yellow_2022, yellow_2023])
    title_suffix = 'Not For Hire'
else:
    combined_data = pd.concat([fhv_2022, fhv_2023, green_2022, green_2023, yellow_2022, yellow_2023])
    title_suffix = 'All'

# Filter the data to only include the month of June
combined_data = combined_data[(combined_data['year'].isin([2022, 2023])) & (combined_data['month'] == 6)]

# Calculate the annual count of trips for the selected service type for June 2022 and June 2023
annual_counts = combined_data.groupby(['year']).size()

# Calculate the total monthly trip count for the selected service type
monthly_counts = combined_data.groupby(['year', 'month']).size().unstack(fill_value=0)

# Calculate the average trip distance for the selected service type
avg_distance = combined_data.groupby(['year'])['trip_distance'].mean()


# Calculate the percentage change in demand for the selected service type
demand_increase = (
    (annual_counts[2023] - annual_counts[2022]) / annual_counts[2022]
) * 100

# KPI objective
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
    st.success(f'Demand for {title_suffix} service increased by {demand_increase:.2f}%.')
elif demand_increase >= 0:
    st.error(f'Demand for {title_suffix} service increased by only {demand_increase:.2f}%.')
else:
    st.error(f'Demand for {title_suffix} service decreased by {demand_increase:.2f}%.')

# Define a custom color palette
color_palette = ['#ADD8E6', '#90EE90', '#808080']

# Define a consistent figure size
fig_width = 300
fig_height = 300

# Create columns to display figures and titles side by side
col1, col2, col3 = st.columns(3)

# Create a Plotly bar chart for annual count of trips for the selected service type
if service_type == 'Both':
    # Define colors for each category
    colors = [color_palette[0], color_palette[1]]

    # Create a new DataFrame to separate "For Hire" and "Not For Hire" data
    data_for_hire = combined_data[combined_data['type_service'] == 1]
    data_not_for_hire = combined_data[combined_data['type_service'] == 0]

    # Calculate the annual count of trips for "For Hire" and "Not For Hire"
    annual_counts_for_hire = data_for_hire.groupby(['year']).size()
    annual_counts_not_for_hire = data_not_for_hire.groupby(['year']).size()

    # Create stacked bar chart for annual count of trips (fig1)
    fig1 = go.Figure(data=[
        go.Bar(name='For Hire', x=annual_counts_for_hire.index, y=annual_counts_for_hire.values, marker_color=colors[0]),
        go.Bar(name='Not For Hire', x=annual_counts_not_for_hire.index, y=annual_counts_not_for_hire.values, marker_color=colors[1])
    ])
    fig1.update_layout(barmode='stack', xaxis_title='Year', yaxis_title='Count')
    fig1.update_layout(width=fig_width, height=fig_height)
    with col1:
        st.write("Annual Count of Trips by Service Type (Stacked)")
        st.plotly_chart(fig1)

else:
    if service_type != 'Both':
        # Create a Plotly bar chart for annual count of trips for the selected service type
        fig1 = px.bar(annual_counts, x=annual_counts.index, y=annual_counts.values, labels={'y': 'Count'})
        fig1.update_traces(marker_color=color_palette[0])
        fig1.update_layout(width=fig_width, height=fig_height)
        with col1:
            st.write(f'Annual Count of Trips for {title_suffix} Service')
            st.plotly_chart(fig1)

# Create a Plotly line chart for total monthly trip count for the selected service type
fig2 = px.line(monthly_counts, x=monthly_counts.index, y=monthly_counts.columns, labels={'y': 'Count'})
fig2.update_traces(line_color=color_palette[1])
fig2.update_layout(width=fig_width, height=fig_height)
with col2:
    st.write(f'Total Monthly Trip Count for {title_suffix} Service')
    st.plotly_chart(fig2)

# Create a Plotly bar chart for average trip distance for the selected service type
if service_type == 'Both':
    # Create a new DataFrame to separate "For Hire" and "Not For Hire" data
    data_for_hire = combined_data[combined_data['type_service'] == 1]
    data_not_for_hire = combined_data[combined_data['type_service'] == 0]

    # Calculate the average trip distance for "For Hire" and "Not For Hire"
    avg_distance_for_hire = data_for_hire.groupby(['year'])['trip_distance'].mean()
    avg_distance_not_for_hire = data_not_for_hire.groupby(['year'])['trip_distance'].mean()

    # Create stacked bar chart for average trip distance (fig3)
    fig3 = go.Figure(data=[
        go.Bar(name='For Hire', x=avg_distance_for_hire.index, y=avg_distance_for_hire.values, marker_color=color_palette[0]),
        go.Bar(name='Not For Hire', x=avg_distance_not_for_hire.index, y=avg_distance_not_for_hire.values, marker_color=color_palette[1])
    ])
    fig3.update_layout(barmode='stack', xaxis_title='Year', yaxis_title='Average Distance')
    fig3.update_layout(width=fig_width, height=fig_height)
    with col1:
        st.write("Annual Distance by Service Type (Stacked)")
        st.plotly_chart(fig3)

else:
    if service_type != 'Both':
        # Create a Plotly bar chart for average trip distance for the selected service type
        fig3 = px.bar(avg_distance, x=avg_distance.index, y=avg_distance.values, labels={'y': 'Average Distance'})
        fig3.update_traces(marker_color=color_palette[2])
        fig3.update_layout(width=fig_width, height=fig_height)
        with col1:
            st.write(f'Annual Distance for {title_suffix} Service')
            st.plotly_chart(fig3)

# Calculate the annual count of trips for 'For Hire' service for June 2022 and June 2023
if service_type in ['For Hire', 'Both']:
    annual_counts_for_hire = combined_data[combined_data['type_service'] == 1].groupby(['year']).size()
else:
    annual_counts_for_hire = pd.Series([0, 0], index=[2022, 2023])

# Calculate the annual count of trips for 'Green' and 'Yellow' services for June 2022 and June 2023
if service_type in ['Not For Hire', 'Both']:
    annual_counts_green_yellow = combined_data[combined_data['type_service'] == 0].groupby(['year']).size()
else:
    annual_counts_green_yellow = pd.Series([0, 0], index=[2022, 2023])

# Create a Plotly line chart to compare 'For Hire' and 'Green/Yellow' services for June 2022 and June 2023
fig4 = go.Figure()

if service_type == 'For Hire':
    fig4.add_trace(go.Scatter(x=[2022, 2023], y=[annual_counts_for_hire[2022], annual_counts_for_hire[2023]], mode='lines', name='For Hire', line=dict(color=color_palette[0])))
elif service_type == 'Not For Hire':
    fig4.add_trace(go.Scatter(x=[2022, 2023], y=[annual_counts_green_yellow[2022], annual_counts_green_yellow[2023]], mode='lines', name='Green/Yellow', line=dict(color=color_palette[1])))

if service_type == 'Both':
    fig4.add_trace(go.Scatter(x=[2022, 2023], y=[annual_counts_for_hire[2022], annual_counts_for_hire[2023]], mode='lines', name='For Hire', line=dict(color=color_palette[0])))
    fig4.add_trace(go.Scatter(x=[2022, 2023], y=[annual_counts_green_yellow[2022], annual_counts_green_yellow[2023]], mode='lines', name='Green/Yellow', line=dict(color=color_palette[1])))
fig4.update_layout(width=fig_width, height=fig_height)
with col2:
    st.write('Comparison of For Hire and Green/Yellow Services')
    st.plotly_chart(fig4)

# Calculate the count of trips by service type for both 'For Hire' and 'Not For Hire'
for_hire_counts = combined_data[combined_data['type_service'] == 1]['type_service'].count()
not_for_hire_counts = combined_data[combined_data['type_service'] == 0]['type_service'].count()

# Create a pie chart for service type distribution
if service_type == 'Both':
    labels = ['For Hire', 'Not For Hire']
    values = [for_hire_counts, not_for_hire_counts]
    colors = [color_palette[0], color_palette[1]]  # Light blue for 'For Hire' and light green for 'Not For Hire'

    fig5 = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    fig5.update_traces(textinfo='percent', textfont_size=15)
    fig5.update_layout(width=fig_width, height=fig_height)
    with col3:
        st.write('Service Type Distribution')
        st.plotly_chart(fig5)

# Calculate the revenue for "For Hire" and "Not For Hire" services for June 2022 and June 2023
revenue_for_hire = combined_data[combined_data['type_service'] == 1].groupby(['year'])['total_amount'].sum()
revenue_not_for_hire = combined_data[combined_data['type_service'] == 0].groupby(['year'])['total_amount'].sum()

# Create a pie chart for revenue distribution
if service_type == 'Both':
    labels = ['For Hire', 'Not For Hire']
    values = [revenue_for_hire[2023], revenue_not_for_hire[2023]]  # Use data for June 2023
    colors = [color_palette[0], color_palette[1]]  # Light blue for 'For Hire' and light green for 'Not For Hire'

    fig6 = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    fig6.update_traces(textinfo='percent', textfont_size=15)
    fig6.update_layout(width=fig_width, height=fig_height)

    with col3:
        st.write('Revenue Distribution for Both Services')
        st.plotly_chart(fig6)