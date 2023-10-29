# FINAL DATA SCIENCE PROJECT - HENRY
## GROUP 5

![Cover](Images/NYC_Taxis.jpg)

### Description

Welcome to the data-driven analysis of a prospective business venture in the bustling city of New York. In this project, we take on the role of data scientists, partnering with a well-established transportation company that specializes in long-distance passenger travel, primarily using large-volume vehicles like buses. The company has set its sights on expanding its services by venturing into short-distance passenger travel within New York City. Their vision is to introduce a green and environmentally friendly mode of transportation, utilizing electric or hybrid vehicles, particularly for shared rides serving the city's three major airports.

The primary objective of our analysis is to evaluate the viability and convenience of this proposed investment. We will rely on a robust dataset that includes information from the New York Taxi Service, among other relevant data sources. By employing data-driven insights and key performance indicators (KPIs), we aim to provide our client with a clear understanding of the potential success of this new venture.

Key questions we seek to answer include:

- Can we ensure that each vehicle achieves a goal of 10 trips, considering factors such as speed, autonomy, charging time (in the case of electric cars), and waiting periods?
- Will there be a 5% increase in demand for shared airport transfers, as indicated by a comparison of NYC taxi data from July 2023 and July 2022?
- What is the expected reduction in carbon emissions compared to traditional combustion-fueled taxi services when using environmentally friendly vehicles?
- How do the economic costs of electric and hybrid vehicles compare, taking into account variables like sale price, fuel costs, autonomy, and durability?

This project kicks off with a comprehensive exploratory data analysis, aiming to uncover valuable insights from the available datasets. Additionally, we will create informative visualizations to aid in understanding and interpretation.

As we progress through our analysis, we will diligently record and share our findings, insights, and conclusions on our [GitHub repository](https://github.com/ManuMartinezM/Proyecto_Final_Grupo_5). Our ultimate goal is to provide the transportation company with a data-driven foundation to make informed decisions regarding their potential investment in short-distance passenger travel within the city of New York.

# KPIs

## KPI 1: 5% increase in demand for the type of service contracted

### Description:
Evaluate the 5% increase in demand for contracted service-type trips compared to non-contracted services between 2022 and 2023.

### Associated Metrics:
- Annual count of trips categorized by service type.
- Total monthly trip count.
- Average trip distance by service type.

### Goal:
Provide the rationale for the decision to operate as a contracted transportation service company.

## KPI 2: 5% increase in demand for shared rides

### Description:
Evaluate the 5% increase in shared trips demand between 2022 and 2023. This comparison is made by examining the number of shared trips as a percentage of total trips for each year.

### Associated Metrics:
- Distribution of shared trips by service.
- Number of passengers per trip.
- Count of trips categorized by service.

### Goal:
The choice of the taxi service type is crucial to ensure efficiency and the fulfillment of our objectives.

## KPI 3: 5% increase in demand for airport taxi rides

### Description:
Achieve a 5% increase in airport-to-airport taxi demand by comparing the trips taken in the month of June in 2023 and 2022.

### Associated Metrics:
- Variation in the number of individuals traveling to and from the airport.
- Percentage of airport trips in relation to the total number of trips.
- Common departure and arrival locations.
- Common departure and arrival times.
- Distribution of trip frequencies by day of the week.
- Number of airport trips categorized by borough.

### Goal:
Assess the feasibility of implementing an airport-exclusive transportation service.

## KPI 4: 10% increase in the average utility for vehicles

### Description:
Evaluate the 10% increase in the average utility (lifespan / cost in dollars) of the Top 10 electric vehicles compared to the Top 10 hybrid vehicles between 2022 and 2023.

### Associated Metrics:
- Travel time (average duration).
- Charging time.
- Range for each type of vehicle.
- Purchase cost.
- Fuel cost.

### Goal:
Support the decision to acquire electric vehicles despite their higher average initial cost.

## KPI 5: 5% reduction in carbon emissions

### Description:
Achieve a 5% reduction in carbon emissions by comparing the Top 10 electric cars to the Top 10 hybrid cars when transporting the same number of passengers over a 25-mile distance.

### Associated Metrics:
- Average emissions per trip by car type.
- Number of trips taken by electric and hybrid cars in both non-shared and shared modes to transport the same number of passengers.
- Noise pollution due to traffic.

### Goal:
Emissions reduction for transportation is as crucial as economic profitability.

# Datasets (EDA)

## Technical information about the various available vehicle models:

### Alternative Fuel Vehicles US.csv
- Available car models that use alternative fuels and their technical data.
- (882 rows and 22 columns).

### Vehicle Fuel Economy Data.csv
- Car models, with manufacturing information, technical specifications, and carbon emissions per mile.
- (46,186 rows and 82 columns).

### ElectricCarData_Clean.csv
- Electric car models, with technical specifications and their prices.
- (103 rows and 14 columns).

### ElectricCarData_Norm.csv
- Same information as ElectricCarData_Clean.csv without numeric values cleaned.

### Light Duty Vehicles.csv
- Light vehicle models and technical specifications.
- (3,008 rows and 29 columns).

### Electric and Alternative Fuel Charging Stations.csv
- Fuel charging stations across the United States with information on the provided services.
- (70,406 rows and 65 columns).

## NYC Taxi Zones

### taxi+_zone_lookup.csv
- Zones in each district and their assigned taxi service.
- (265 rows and 4 columns).

### taxi_zones.dbf
- Zones in each district, geolocation coordinates, and IDs.
- (263 rows and 6 columns).

### Information about taxi trips in NYC

Downloaded from the NYC Taxi and Limousine Commission website. All datasets contain information about trips taken in NYC, including the starting and ending location, date and time, distance traveled, fares, and taxes, for the months of June in the years 2022 and 2023.

### yellow_tripdata_2023-06.parquet
-Information on trips in yellow taxis covering the entire city.

### yellow_tripdata_2022-06.parquet
- Information on trips in yellow taxis covering the entire city.

### green_tripdata_2023-06.parquet
- Information on trips in green taxis covering all districts except Manhattan.

### green_tripdata_2022-06.parquet
- Information on trips in green taxis covering all districts except Manhattan.

### fhvhv_tripdata_2023-06.parquet
- Information on for-hire vehicle (FHV) trips (Uber, Lyft, Via, etc.).

### fhvhv_tripdata_2022-06.parquet
- Information on for-hire vehicle (FHV) trips (Uber, Lyft, Via, etc.).

### fhv_tripdata_2023-06.parquet
- Information on contracted trips with high volume of rides.

### fhv_tripdata_2022-06.parquet
- Information on contracted trips with high volume of rides.

### data_reports_monthly.csv
- Monthly report spanning from 2010 to 2023, including trip counts, costs, and shared trips.

# Machine Learning Model

Build a travel classifier based on their environmental impact (high, medium, or low) to establish a differential fare system to encourage the use of environmentally low-impact modes of transportation.

# Tech Stack


## EDA

### Python 3.8 ![Python Logo](Images/Python_Icon.png)
Libraries:
- Pandas
- Matplotlib
- Seaborn
- NumPy
- Plotly
- DateTime

## Data Warehouse

### Amazon S3 ![Amazon S3 Logo](Images/Amazon_S3_Icon.png)

## Database

### Amazon Aurora MySQL ![Amazon S3 Logo](Images/Amazon_S3_Icon.png)

## Dashboard

### Streamlit ![Streamlit Logo](Images/Streamlit_Icon.png)
