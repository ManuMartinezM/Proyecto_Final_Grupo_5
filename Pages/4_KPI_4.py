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

fhv_2022 = pd.read_csv('clean_fhvhv_2022-06.csv')
fhv_2023 = pd.read_csv('clean_fhvhv_2023-06.csv')

green_2022 = pd.read_csv('clean_green_2022-06.csv')
green_2023 = pd.read_csv('clean_green_2023-06.csv')

yellow_2022 = pd.read_csv('clean_yellow_2022-06.csv')
yellow_2023 = pd.read_csv('clean_yellow_2023-06.csv')

# Sidebar
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-06-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2022-06-30"))

# Filter data based on selected date range
filtered_fhv_2022 = fhv_2022[(fhv_2022['year'] == 2022) & (fhv_2022['month'] == 6) & (fhv_2022['day'] >= start_date.day) & (fhv_2022['day'] <= end_date.day)]
filtered_fhv_2023 = fhv_2023[(fhv_2023['year'] == 2023) & (fhv_2023['month'] == 6) & (fhv_2023['day'] >= start_date.day) & (fhv_2023['day'] <= end_date.day)]

# Calculate demand growth
demand_growth = (
    ((filtered_fhv_2023['trip_distance'].count() - filtered_fhv_2022['trip_distance'].count()) / filtered_fhv_2022['trip_distance'].count()) +
    ((filtered_fhv_2023['passenger_count'].sum() - filtered_fhv_2022['passenger_count'].sum()) / filtered_fhv_2022['passenger_count'].sum()) +
    ((filtered_fhv_2023['total_amount'].sum() - filtered_fhv_2022['total_amount'].sum()) / filtered_fhv_2022['total_amount'].sum())
) / 3

# Main Dashboard
st.title("New York City Taxi Service Analysis")
st.markdown(f"**Demand Growth**: {demand_growth * 100:.2f}%")
if demand_growth > 0:
    st.markdown('<font color="green">**Positive Growth**</font>', unsafe_allow_html=True)
else:
    st.markdown('<font color="red">**Negative Growth**</font>', unsafe_allow_html=True)

# Line Chart for growth
st.header("Percentage Growth in Number of Trips, Passengers, and Revenue")
selected_metrics = st.multiselect("Select Metrics", ["Number of Trips", "Number of Passengers", "Total Revenue"], default=["Number of Trips"])
fig = go.Figure()

if "Number of Trips" in selected_metrics:
    fig.add_trace(go.Scatter(x=filtered_fhv_2022['day'], y=filtered_fhv_2022['trip_distance'], mode='lines', name='Trips (2022)', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=filtered_fhv_2023['day'], y=filtered_fhv_2023['trip_distance'], mode='lines', name='Trips (2023)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=filtered_fhv_2022['day'], y=filtered_fhv_2022['passenger_count'], mode='lines', name='Passengers (2022)', line=dict(color='grey')))
    fig.add_trace(go.Scatter(x=filtered_fhv_2023['day'], y=filtered_fhv_2023['passenger_count'], mode='lines', name='Passengers (2023)', line=dict(color='blue')))
if "Total Revenue" in selected_metrics:
    fig.add_trace(go.Scatter(x=filtered_fhv_2022['day'], y=filtered_fhv_2022['total_amount'], mode='lines', name='Revenue (2022)', line=dict(color='grey')))
    fig.add_trace(go.Scatter(x=filtered_fhv_2023['day'], y=filtered_fhv_2023['total_amount'], mode='lines', name='Revenue (2023)', line=dict(color='blue')))

fig.update_layout(title="Percentage Growth Over Time",
                  xaxis_title="Day",
                  yaxis_title="Count/Sum",
                  hovermode="x unified")
st.plotly_chart(fig)

# Line Chart for sum of passengers to/from airports
st.header("Sum of Passengers to/from Airports by Day")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=filtered_fhv_2022['day'], y=filtered_fhv_2022[filtered_fhv_2022['DOLocationID'].isin([1, 132, 138])]['passenger_count'].sum(), mode='lines', name='Passengers to/from Airports (2022)', line=dict(color='green')))
fig2.add_trace(go.Scatter(x=filtered_fhv_2023['day'], y=filtered_fhv_2023[filtered_fhv_2023['DOLocationID'].isin([1, 132, 138])]['passenger_count'].sum(), mode='lines', name='Passengers to/from Airports (2023)', line=dict(color='blue')))

fig2.update_layout(title="Sum of Passengers to/from Airports by Day",
                   xaxis_title="Day",
                   yaxis_title="Total Passengers",
                   hovermode="x unified")
st.plotly_chart(fig2)

# Donut Chart for airport trips
st.header("Proportion of Airport Trips")
fig3 = px.pie(filtered_fhv_2023[filtered_fhv_2023['DOLocationID'].isin([1, 132, 138])], names="DOLocationID",
              title="Airport Trips",
              color_discrete_sequence=['blue', 'green', 'grey'])
st.plotly_chart(fig3)

# Bar Chart for top pick-up locations
st.header("Top Pick-up Locations Ending at Airports")
top_pickup_locations = filtered_fhv_2023[filtered_fhv_2023['DOLocationID'].isin([1, 132, 138])]['PULocationID'].value_counts().nlargest(10)
fig4 = px.bar(top_pickup_locations, x=top_pickup_locations.index, y=top_pickup_locations.values, color=top_pickup_locations.index,
              labels={'x': 'Pick-up Location ID', 'y': 'Trips'},
              title="Top 10 Pick-up Locations Ending at Airports",
              color_discrete_sequence=['green'])
st.plotly_chart(fig4)

# Bar Chart for airport trips by day of the week
st.header("Airport Trips by Day of the Week")
filtered_fhv_2023['day_of_week'] = filtered_fhv_2023['day'].apply(lambda x: pd.Timestamp(f"2023-06-{x}").day_name())
airport_trips_by_day = filtered_fhv_2023[filtered_fhv_2023['DOLocationID'].isin([1, 132, 138])]['day_of_week'].value_counts()
fig5 = px.bar(airport_trips_by_day, x=airport_trips_by_day.index, y=airport_trips_by_day.values, labels={'x': 'Day of the Week', 'y': 'Trips'},
              title="Airport Trips by Day of the Week",
              color_discrete_sequence=['grey'])
st.plotly_chart(fig5)