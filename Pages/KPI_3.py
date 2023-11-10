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
            WHERE year = 2022
            AND (pulocationid IN (1, 132, 138) OR dolocationid IN (1, 132, 138)) ) AS initial,
            (SELECT AVG(trip_distance) AS trip_distance, SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2023
            AND (pulocationid IN (1, 132, 138) OR dolocationid IN (1, 132, 138)) ) AS final
    """

    # Execute the SQL query and retrieve the results
    with conn.cursor() as cursor:
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

    # Define a custom color palette
    color_palette = ['#ADD8E6', '#90EE90', '#FFA07A', '#D3D3D3', '#FFFFE0', '#87CEEB', '#98FB98', '#FFD700', '#C0C0C0', '#FFA500']

    # Define a consistent figure size
    fig_width = 350
    fig_height = 450

    # Create columns to display figures and titles side by side
    col1, col2, col3 = st.columns(3)

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
            AND (pulocationid IN (1, 132, 138) OR dolocationid IN (1, 132, 138)) ) AS initial,
            (SELECT AVG(trip_distance) AS trip_distance, 
                    SUM(total_amount) AS total_amount, COUNT(*) AS total_trips
            FROM trips_data
            WHERE year = 2023
            AND (pulocationid IN (1, 132, 138) OR dolocationid IN (1, 132, 138)) ) AS final
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

    # Create a radio button for selecting the year for fig_2
    selected_year_fig_2 = col2.radio("Select Year:", [2022, 2023], key="year_fig_2", horizontal=True)

    # Define the base SQL query to calculate the count of airport trips and non-airport trips for fig_2
    base_donut_query_fig_2 = f'''
        SELECT
            CASE
                WHEN service_type_id = 1 THEN 'For-Hire'
                WHEN service_type_id = 0 THEN 'Not For-Hire'
                ELSE 'Other'
            END AS service_type_id,
            COUNT(*) AS trip_count
        FROM trips_data
        WHERE year = {selected_year_fig_2}
        AND (pulocationid IN (1, 132, 138) OR dolocationid IN (1, 132, 138))
    '''

    # Add GROUP BY for the CASE statement
    base_donut_query_fig_2 += """
        GROUP BY
            CASE
                WHEN service_type_id = 1 THEN 'For-Hire'
                WHEN service_type_id = 0 THEN 'Not For-Hire'
                ELSE 'Other'
            END
    """

    # Execute the donut query for fig_2 and fetch the result
    cursor.execute(base_donut_query_fig_2)
    donut_data_fig_2 = cursor.fetchall()

    # Create a DataFrame from the SQL query result for fig_2
    df_donut_fig_2 = pd.DataFrame(donut_data_fig_2, columns=['service_type_id', 'trip_count'])

    # Create a donut chart using Plotly Go with specified colors for slices for fig_2
    fig_2 = go.Figure(data=[
        go.Pie(
            labels=df_donut_fig_2['service_type_id'],
            values=df_donut_fig_2['trip_count'],
            marker=dict(colors=color_palette)
        )
    ])

    # Update the title and other properties of the donut chart for fig_2
    fig_2.update_layout(
        title='For-Hire vs. Not For-Hire Airport Trips',
        showlegend=False,  # Hide legend to create a donut chart
        width=fig_width,
        height=fig_height
    )

    # Display the fig_2 donut chart in your Streamlit app
    col2.plotly_chart(fig_2)

   # Create a radio button for selecting For-Hire or Not For-Hire vehicles
    selected_vehicle_type = col3.radio("Select Vehicle Type:", ["For-Hire", "Not For-Hire"], horizontal=True)

    # Create a radio button for selecting the year
    selected_year = col3.radio("Select Year:", [2022, 2023], horizontal=True)

    # SQL query to join trips_data with taxi_location_name and count trips to airport destinations
    top_pickup_query = f"""
        SELECT tz.location_name, COUNT(*) AS trip_count
        FROM trips_data AS td
        JOIN locations AS tz
        ON td.pulocationid = tz.location_id
        WHERE dolocationid IN (1, 132, 138)
        AND td.service_type_id = {'1' if selected_vehicle_type == 'For-Hire' else '0'}
        AND td.year = {selected_year}
    """

    # Combine conditions with the base query
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
        title='Top 10 Pick-up Locations with Most Trips to Airport Destinations',
        xaxis_title='Location (location_name)',
        yaxis_title='Number of Trips',
        width=fig_width,
        height=fig_height
    )

    col3.plotly_chart(fig_3)

    # Create a radio button for selecting For-Hire or Not For-Hire vehicles
    selected_vehicle_type_fig_4 = col2.radio("Select Vehicle Type:", ["For-Hire", "Not For-Hire"], key="vehicle_type_fig_4", horizontal=True)

    # Create a radio button for selecting the year (fig_4)
    selected_year_fig4 = col2.radio("Select Year:", [2022, 2023], key="year_fig_4", horizontal=True)

    # SQL query to count trips for each day of the week and order by the desired order
    day_of_week_query = f"""
        SELECT
            EXTRACT(DAY_OF_WEEK FROM DATE(CAST(year AS VARCHAR) || '-' || CAST(month AS VARCHAR) || '-' || CAST(day AS VARCHAR))) AS day_of_week,
            COUNT(*) AS trip_count
        FROM
            trips_data
        WHERE
            year = {selected_year_fig4}
            AND (pulocationid IN (1, 132, 138) OR dolocationid IN (1, 132, 138))
            AND (CASE WHEN '{selected_vehicle_type_fig_4}' = 'For-Hire' THEN service_type_id = 1
                WHEN '{selected_vehicle_type_fig_4}' = 'Not For-Hire' THEN service_type_id = 0 END)
    """

    # Define a mapping between numerical values and day names
    day_name_mapping = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday'
    }

    # Use a CASE statement to assign numerical values to days of the week
    day_of_week_query += """
        GROUP BY
            EXTRACT(DAY_OF_WEEK FROM DATE(CAST(year AS VARCHAR) || '-' || CAST(month AS VARCHAR) || '-' || CAST(day AS VARCHAR)))
        ORDER BY
            CASE
            WHEN day_of_week = 2 THEN 1
            WHEN day_of_week = 3 THEN 2
            WHEN day_of_week = 4 THEN 3
            WHEN day_of_week = 5 THEN 4
            WHEN day_of_week = 6 THEN 5
            WHEN day_of_week = 7 THEN 6
            WHEN day_of_week = 1 THEN 7
            END
    """

    # Execute the SQL query and fetch the result
    cursor.execute(day_of_week_query)
    day_of_week_data = cursor.fetchall()

    # Create a DataFrame from the SQL query result
    df_day_of_week = pd.DataFrame(day_of_week_data, columns=['day_of_week', 'trip_count'])

    # Map numerical values to day names in the DataFrame
    df_day_of_week['day_of_week'] = df_day_of_week['day_of_week'].map(day_name_mapping)

    # Create a Plotly Go bar chart (named fig_5)
    fig_4 = go.Figure(go.Bar(
        x=df_day_of_week['day_of_week'],
        y=df_day_of_week['trip_count'],
        text=df_day_of_week['trip_count'],
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