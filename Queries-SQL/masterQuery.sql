drop database if exists NYC_TAXIS;
create database if not exists NYC_TAXIS;
USE NYC_TAXIS;

# Tipe service
drop table if exists type_service;
CREATE TABLE if not exists type_service(
	Type_ServiceID INT  PRIMARY KEY,
    Service VARCHAR(20)
    );
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\type_services.csv'
INTO TABLE type_service  
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

# Data report monthly 
drop table if exists data_report_monthly;
CREATE TABLE if not exists data_report_monthly(
	ID INT PRIMARY KEY,
    License_Class INT,
    Year INT,
    Month int,
    Total_Trips INT,
    Total_Shared_Trips INT,
    Unique_Vehicles VARCHAR(50),
    FOREIGN KEY(License_Class) REFERENCES type_service(Type_ServiceID));

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_data_report_monthly.csv'
INTO TABLE data_report_monthly  
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

# Taxi zone
drop table if exists taxi_zone;
CREATE TABLE if not exists taxi_zone(
    OBJECTID INT PRIMARY KEY,
	LocationID INT,
    Borough VARCHAR(30),
    Zone VARCHAR(150));

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_taxi_zone.csv'
INTO TABLE taxi_zone  
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

# Vehicle Fuel economy
drop table if exists vehicle_fuel_economy;
CREATE TABLE if not exists vehicle_fuel_economy(
    ID INT PRIMARY KEY,
    Model VARCHAR(50),
    Co2 FLOAT(6,2));

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_Vehicle Fuel Economy Data.csv'
INTO TABLE vehicle_fuel_economy  
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

# Trips data
drop table if exists trips_data;
CREATE TABLE if not exists trips_data(
	
    PULocationID INT,
    DOLocationID INT,
    trip_distance FLOAT,
    total_amount DECIMAL,
    passenger_count INT,
    year INT,
    month INT,
    day INT,
    PU_time VARCHAR(6),
    DO_time VARCHAR(6),
    trip_time INT,
    type_service INT,
    FOREIGN KEY(PULocationID) REFERENCES taxi_zone(OBJECTID),
    FOREIGN KEY(DOLocationID) REFERENCES taxi_zone(OBJECTID),
    FOREIGN KEY(Type_Service) REFERENCES type_service(Type_ServiceID)
    );
    

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_fhvhv_2022-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 
LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_fhvhv_2023-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_green_2022-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_green_2023-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_yellow_2022-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_yellow_2023-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;


ALTER TABLE trips_data ADD COLUMN TripID INT AUTO_INCREMENT PRIMARY KEY;
SET @id := 0;
UPDATE trips_data SET TripID = (@id := @id + 1);

#Electric_Car_Data
DROP TABLE IF EXISTS electric_car_data;
CREATE TABLE IF NOT EXISTS electric_car_data (
	Brand VARCHAR(255),
    Model VARCHAR(255),
    PriceUSD DECIMAL(10, 2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_electric_car_data.csv' 
INTO TABLE electric_car_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

# Light_Duty_Vehicles
DROP TABLE IF EXISTS light_duty_vehicles;
CREATE TABLE IF NOT EXISTS light_duty_vehicles (
    Model VARCHAR(255),
    ModelYear INT,
    Manufacturer VARCHAR(255),
    Fuel VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_light_duty_vehicles.csv' 
INTO TABLE light_duty_vehicles
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


