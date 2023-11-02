import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import warnings

st.set_page_config(page_title="KPI 3", page_icon=":taxi:", layout="wide")

st.header("KPI: 5% increase in demand for airport taxi rides")
st.markdown("***")

green_2022 = pd.read_csv('green_2022-06.csv')

# Convert date columns to datetime
green_2022['lpep_pickup_datetime'] = pd.to_datetime(green_2022['lpep_pickup_datetime'])
green_2022['lpep_dropoff_datetime'] = pd.to_datetime(green_2022['lpep_dropoff_datetime'])

# Sidebar: Date Range Selection
st.sidebar.header("Date Range Selection")
start_date = st.sidebar.date_input("Start Date", datetime(2022, 6, 1))
end_date = st.sidebar.date_input("End Date", datetime(2022, 6, 30))

# Convert start_date and end_date to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the dataset based on selected date range
filtered_data = green_2022[(green_2022['lpep_pickup_datetime'] >= start_date) & (green_2022['lpep_pickup_datetime'] <= end_date)]

# Calculate demand growth
total_trips_growth = (filtered_data['trip_distance'].count() / green_2022['trip_distance'].count() - 1) * 100
total_passengers_growth = (filtered_data['passenger_count'].sum() / green_2022['passenger_count'].sum() - 1) * 100
total_revenue_growth = (filtered_data['total_amount'].sum() / green_2022['total_amount'].sum() - 1) * 100
demand_growth = (total_trips_growth + total_passengers_growth + total_revenue_growth) / 3

# Filter the data for trips to and from airports (location IDs 1, 132, and 138)
airport_data = filtered_data[filtered_data['DOLocationID'].isin([1, 132, 138])]

# Calculate the percentage growth in the number of passengers, number of trips, and revenue
airport_data['date'] = airport_data['lpep_pickup_datetime'].dt.date
passengers_growth = airport_data.groupby('date')['passenger_count'].count().pct_change() * 100
trips_growth = airport_data.groupby('date')['trip_distance'].count().pct_change() * 100
revenue_growth = airport_data.groupby('date')['total_amount'].sum().pct_change() * 100

# Sidebar: Banner for Demand Growth
demand_color = 'green' if demand_growth > 0 else 'red'
st.sidebar.markdown(f'<h1 style="color:black;font-size:20px;">Demand Growth</h1>', unsafe_allow_html=True)
st.sidebar.markdown(f'<h1 style="color:{demand_color};">{demand_growth:.2f}%</h1>', unsafe_allow_html=True)

# Add the Multiselect widget in the sidebar
selected_metrics = st.sidebar.multiselect("Select Metrics to Display", ["Passengers", "Trips", "Revenue"], default=["Passengers", "Trips", "Revenue"])

# Create columns to display figures side by side
col1, col2, col3 = st.columns(3)

# Define a consistent figure size
fig_width = 300
fig_height = 300

# Create a line chart for selected metrics
fig1 = go.Figure()
if "Passengers" in selected_metrics:
    fig1.add_trace(go.Scatter(x=passengers_growth.index, y=passengers_growth, name='Passengers', line=dict(color='grey')))
if "Trips" in selected_metrics:
    fig1.add_trace(go.Scatter(x=trips_growth.index, y=trips_growth, name='Trips', line=dict(color='#ADD8E6')))
if "Revenue" in selected_metrics:
    fig1.add_trace(go.Scatter(x=revenue_growth.index, y=revenue_growth, name='Revenue', line=dict(color='#90EE90')))
fig1.update_layout(
    width=fig_width,
    height=fig_height,
    xaxis=dict(
        tickvals=passengers_growth.index,
        ticktext=[i if i.day % 5 == 0 else '' for i in passengers_growth.index]
    ),
    hovermode="x unified"
)

