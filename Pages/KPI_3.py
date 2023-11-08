import streamlit as st
import pymysql
import pyathena
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def display_KPI_3_page():

    st.header("KPI: 5% increase in demand in airport taxi rides")
    st.markdown("***")

    # Replace these values with your database information
    host = 'database-1.cb8vqbpvimzr.us-east-2.rds.amazonaws.com'
    user = 'admin'
    password = 'adminadmin'
    database = 'NYC_TAXIS'

    # Establish a connection to the database
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()

    # SQL query for KPI calculation including trips growth
    kpi_query = """
        SELECT
            ((final.trip_distance - initial.trip_distance) / initial.trip_distance +
            (final.total_amount - initial.total_amount) / initial.total_amount +
            ((final.total_trips - initial.total_trips) / initial.total_trips)) * 100 / 3 AS demand_increase
        FROM
            (SELECT AVG(trip_distance) AS trip_distance, SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2022
            AND (PULocationID IN (1, 132, 138) OR DOLocationID IN (1, 132, 138)) ) AS initial,
            (SELECT AVG(trip_distance) AS trip_distance, SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2023
            AND (PULocationID IN (1, 132, 138) OR DOLocationID IN (1, 132, 138)) ) AS final
    """

    # Execute the KPI query and fetch the result
    cursor.execute(kpi_query)
    demand_increase = cursor.fetchone()[0]

    # Define the title and KPI objective
    title_suffix = "Airport Trips"
    kpi_objective = 5

    # Create a banner to display the KPI status
    kpi_style = f"""
        padding: 10px;
        font-size: 20px;
        border-radius: 10px;
        color: white;
        display: flex;
        justify-content: space-between;
        background-color: {"#4CAF50" if demand_increase >= kpi_objective else "#FF5733"};
    """
    st.markdown(f'<div style="{kpi_style}">Goal: {kpi_objective}%<div>{"KPI goal met!" if demand_increase >= kpi_objective else "KPI not met"}</div></div>', unsafe_allow_html=True)

    # Display the KPI banner
    if demand_increase >= 5:
        st.success(f'Demand for {title_suffix} service increased by {demand_increase:.2f}%.')
    elif demand_increase >= 0:
        st.error(f'Demand for {title_suffix} service increased by only {demand_increase:.2f}%.')
    else:
        st.error(f'Demand for {title_suffix} service decreased by {demand_increase:.2f}%.')

    # Create selectboxes in the Streamlit sidebar for filtering by "type_service" and "year"
    filter_type_service = st.sidebar.selectbox("Filter by service type", ["Both", "For-Hire", "Not For-Hire"])
    filter_year = st.sidebar.selectbox("Filter by year", ["Both", "2022", "2023"])

    # Define SQL query based on the selected filter options
    if filter_type_service == "For-Hire":
        type_service_condition = "type_service = 1"
    elif filter_type_service == "Not For-Hire":
        type_service_condition = "type_service = 0"
    else:  # "Both" (no filter)
        type_service_condition = "1=1"

    if filter_year == "2022":
        year_condition = "year = 2022"
    elif filter_year == "2023":
        year_condition = "year = 2023"
    else:  # "Both" (no filter)
        year_condition = "1=1"

    # Define a custom color palette
    color_palette = ['#ADD8E6', '#90EE90', '#FFA07A', '#D3D3D3', '#FFFFE0', '#87CEEB', '#98FB98', '#FFD700', '#C0C0C0', '#FFA500']

    # Define a consistent figure size
    fig_width = 350
    fig_height = 450

    # Create columns to display figures and titles side by side
    col1, col2, col3 = st.columns(3)

    # Add conditions to the SQL query based on selected filters
    if filter_type_service == "For-Hire":
        type_service_condition = "AND type_service = 1"
    elif filter_type_service == "Not For-Hire":
        type_service_condition = "AND type_service = 0"
    else:  # "Both" (no filter)
        type_service_condition = ""

    # SQL query for calculating percentage growth of each variable with filter
    growth_query = f"""
        SELECT
            ((final.trip_distance - initial.trip_distance) / initial.trip_distance) * 100 AS distance_growth,
            ((final.total_amount - initial.total_amount) / initial.total_amount) * 100 AS revenue_growth,
            ((final.total_trips - initial.total_trips) / initial.total_trips) * 100 AS trips_growth
        FROM
            (SELECT AVG(trip_distance) AS trip_distance, 
                    SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2022
            AND (PULocationID IN (1, 132, 138) OR DOLocationID IN (1, 132, 138) {type_service_condition}) ) AS initial,
            (SELECT AVG(trip_distance) AS trip_distance, 
                    SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2023
            AND (PULocationID IN (1, 132, 138) OR DOLocationID IN (1, 132, 138) {type_service_condition}) ) AS final
    """

    # Execute the percentage growth query
    cursor.execute(growth_query)
    growth_values = cursor.fetchone()

    # Extract growth values for distance, revenue, and trips
    distance_growth,revenue_growth, trips_growth = growth_values

    # Create a DataFrame for the percentage growth values
    metrics = ["Trips", "Distance", "Revenue"]
    growth = [trips_growth, distance_growth, revenue_growth]

    df_growth = pd.DataFrame({'Metrics': metrics, 'Growth': growth})

    # Create a bar chart using Plotly
    fig_1 = go.Figure()

    fig_1.add_trace(go.Bar(
        x=df_growth['Metrics'],
        y=df_growth['Growth'],
        text=df_growth['Growth'].apply(lambda x: f'{x:.2f}%'),
        marker_color=color_palette
    ))

    # Update the title and axis labels
    fig_1.update_layout(
        title='Percentage Growth of Trips, Distance and Revenue',
        xaxis_title='Metrics',
        yaxis_title='Percentage Growth',
        width=fig_width,
        height=fig_height
    )

    # Display the bar chart in your Streamlit app
    col1.plotly_chart(fig_1)

    # Define the base SQL query to calculate the count of airport trips and non-airport trips
    base_donut_query = """
        SELECT
            CASE
                WHEN PULocationID IN (1, 132, 138) OR DOLocationID IN (1, 132, 138) THEN 'Airport Trips'
                ELSE 'Other Trips'
            END AS trip_type,
            COUNT(*) AS trip_count
        FROM trips_data
    """

    # Add conditions to the SQL query based on selected filters
    if filter_type_service == "For-Hire":
        type_service_condition = "AND type_service = 1"
    elif filter_type_service == "Not For-Hire":
        type_service_condition = "AND type_service = 0"
    else:  # "Both" (no filter)
        type_service_condition = ""

    if filter_year == "2022":
        year_condition = "AND year = 2022"
    elif filter_year == "2023":
        year_condition = "AND year = 2023"
    else:  # "Both" (no filter)
        year_condition = ""

    # Combine conditions with the base query
    donut_query = base_donut_query + f" WHERE 1=1 {type_service_condition} {year_condition} GROUP BY trip_type"

    # Execute the donut query and fetch the result
    cursor.execute(donut_query)
    donut_data = cursor.fetchall()

    # Create a DataFrame from the SQL query result
    df_donut = pd.DataFrame(donut_data, columns=['trip_type', 'trip_count'])

    # Create a donut chart using Plotly Go with specified colors for slices
    fig_2 = go.Figure(data=[
        go.Pie(
            labels=df_donut['trip_type'],
            values=df_donut['trip_count'],
            marker=dict(colors=color_palette)
        )
    ])

    # Update the title and other properties of the donut chart
    fig_2.update_layout(
        title='Airport Trips vs. Other Trips',
        showlegend=False,  # Hide legend to create a donut chart
        width=fig_width,
        height=fig_height
    )

    # Display the donut chart in your Streamlit app
    col2.plotly_chart(fig_2)

    # SQL query to join trips_data with taxi_zone and count trips to airport destinations
    top_pickup_query = """
        SELECT tz.Zone, COUNT(*) AS trip_count
        FROM trips_data AS td
        JOIN taxi_zone AS tz
        ON td.PULocationID = tz.LocationID
        WHERE DOLocationID IN (1, 132, 138)
    """

    # Add conditions based on the filter_type_service value
    if filter_type_service == "For-Hire":
        top_pickup_query += " AND td.type_service = 1"
    elif filter_type_service == "Not For-Hire":
        top_pickup_query += " AND td.type_service = 0"

    if filter_year == "2022":
        year_condition = " AND `year` = 2022"
    elif filter_year == "2023":
        year_condition = " AND `year` = 2023"
    else:  # "Both" (no filter)
        year_condition = ""

    # Add year filter condition
    top_pickup_query += year_condition

    top_pickup_query += """
        GROUP BY tz.Zone
        ORDER BY trip_count DESC
        LIMIT 10  # Select the top 10 locations with the most trips
    """

    # Execute the SQL query and fetch the result
    cursor.execute(top_pickup_query)
    top_pickup_data = cursor.fetchall()

    # Create a DataFrame from the SQL query result
    df_top_pickup = pd.DataFrame(top_pickup_data, columns=['Zone', 'trip_count'])

    # Sort the DataFrame by trip_count in descending order (for the bar chart)
    df_top_pickup = df_top_pickup.sort_values(by='trip_count', ascending=False)

    # Create a bar chart using Plotly Go (with the name fig_3)
    fig_3 = go.Figure(go.Bar(
        x=df_top_pickup['Zone'],
        y=df_top_pickup['trip_count'],
        text=df_top_pickup['trip_count'],
        textposition='outside',
        marker_color=color_palette
    ))

    # Update the title and other properties of the bar chart
    fig_3.update_layout(
        title='Top 10 Pick-up Locations with Most Trips to Airport Destinations',
        xaxis_title='Location (Zone)',
        yaxis_title='Number of Trips',
        width=fig_width,
        height=fig_height
    )

    col3.plotly_chart(fig_3)

    # SQL query to count trips for each day of the week and order by the desired order
    day_of_week_query = """
        SELECT DAYNAME(DATE(CONCAT(year, '-', month, '-', day))) AS day_of_week, COUNT(*) AS trip_count
        FROM trips_data
        WHERE year IN (2022, 2023)
        AND (PULocationID IN (1, 132, 138) OR DOLocationID IN (1, 132, 138))
    """

    # Add conditions based on the filter_type_service value
    if filter_type_service == "For-Hire":
        day_of_week_query += " AND type_service = 1"
    elif filter_type_service == "Not For-Hire":
        day_of_week_query += " AND type_service = 0"

    # Add conditions based on the filter_year value
    if filter_year == "2022":
        day_of_week_query += " AND year = 2022"
    elif filter_year == "2023":
        day_of_week_query += " AND year = 2023"

    # Group the data by day of the week
    day_of_week_query += """
        GROUP BY day_of_week
        ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    """

    # Execute the SQL query and fetch the result
    cursor.execute(day_of_week_query)
    day_of_week_data = cursor.fetchall()

    # Create a DataFrame from the SQL query result
    df_day_of_week = pd.DataFrame(day_of_week_data, columns=['Day of the Week', 'Trip Count'])

    # Create a Plotly Go bar chart (named fig_5)
    fig_4 = go.Figure(go.Bar(
        x=df_day_of_week['Day of the Week'],
        y=df_day_of_week['Trip Count'],
        text=df_day_of_week['Trip Count'],
        textposition='outside',
        marker_color=color_palette  # Use the color palette here
    ))

    # Update the title and other properties of the bar chart
    fig_4.update_layout(
        title='Number of Trips for Each Day of the Week',
        xaxis_title='Day of the Week',
        yaxis_title='Number of Trips',
        width=fig_width,
        height=fig_height
    )

    # Display the fig_5 bar chart in your Streamlit app
    col2.plotly_chart(fig_4)

    # Close the database connection
    connection.close()