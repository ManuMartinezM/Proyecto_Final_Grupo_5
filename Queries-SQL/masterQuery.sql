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

# Data report monthly 
drop table if exists monthly_reports;
CREATE TABLE if not exists monthly_reports(
	Report_id INT PRIMARY KEY,
    Service_type_id INT,
    Year INT,
    Month int,
    Trips_per_day INT,
    Shared_trips_per_day INT,
    Unique_vehicles VARCHAR(50),
    FOREIGN KEY(Service_type_id) REFERENCES service_types(Service_type_id));

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_data_report_monthly.csv'
INTO TABLE monthly_reports 
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;


# Trips data
drop table if exists trips_data;
CREATE TABLE if not exists trips_data(
	
    PU_location_id INT,
    DO_location_id INT,
    Trip_distance FLOAT,
    Total_amount DECIMAL,
    Year INT,
    Month INT,
    Day INT,
    PU_time VARCHAR(6),
    DO_time VARCHAR(6),
    Trip_time INT,
    Service_type_id INT,
    FOREIGN KEY(PU_location_id) REFERENCES locations(Location_id),
    FOREIGN KEY(DO_location_id) REFERENCES locations(Location_id),
    FOREIGN KEY(Service_type_id) REFERENCES service_types(Service_type_id)
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

DROP TABLE IF EXISTS Annual_vehicle_emissions;
CREATE TABLE IF NOT EXISTS Annual_vehicle_emissions (
    Vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    Year INT,
    Brand VARCHAR(255),
    Model VARCHAR(255),
    Fuel VARCHAR(255),
    Fuel_use INT,
    Electricity_use INT,
    Fuel_elec_cost INT,
    Operating_cost INT ,
    Cost_per_mile DECIMAL(10, 2),
    Annual_emissions_lbs_co2 DECIMAL(10,2 )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_vehicle_annual_emissions.csv.csv' 
INTO TABLE Annual_vehicle_emissions
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;
