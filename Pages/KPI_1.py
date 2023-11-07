import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.header("KPI: 5% increase in demand in For-Hire service")
st.markdown("***")

# Replace these values with your database information
host = 'database-1.cb8vqbpvimzr.us-east-2.rds.amazonaws.com'
user = 'admin'
password = 'adminadmin'
database = 'NYC_TAXIS'

# Establish a connection to the database
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

# Create a function to fetch data from the database
def fetch_data():
    query = "SELECT * FROM trips_data"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# Calculate the KPI directly using SQL queries
kpi_query = """
    SELECT
        ((final.trip_distance - initial.trip_distance) / initial.trip_distance +
        (final.total_amount - initial.total_amount) / initial.total_amount +
        ((final.total_trips - initial.total_trips) / initial.total_trips)) * 100 / 3 AS demand_increase
    FROM
        (SELECT SUM(trip_distance) AS trip_distance, SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
        FROM trips_data WHERE year = 2022 AND type_service = 1) AS initial,
        (SELECT SUM(trip_distance) AS trip_distance, SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
        FROM trips_data WHERE year = 2023 AND type_service = 1) AS final
"""
cursor.execute(kpi_query)
demand_increase_result = cursor.fetchone()
demand_increase = demand_increase_result[0] if demand_increase_result is not None else None

# Define the title_suffix
title_suffix = "For-Hire Vehicles"

# Define KPI objective
kpi_objective = 5  # Adjust this value as needed

# Define CSS styles based on KPI status (met or not met)
kpi_style = f"""
    padding: 10px;
    font-size: 20px;
    border-radius: 10px;
    color: white;
    display: flex;
    justify-content: space-between;
    background-color: {"#4CAF50" if demand_increase and demand_increase >= kpi_objective else "#FF5733"};
"""

# Display the KPI banner
st.markdown(f'<div style="{kpi_style}">Goal: {kpi_objective}%<div>{"KPI goal met!" if demand_increase and demand_increase >= kpi_objective else "KPI not met"}</div></div>', unsafe_allow_html=True)

# Display the KPI banner
if demand_increase and demand_increase >= 5:
    st.success(f'Demand for {title_suffix} service increased by {demand_increase:.2f}%.')
elif demand_increase and demand_increase >= 0:
    st.error(f'Demand for {title_suffix} service increased by only {demand_increase:.2f}%.')
elif demand_increase is not None:
    st.error(f'Demand for {title_suffix} service decreased by {demand_increase:.2f}%.')

# Add a selectbox in the sidebar for type of service filter
service_filter = st.sidebar.selectbox("Filter by Type of Service", ["Both", "For-Hire", "Not For-Hire"])

# Define a custom color palette
color_palette = ['#ADD8E6', '#90EE90', '#FFA07A', '#D3D3D3', '#FFFFE0', '#87CEEB', '#98FB98', '#FFD700', '#C0C0C0', '#FFA500']

# Define a consistent figure size
fig_width = 350
fig_height = 450

# Create columns to display figures and titles side by side
col1, col2, col3 = st.columns(3)

sql_query_1 = """
SELECT CONCAT(LPAD(month, 2, '0'), '-', year) AS month_year,
       AVG(CASE WHEN type_service = 0 THEN trip_distance ELSE NULL END) AS Not_For_Hire,
       AVG(CASE WHEN type_service = 1 THEN trip_distance ELSE NULL END) AS For_Hire
FROM trips_data
WHERE year IN (2022, 2023) AND month = 6
GROUP BY month_year
"""

# Use pandas to read the SQL query results into a DataFrame
df_1 = pd.read_sql(sql_query_1, connection)

# Create a data frame
data_1 = pd.DataFrame({
    "month_year": df_1["month_year"].astype(float),  # Convert the column to a numeric type
    "Not_For_Hire": df_1["Not_For_Hire"],
    "For_Hire": df_1["For_Hire"]
})

# Group the data by year
df_1_grouped = df_1.groupby("year").sum()

# Create a bar chart using Plotly Express
fig_1 = px.bar(
    df_1_grouped, 
    x=df_1_grouped.index,  # The years
    y=["Not_For_Hire", "For_Hire"],
    barmode="stack",
    color_discrete_sequence=color_palette
)

# Update the title and axis labels
fig_1.update_layout(
    title="Average Trip Distance Comparison",
    xaxis_title="Year",
    yaxis_title="Average Trip Distance (miles)",
    width=fig_width,
    height=fig_height
)

# Show the chart using Streamlit
col2.plotly_chart(fig_1)

sql_query_2 = """
SELECT type_service, COUNT(*) AS trip_count
FROM trips_data
WHERE year IN (2022, 2023) AND month = 6
GROUP BY type_service
"""

# Read the SQL query results into a DataFrame
df_2 = pd.read_sql(sql_query_2, connection)

# Create a DataFrame with the updated labels
df_2['type_service'] = df_2['type_service'].replace({0: 'Not For-Hire', 1: 'For-Hire'})

# Define custom colors for the pie chart
custom_colors = color_palette[::-1]  # Reverse the color palette to invert the colors

# Create a pie chart using Plotly Express with custom colors
fig_2 = px.pie(
    df_2,
    values="trip_count",
    names="type_service",
    labels={"type_service": "Type of Service"},
    color_discrete_sequence=custom_colors
)

# Customize the figure layout
fig_2.update_layout(
    title="Distribution of Trips by Type of Service",
    width=fig_width,
    height=fig_height
)

# Display the chart using Streamlit
col3.plotly_chart(fig_2)