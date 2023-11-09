import streamlit as st
import pymysql
import pyathena
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def display_KPI_4_page():

    st.header("KPI: 10% increase in average utility for vehicles")
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

    kpi_data = pd.read_sql_query("""
    SELECT
        Year,
        Brand,
        Model,
        Fuel,
        vehicle_price,
        Cost_per_mile
    FROM
        annual_vehicle_emissions
    WHERE
        Year = 2023
        AND (Fuel = 'EV' OR Fuel LIKE '%Hybrid%')
    ORDER BY
        vehicle_price ASC, Cost_per_mile ASC
    LIMIT 10
    """, conn)

    # Extract the top 10 electric and hybrid vehicles
    top_10_electric = kpi_data[kpi_data['Fuel'] == 'EV']
    top_10_hybrid = kpi_data[kpi_data['Fuel'].str.contains('Hybrid')]

    # Calculate the average utility rate for the top 10 electric and hybrid vehicles
    avg_utility_electric = (top_10_electric['vehicle_price'] / top_10_electric['Cost_per_mile']).mean()
    avg_utility_hybrid = (top_10_hybrid['vehicle_price'] / top_10_hybrid['Cost_per_mile']).mean()

    # Determine if the KPI goal is met
    kpi_goal_met = avg_utility_electric >= 1.1 * avg_utility_hybrid

    # Define KPI objective
    kpi_objective = 10  # Set the desired KPI objective percentage

    # Display the KPI banner with the percentage
    if kpi_goal_met:
        percentage_improvement = ((avg_utility_electric / avg_utility_hybrid) - 1) * 100
    else:
        percentage_improvement = ((avg_utility_hybrid / avg_utility_electric) - 1) * 100

    # Display the KPI banner
    kpi_style = f"""
        padding: 10px;
        font-size: 20px;
        border-radius: 10px;
        color: white;
        display: flex;
        justify-content: space-between;
        background-color: {"#4CAF50" if percentage_improvement >= kpi_objective else "#FF5733"};
    """
    st.markdown(f'<div style="{kpi_style}">Goal: {kpi_objective}%<div>{"KPI goal met!" if percentage_improvement >= kpi_objective else "KPI not met"}</div></div>', unsafe_allow_html=True)

    # Display the KPI banner in the same format as demand_increase
    if percentage_improvement >= kpi_objective:
        st.success(f'The top 10 electric vehicles have a {percentage_improvement:.2f}% better utility rate than the top 10 hybrid vehicles.')
    elif percentage_improvement >= 0:
        st.error(f'The top 10 electric vehicles do not have a {percentage_improvement:.2f}% better utility rate than the top 10 hybrid vehicles.')
    else:
        st.error(f'The top 10 electric vehicles have a {abs(percentage_improvement):.2f}% worse utility rate than the top 10 hybrid vehicles.')

        # Create a custom color palette
    color_palette = {'Gasoline': '#FFA07A', 'EV': '#90EE90', 'Hybrid': '#ADD8E6'}

    # Define a consistent figure size
    fig_width = 350
    fig_height = 450

    # Create columns to display figures and titles side by side
    col1, col2, col3 = st.columns(3)

    query_1 = f'''
        SELECT * 
        FROM annual_vehicle_emissions
        WHERE year IN (2022, 2023)
        ORDER BY vehicle_price ASC
    '''

    # Execute the SQL query and load data into a DataFrame
    df = pd.read_sql_query(query_1, conn)   

    # Color palette
    color_palette = {'Gasoline': '#FFA07A', 'EV': '#90EE90', 'Hybrid': '#ADD8E6'}

    # Streamlit radio filter for fuel type selection
    selected_fuel_type = col3.radio("Select Fuel Type", df['fuel'].unique(), index=2, horizontal=True)

    # Create a radio button for the user to choose the year, with "Both" selected by default
    selected_year_radio = col3.radio("Select Year", ["2022", "2023"], index=1, horizontal=True)

    # Filter data based on selected fuel type and year
    filtered_data = df[(df['fuel'] == selected_fuel_type) & (df['year'] == int(selected_year_radio))].nlargest(10, 'vehicle_price')

    # Create Plotly figure
    fig_1 = go.Figure()

    # Add bar trace for the selected fuel type and year
    fig_1.add_trace(
        go.Bar(
            x=filtered_data['model'],
            y=filtered_data['vehicle_price'],
            marker_color=color_palette[selected_fuel_type],
            name=selected_fuel_type
        )
    )

    # Update layout for better visibility
    fig_1.update_layout(
        title=f'Top 10 Vehicles - {selected_fuel_type} Fuel Type - Year {selected_year_radio}',
        xaxis_title='Vehicle Model',
        yaxis_title='Price',
        barmode='group',
        width=fig_width,
        height=fig_height
    )

    col3.plotly_chart(fig_1)

    # Sample SQL query for utility calculation
    query_utility = """
        SELECT
            Fuel,
            AVG(vehicle_price / Cost_per_mile) AS Utility
        FROM
            annual_vehicle_emissions
        WHERE
            Year = 2023
            AND (Fuel = 'EV' OR Fuel LIKE '%Hybrid%')
        GROUP BY
            Fuel
    """

    # Execute the SQL query and load data into a DataFrame
    df_utility = pd.read_sql_query(query_utility, conn)

    # Color palette
    color_palette = {'Gasoline': '#FFA07A', 'EV': '#90EE90', 'Hybrid': '#ADD8E6'}

    # Create Plotly pie chart
    fig_2 = go.Figure()

    fig_2.add_trace(
        go.Pie(
            labels=df_utility['Fuel'],
            values=df_utility['Utility'],
            marker=dict(colors=[color_palette[fuel] for fuel in df_utility['Fuel']]),
            hole=0.3,
            textinfo='label+percent',
            hoverinfo='label+percent'
        )
    )

    # Update layout for better visibility
    fig_2.update_layout(
        title='Fuel Type Utility Comparison',
        width=fig_width,
        height=fig_height
    )

    # Display the pie chart
    col2.plotly_chart(fig_2)

    # Sample SQL query for average cost_per_mile calculation
    query_cost_per_mile = """
        SELECT
            Fuel,
            AVG(ROUND(Cost_per_mile, 2)) AS Avg_Cost_per_Mile
        FROM
            annual_vehicle_emissions
        WHERE
            Year = 2023
            AND (Fuel = 'EV' OR Fuel LIKE '%Hybrid%' OR Fuel = 'Gasoline')
        GROUP BY
            Fuel
    """

    # Execute the SQL query and load data into a DataFrame
    df_cost_per_mile = pd.read_sql_query(query_cost_per_mile, conn)

    # Color palette
    color_palette = {'Gasoline': '#FFA07A', 'EV': '#90EE90', 'Hybrid': '#ADD8E6'}

    # Create Plotly bar chart
    fig_3 = go.Figure()

    fig_3.add_trace(
        go.Bar(
            x=df_cost_per_mile['Fuel'],
            y=df_cost_per_mile[('Avg_Cost_per_Mile')],
            marker_color=[color_palette[fuel] for fuel in df_cost_per_mile['Fuel']],
            text=df_cost_per_mile['Avg_Cost_per_Mile'],
            textposition='auto'
        )
    )

    # Update layout for better visibility
    fig_3.update_layout(
        title='Average Cost per Mile Comparison',
        xaxis_title='Fuel Type',
        yaxis_title='Average Cost per Mile',
        width=fig_width,
        height=fig_height
    )

    # Display the bar chart
    col1.plotly_chart(fig_3)