# Line chart for variation in sum of passengers to/from airports by day
airport_passengers = airport_data.groupby(airport_data['lpep_pickup_datetime'].dt.strftime('%d-%m-%Y'))['passenger_count'].sum().reset_index()
fig2 = px.line(airport_passengers, x='lpep_pickup_datetime', y='passenger_count')
fig2.update_traces(line=dict(color='green'))

# Calculate date intervals with 5-day increments
min_date = pd.to_datetime(airport_passengers['lpep_pickup_datetime'].min(), format='%d-%m-%Y')
date_range = [min_date]
while date_range[-1] < pd.to_datetime(airport_passengers['lpep_pickup_datetime'].max(), format='%d-%m-%Y'):
    date_range.append(date_range[-1] + pd.DateOffset(days=5))

date_range_str = [date.strftime('%d-%m-%Y') for date in date_range]

fig2.update_xaxes(
    title_text=None,
)
fig2.update_yaxes(title_text="Passenger Count")  # Set the y-axis title
fig2.update_layout(
    width=fig_width,
    height=fig_height,
    xaxis=dict(
        tickvals=airport_passengers.index,
        ticktext=[date if idx % 5 == 0 else '' for idx, date in enumerate(airport_passengers['lpep_pickup_datetime'])]
    ),
    hovermode="x unified"
)

# Donut chart for trips to and from airports
total_trips = filtered_data['trip_distance'].count()
airport_trips = airport_data['trip_distance'].count()
other_trips = total_trips - airport_trips
fig3 = go.Figure(data=[go.Pie(labels=['Airport Transfers', 'Other Trips'], values=[airport_trips, other_trips])])
fig3.update_traces(marker=dict(colors=['blue', 'green']))
fig3.update_traces(hole=0.4)
fig3.update_layout(
    width=fig_width,
    height=fig_height,
    xaxis=dict(tickvals=passengers_growth.index),
    hovermode="x unified"
)

# Bar chart for top 10 pickup location IDs ending at airports
# Filter data for trips with destinations at airports
airport_trips = airport_data[airport_data['DOLocationID'].isin([1, 132, 138])]

# Count the number of trips for each pickup location ID
pickup_location_counts = airport_trips['PULocationID'].value_counts()

# Get the top 10 pickup location IDs in descending order
top_10_pickup_ids = pickup_location_counts.nlargest(10).sort_index(ascending=False)

fig4 = px.bar(top_10_pickup_ids, x=top_10_pickup_ids.index, y=top_10_pickup_ids.values)
fig4.update_traces(marker=dict(color='green'))
fig4.update_layout(
    width=fig_width,
    height=fig_height,
    hovermode="x unified"
)
fig4.update_xaxes(categoryorder="total descending")
fig4.update_xaxes(title_text="Pick-Up Location ID")
fig4.update_yaxes(title_text="Trips Count")

# Bar chart for airport trips by day of the week
airport_data['day_of_week'] = airport_data['lpep_pickup_datetime'].dt.day_name()
airport_day_of_week = airport_data['day_of_week'].value_counts()
fig5 = px.bar(airport_day_of_week, x=airport_day_of_week.index, y=airport_day_of_week.values)
fig5.update_traces(marker=dict(color='grey'))
fig5.update_layout(
    width=fig_width,
    height=fig_height,
    xaxis=dict(tickvals=passengers_growth.index),
    hovermode="x unified"
)
fig5.update_xaxes(categoryorder="array", categoryarray=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
fig5.update_xaxes(title_text="Day of the Week")
fig5.update_yaxes(title_text="Trips Count")

# Display figures in columns
with col1:
    st.write("Percentage Growth (Trips, Passengers and Revenue)")
    st.plotly_chart(fig1, use_container_width=True)
    st.write("Number of passengers to and from airports")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.write("Airport Transfers vs. Other Trips")
    st.plotly_chart(fig3, use_container_width=True)

with col3:
    st.write("Top 10 Pick-Up points with airports as a destination")
    st.plotly_chart(fig4, use_container_width=True)
    st.write("Number of airport trips by day of the week")
    st.plotly_chart(fig5, use_container_width=True)




