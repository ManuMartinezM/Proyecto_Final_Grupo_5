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

    # Define AWS credentials and Athena configuration
    aws_access_key_id = 'AKIAVXORHVGZHZV2PD53'
    aws_secret_access_key = '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'
    athena_database = 'athena-test-db'
    athena_s3_staging_dir = 's3://taxi-data-smart-analytics/athena/'
    aws_region = 'us-east-2'

    # Create a connection to Athena
    conn = pyathena.connect(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,    
        s3_staging_dir=athena_s3_staging_dir,
        schema_name=athena_database,
        region_name=aws_region
    ) 


    # Define KPI objective
    kpi_objective = 5  # Adjust this value as needed

    # SQL query to calculate shared trips demand for 2022 and 2023
    kpi_query = """
        SELECT
            SUM(CASE WHEN Year = 2022 THEN shared_trips_per_day ELSE 0 END) AS shared_trips_2022,
            SUM(CASE WHEN Year = 2023 THEN shared_trips_per_day ELSE 0 END) AS shared_trips_2023
        FROM monthly_reports
    """

    # Execute the SQL query and retrieve the results
    with conn.cursor() as cursor:
        cursor.execute(kpi_query)
        shared_trips_data = cursor.fetchall()

   # Check if shared_trips_data contains at least one row
    if len(shared_trips_data) > 0:
        shared_trips_2022 = shared_trips_data[0][0]
        shared_trips_2023 = shared_trips_data[0][1]
        if shared_trips_2022 == 0:
            shared_trips_data = None
        else:
            shared_trips_data = ((shared_trips_2023 - shared_trips_2022) / shared_trips_2022) * 100
    else:
        # Handle the case where the query did not return the expected data
        shared_trips_data = None

    # Define CSS styles based on KPI status (met or not met)
    kpi_style = f"""
        padding: 10px;
        font-size: 20px;
        border-radius: 10px;
        color: white;
        display: flex;
        justify-content: space-between;
        background-color: {"#4CAF50" if shared_trips_data and shared_trips_data >= kpi_objective else "#FF5733"};
    """

    # Display the KPI banner
    st.markdown(f'<div style="{kpi_style}">Goal: {kpi_objective}%<div>{"KPI goal met!" if shared_trips_data and shared_trips_data >= kpi_objective else "KPI not met"}</div></div>', unsafe_allow_html=True)


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
            SUM(shared_trips_per_day) AS Shared_Trips
        FROM monthly_reports
        WHERE Year IN (2022, 2023){where_clause}
        GROUP BY Year
    """

    # Execute the query
    cursor.execute(sql_query_1)

    # Read the SQL query results into a DataFrame
    df_1 = pd.read_sql(sql_query_1, conn)

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
            SUM(shared_trips_per_day) AS Shared_Trips,
            SUM(trips_per_day) AS trips_per_day
        FROM monthly_reports
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
