import streamlit as st
import pymysql
import pyathena
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def display_KPI_2_page():

    st.header("KPI: 5% increase in demand for shared rides between 2022 and 2023")
    st.markdown("***")

    # Replace these values with your database information
    host = 'database-1.cb8vqbpvimzr.us-east-2.rds.amazonaws.com'
    user = 'admin'
    password = 'adminadmin'
    database = 'NYC_TAXIS'

    # Establish a connection to the database
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()

    # Define KPI objective
    kpi_objective = 5  # Adjust this value as needed

    # SQL query to calculate shared trips demand for 2022 and 2023
    sql_query = """
        SELECT
            SUM(CASE WHEN Year = 2022 THEN Total_Shared_Trips ELSE 0 END) AS shared_trips_2022,
            SUM(CASE WHEN Year = 2023 THEN Total_Shared_Trips ELSE 0 END) AS shared_trips_2023
        FROM data_report_monthly
    """

    # Execute the query
    cursor.execute(sql_query)
    shared_trips_data = cursor.fetchone()

    # Calculate the demand increase
    shared_trips_2022 = shared_trips_data[0]
    shared_trips_2023 = shared_trips_data[1]
    if shared_trips_2022 == 0:
        demand_increase = None
    else:
        demand_increase = ((shared_trips_2023 - shared_trips_2022) / shared_trips_2022) * 100

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
    title_suffix = "Shared Rides"
    if demand_increase and demand_increase >= 5:
        st.success(f'Demand for {title_suffix} increased by {demand_increase:.2f}%.')
    elif demand_increase and demand_increase >= 0:
        st.error(f'Demand for {title_suffix} increased by only {demand_increase:.2f}%.')
    elif demand_increase is not None:
        st.error(f'Demand for {title_suffix} decreased by {demand_increase:.2f}%.')

    # Sidebar filter for Type of Service
    service_filter = st.sidebar.selectbox("Filter by Type of Service", ["Both", "For-Hire", "Not For-Hire"])

    # Sidebar filter for Year
    year_filter = st.sidebar.selectbox("Filter by Year", ["Both", "2022", "2023"])

    # Define a custom color palette
    color_palette = ['#ADD8E6', '#90EE90', '#FFA07A', '#D3D3D3', '#FFFFE0', '#87CEEB', '#98FB98', '#FFD700', '#C0C0C0', '#FFA500']

    # Define a consistent figure size
    fig_width = 350
    fig_height = 450

    # Create columns to display figures and titles side by side
    col1, col2, col3 = st.columns(3)

    # Build the WHERE clause for SQL query based on filters
    where_clause = ""
    if service_filter != "Both":
        where_clause += f" AND License_Class = {'1' if service_filter == 'For-Hire' else '0'}"
    if year_filter != "Both":
        where_clause += f" AND Year = {year_filter}"

    # SQL query to calculate shared trips demand
    sql_query_1 = f"""
        SELECT
            Year,
            SUM(Total_Shared_Trips) AS Shared_Trips
        FROM data_report_monthly
        WHERE Year IN (2022, 2023){where_clause}
        GROUP BY Year
    """

    # Execute the query
    cursor.execute(sql_query_1)

    # Read the SQL query results into a DataFrame
    df_1 = pd.read_sql(sql_query_1, connection)

    # Define a custom color palette
    color_palette = ['#ADD8E6', '#90EE90']

    # Define a consistent figure size
    fig_width = 350
    fig_height = 450

    # Create columns to display figures and titles side by side
    col1, col2, col3 = st.columns(3)

    # Create a bar chart using Plotly Go
    fig_1 = go.Figure()

    fig_1.add_trace(go.Bar(
        x=df_1['Year'],
        y=df_1['Shared_Trips'],
        marker_color=color_palette,
    ))

    # Update the layout
    fig_1.update_layout(
        title="Number of Shared Trips",
        xaxis_title="Year",
        yaxis_title="Number of Shared Trips",
        xaxis={'type': 'category'},
        width=fig_width,
        height=fig_height
    )

    # Show the chart using Streamlit
    col1.plotly_chart(fig_1)

    # Define the SQL query for the pie chart
    sql_query_2 = """
        SELECT
            SUM(Total_Shared_Trips) AS Shared_Trips,
            SUM(Total_Trips) AS Total_Trips
        FROM data_report_monthly
        WHERE 1=1
    """

    # Modify the query based on the selected filters
    if service_filter == "For-Hire":
        sql_query_2 += " AND License_Class = '1'"
    elif service_filter == "Not For-Hire":
        sql_query_2 += " AND License_Class = '0'"

    # Use manual formatting for year filter
    if year_filter == "2022":
        sql_query_2 += " AND Year = 2022"
    elif year_filter == "2023":
        sql_query_2 += " AND Year = 2023"

    # Execute the SQL query and fetch the results
    cursor.execute(sql_query_2)
    data_2 = cursor.fetchall()

    # Create the pie chart
    shared_trips = data_2[0][0]
    total_trips = data_2[0][1]

    fig_2 = go.Figure(data=[go.Pie(
        labels=["Shared Trips", "Total Trips"],
        values=[shared_trips, total_trips],
        marker=dict(colors=color_palette)  # Set custom colors
    )])

    # Customize the figure layout
    fig_2.update_layout(
        title="Comparison of Shared Trips vs. Total Trips",
        width=fig_width,
        height=fig_height
    )

    # Show the chart using Streamlit
    col2.plotly_chart(fig_2)




    

    # Close the cursor and connection
    cursor.close()
    connection.close()