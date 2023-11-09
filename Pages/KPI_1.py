import streamlit as st
import pymysql
import pyathena
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


def display_KPI_1_page():

    st.header("KPI: 2% increase in demand in For-Hire service")
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

    # SQL query for KPI calculation including trips growth
    kpi_query = """
        SELECT
            ((final.trip_distance - initial.trip_distance) / initial.trip_distance +
            (final.total_amount - initial.total_amount) / initial.total_amount +
            ((final.total_trips - initial.total_trips) / initial.total_trips)) * 100 / 3 AS demand_increase
        FROM
            (SELECT AVG(trip_distance) AS trip_distance, SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2022) AS initial,
            (SELECT AVG(trip_distance) AS trip_distance, SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2023) AS final
    """

    # Execute the SQL query and retrieve the results
    with conn.cursor() as cursor:
        cursor.execute(kpi_query)
        demand_increase = cursor.fetchone()

    # Define the title_suffix
    title_suffix = "For-Hire Vehicles"

    # Define KPI objective
    kpi_objective = 2

    # Create a banner to display the KPI status
    kpi_style = f"""
        padding: 10px;
        font-size: 20px;
        border-radius: 10px;
        color: white;
        display: flex;
        justify-content: space-between;
        background-color: {"#4CAF50" if demand_increase[0] >= kpi_objective else "#FF5733"};
    """
    st.markdown(f'<div style="{kpi_style}">Goal: {kpi_objective}%<div>{"KPI goal met!" if demand_increase[0] >= kpi_objective else "KPI not met"}</div></div>', unsafe_allow_html=True)

    # Display the KPI banner
    if demand_increase[0] >= 2:
        st.success(f'Demand for {title_suffix} service increased by {demand_increase[0]:.2f}%.')
    elif demand_increase[0] >= 0:
        st.error(f'Demand for {title_suffix} service increased by only {demand_increase[0]:.2f}%.')
    else:
        st.error(f'Demand for {title_suffix} service decreased by {demand_increase[0]:.2f}%.')



    # Create selectboxes in the Streamlit sidebar for filtering by "type_service" and "year"
    filter_service_type_id = st.sidebar.selectbox("Filter by service type", ["Both", "For-Hire", "Not For-Hire"])
    filter_year = st.sidebar.selectbox("Filter by year", ["Both", "2022", "2023"])

    # Define SQL query based on the selected filter options
    if filter_service_type_id == "For-Hire":
        type_service_condition = "type_service = 1"
    elif filter_service_type_id == "Not For-Hire":
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



#First graph:
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
            WHERE year = 2022) AS initial,
            (SELECT AVG(trip_distance) AS trip_distance, 
                    SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2023) AS final
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

#Second Graph:
    # Define the base SQL query to calculate the count of airport trips and non-airport trips
<<<<<<< HEAD
    # Combine conditions with the base query

    # Define the base SQL query to calculate the count of airport trips and non-airport trips
    base_donut_query = """
        SELECT
            CASE
                WHEN type_service = 1 THEN 'For-Hire'
                WHEN type_service = 0 THEN 'Not For-Hire'
                ELSE 'Other'
            END AS trip_type,
            COUNT(*) AS trip_count
        FROM trips_data
        WHERE type_service IN (0, 1)
        GROUP BY trip_type
    """
=======
    base_donut_query = '''
    SELECT
        CASE
            WHEN service_type_id = 1 THEN 'For-Hire'
            WHEN service_type_id = 0 THEN 'Not For-Hire'
            ELSE 'Other'
        END AS trip_type,
        COUNT(CASE WHEN service_type_id IN (0, 1) THEN 1 ELSE NULL END) AS trip_count
    FROM trips_data
    GROUP BY
        CASE
            WHEN service_type_id = 1 THEN 'For-Hire'
            WHEN service_type_id = 0 THEN 'Not For-Hire'
            ELSE 'Other'
        END'''
>>>>>>> fb42b5f7e86382638bcb6126eb56c91b6e8385d5

    donut_query = f"{base_donut_query} WHERE 1=1 {type_service_condition} {year_condition} GROUP BY trip_type"

    # Add conditions to the SQL query based on selected filters
    if filter_service_type_id== "For-Hire":
        service_type_id_condition = "AND service_type_id = 1"
    elif filter_service_type_id == "Not For-Hire":
        service_type_id_condition = "AND service_type_id= 0"
    else:  # "Both" (no filter)
        service_type_id_condition = ""

    if filter_year == "2022":
        year_condition = "AND year = 2022"
    elif filter_year == "2023":
        year_condition = "AND year = 2023"
    else:  # "Both" (no filter)
        year_condition = ""

    # Combine conditions with the base query
    #donut_query = base_donut_query + f" WHERE 1=1 {service_type_id_condition} {year_condition} GROUP BY trip_type"
    #donut_query = base_donut_query + f"GROUP BY trip_type HAVING 1=1 {service_type_id_condition} {year_condition}"
    # Execute the donut query and fetch the result
    cursor.execute(base_donut_query)
    donut_data = cursor.fetchall()

    # Create a DataFrame from the SQL query result
    df_donut = pd.DataFrame(donut_data, columns=['service_type_id', 'trip_count'])

    # Create a donut chart using Plotly Go with specified colors for slices
    fig_2 = go.Figure(data=[
        go.Pie(
            labels=df_donut['service_type_id'],
            values=df_donut['trip_count'],
            marker=dict(colors=color_palette)
        )
    ])

    # Update the title and other properties of the donut chart
    fig_2.update_layout(
        title='Airport Trips vs. Other Trips',
        showlegend=False,
        width=fig_width,
        height=fig_height
    )

    # Display the donut chart in your Streamlit app
    col2.plotly_chart(fig_2)

    # SQL query to join trips_data with taxi_zone and count trips to airport destinations
    top_pickup_query = """
        SELECT tz.location_name, COUNT(*) AS trip_count
        FROM trips_data AS td
        JOIN Locations AS tz
        ON td.pulocationid = tz.location_id
    """

    # Add conditions based on the filter_service_type_id value
    if filter_service_type_id == "For-Hire":
        top_pickup_query += " AND td.type_service = 1"
    elif filter_service_type_id == "Not For-Hire":
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
        GROUP BY tz.location_name
        ORDER BY trip_count DESC
        LIMIT 10
    """

    # Execute the SQL query and fetch the result
    cursor.execute(top_pickup_query)
    top_pickup_data = cursor.fetchall()

    # Create a DataFrame from the SQL query result
    df_top_pickup = pd.DataFrame(top_pickup_data, columns=['location_name', 'trip_count'])

    # Sort the DataFrame by trip_count in descending order (for the bar chart)
    df_top_pickup = df_top_pickup.sort_values(by='trip_count', ascending=False)

    # Create a bar chart using Plotly Go (with the name fig_3)
    fig_3 = go.Figure(go.Bar(
        x=df_top_pickup['location_name'],
        y=df_top_pickup['trip_count'],
        text=df_top_pickup['trip_count'],
        textposition='outside',
        marker_color=color_palette
    ))

    # Update the title and other properties of the bar chart
    fig_3.update_layout(
        title='Top 10 Pick-up Locations with Most Trips',
        xaxis_title='Location (Zone)',
        yaxis_title='Number of Trips',
        width=fig_width,
        height=fig_height
    )

    col3.plotly_chart(fig_3)
