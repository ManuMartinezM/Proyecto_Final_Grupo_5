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

    data_query = """
        SELECT 
            Year,
            Brand,
            Model,
            Fuel,
            vehicle_price
        FROM annual_vehicle_emissions
        WHERE Year = {} AND ('{}' = 'All' OR Fuel = '{}')
        ORDER BY vehicle_price
        LIMIT 10;
    """

    # Create a sidebar filter to select the year
    selected_year = st.sidebar.selectbox("Select a year", [2022, 2023])

    # Create a sidebar filter to select the fuel type
    selected_fuel = st.sidebar.selectbox("Select a fuel type", ['All', 'EV', 'Hybrid'])

    # Modify the SQL query based on the selected filters
    if selected_fuel == 'All':
        fuel_filter = "'EV', 'Hybrid'"
    else:
        fuel_filter = selected_fuel
    
    # Execute the SQL query with the selected year and fuel type
    data_results = conn.cursor().execute(data_query.format(selected_year, fuel_filter)).fetchall()

    # Create a DataFrame from the query results
    data_df = pd.DataFrame(data_results, columns=['Year', 'Brand', 'Model', 'Fuel', 'Price'])

    # Create a bar chart using Plotly Go
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_df['Model'],
        y=data_df['Price'],
        marker_color='blue',
        name=f'Top 10 Lowest Priced Electric and Hybrid Vehicles in {selected_year}'
    ))
    fig.update_layout(
        title=f'Top 10 Lowest Priced Electric and Hybrid Vehicles in {selected_year}',
        xaxis_title='Model',
        yaxis_title='Price',
        width=700,
        height=500
    )

    # Display the bar chart
    st.plotly_chart(fig)


