import streamlit as st
import pymysql
import pyathena
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def display_KPI_5_page():

    st.header("KPI: 5% reduction in carbon emissions")
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

    # Write SQL query to calculate average emissions for EVs and hybrids
    kpi_query = """
    SELECT
        Fuel,
        AVG(Annual_emissions_lbs_co2) AS avg_emissions
    FROM
        annual_vehicle_emissions
    WHERE
        Fuel = 'EV' OR Fuel = 'Hybrid'
    GROUP BY
        Fuel;
    """

    # Execute the SQL query and retrieve the results
    with conn.cursor() as cursor:
        cursor.execute(kpi_query)
        results = cursor.fetchall()

    # Create a dictionary to store the average emissions
    average_emissions = {}

    # Extract average emissions for EV and Hybrid from the query results
    for row in results:
        fuel_type, avg_emissions = row
        average_emissions[fuel_type] = avg_emissions

    # Calculate the potential reduction in emissions
    average_emissions_ev = average_emissions.get('EV', 0)
    average_emissions_hybrid = average_emissions.get('Hybrid', 0)
    emission_reduction = ((average_emissions_hybrid - average_emissions_ev) / average_emissions_hybrid) * 100

    # Define the KPI objective
    kpi_objective = 5

    # Determine whether the KPI goal is met
    kpi_met = emission_reduction >= kpi_objective

    # Create a Streamlit banner to display the KPI status
    kpi_style = f"""
        padding: 10px;
        font-size: 20px;
        border-radius: 10px;
        color: white;
        display: flex;
        justify-content: space-between;
        background-color: {"#4CAF50" if kpi_met else "#FF5733"};
    """
    st.markdown(f'<div style="{kpi_style}">Goal: {kpi_objective}% Reduction<div>{"KPI goal met!" if kpi_met else "KPI not met"}</div></div>', unsafe_allow_html=True)

    # Display the KPI banner
    if kpi_met:
        st.success(f'Potential reduction in emissions: {emission_reduction:.2f}%')
    else:
        st.error(f'Potential reduction in emissions: {emission_reduction:.2f}%')

    # Write SQL query to retrieve emissions data for EVs, hybrids, and gasoline vehicles
    query_1 = """
    SELECT
        CAST(Year as VARCHAR) as Year,
        Fuel,
        AVG(Annual_emissions_lbs_co2) AS total_emissions
    FROM
        annual_vehicle_emissions
    WHERE
        Fuel IN ('EV', 'Hybrid', 'Gasoline')
    GROUP BY
        Year, Fuel;
    """

    # Execute the SQL query and retrieve the results as a DataFrame
    with conn.cursor() as cursor:
        cursor.execute(query_1)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)

    # Create a custom color palette
    color_palette = {'Gasoline': '#FFA07A', 'EV': '#90EE90', 'Hybrid': '#ADD8E6'}

    # Define a consistent figure size
    fig_width = 350
    fig_height = 450

    # Create columns to display figures and titles side by side
    col1, col2, col3 = st.columns(3)

        # Create a stacked bar chart using Plotly
    fig_1 = go.Figure()

    for fuel_type in df['Fuel'].unique():
        filtered_fuel_df = df[df['Fuel'] == fuel_type]
        fig_1.add_trace(go.Bar(x=filtered_fuel_df['Year'], y=filtered_fuel_df['total_emissions'], name=fuel_type, marker_color=color_palette.get(fuel_type, 'gray')))

    fig_1.update_layout(title_text='Annual Carbon Emissions', width=fig_width, height=fig_height)
    fig_1.update_xaxes(title_text='Year')
    fig_1.update_yaxes(title_text='Total Emissions (lbs CO2)')

    # Display the chart in the Streamlit app
    col1.plotly_chart(fig_1)


    # Write SQL query to retrieve average annual emissions for each type of fuel
    query_2 = """
    SELECT
        Fuel,
        AVG(Annual_emissions_lbs_co2) AS avg_emissions
    FROM
        annual_vehicle_emissions
    WHERE
        CAST(Year AS varchar) IN ('2022', '2023')
    GROUP BY
        Fuel;
    """

    # Execute the SQL query and retrieve the results as a DataFrame
    with conn.cursor() as cursor:
        cursor.execute(query_2)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df_avg_emissions = pd.DataFrame(results, columns=columns)


    # Create a pie chart using Plotly Go to show the distribution of average annual carbon emissions for each fuel type
    fig_2 = go.Figure(data=[go.Pie(labels=df_avg_emissions['Fuel'], values=df_avg_emissions['avg_emissions'], marker_colors=[color_palette.get(fuel_type, 'gray') for fuel_type in df_avg_emissions['Fuel']])])
    fig_2.update_layout(title_text='Distribution of Average Annual Carbon Emissions by Fuel Type', width=fig_width, height=fig_height)

    # Display the pie chart in the Streamlit app
    col2.plotly_chart(fig_2)

   # Create a radio button for the user to choose between "EV," "Hybrid," "Gasoline," with "EV" selected by default
    selected_fuel_type = col3.radio("Select Fuel Type", ["EV", "Hybrid", "Gasoline"], index=0, horizontal=True)

    # Create a radio button for the user to choose the year, with "Both" selected by default
    selected_year_radio = col3.radio("Select Year", ["2022", "2023"], index=1, horizontal=True)

    # Write SQL query to retrieve emissions data for the top 5 vehicle models with the least emissions based on the selected fuel type
    # Update the SQL query to use the selected year from the radio button

    query_3 = f"""
        SELECT
            Model,
            Annual_emissions_lbs_co2
        FROM
            annual_vehicle_emissions
        WHERE
            Fuel = '{selected_fuel_type}' AND CAST(Year AS varchar) IN ('{selected_year_radio}', 'Both')
        ORDER BY
            Annual_emissions_lbs_co2
        LIMIT 5;
    """

    # Execute the SQL query and retrieve the results as a DataFrame
    with conn.cursor() as cursor:
        cursor.execute(query_3)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df_top_models = pd.DataFrame(results, columns=columns)

    # Create a bar chart using Plotly Go for the top 5 vehicle models with the least emissions
    fig_3 = go.Figure()

    fig_3.add_trace(go.Bar(
        x=df_top_models['Model'],
        y=df_top_models['Annual_emissions_lbs_co2'],
        text=df_top_models['Annual_emissions_lbs_co2'],
        textposition='auto',
        marker=dict(color=color_palette.get(selected_fuel_type, 'gray'))  # Use the color of the selected fuel type
    ))

    # Customize the layout of the bar chart
    fig_3.update_layout(
        title=f'Top 5 {selected_fuel_type} Models with Least Annual Emissions (CO2)',
        xaxis=dict(title='Model'),
        yaxis=dict(title='Annual Emissions (lbs CO2)'),
        width=fig_width,
        height=fig_height
    )

    # Display the radio button and the bar chart in the Streamlit app
    col3.plotly_chart(fig_3)





