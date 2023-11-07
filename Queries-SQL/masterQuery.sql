drop database if exists NYC_TAXIS;
create database if not exists NYC_TAXIS;
USE NYC_TAXIS;

# Service types
drop table if exists service_types;
CREATE TABLE if not exists service_types(
	Service_type_id INT  PRIMARY KEY,
    Service_name VARCHAR(20)
    );
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\service_types.csv'
INTO TABLE service_types  
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

# locations
drop table if exists locations;
CREATE TABLE if not exists locations(
    Location_id INT PRIMARY KEY,
    Location_name VARCHAR(150),
    Borough VARCHAR(30)
	);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_taxi_zone.csv'
INTO TABLE locations
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

# fuel_vehicles
drop table if exists fuel_vehicles;
CREATE TABLE if not exists fuel_vehicles(
    Vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    Year INT,
    Brand VARCHAR(50),
    Model VARCHAR(50),
    co2_emission_gpm FLOAT(6,2));

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_Vehicle Fuel Economy Data.csv'
INTO TABLE fuel_vehicles
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
    Year INT,
    Brand VARCHAR(255),
    Fuel VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_light_duty_vehicles.csv' 
INTO TABLE light_duty_vehicles
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


