drop database if exists NYC_TAXIS;
create database if not exists NYC_TAXIS;
USE NYC_TAXIS;

# Service types
drop table if exists service_types;
CREATE TABLE if not exists service_types(
	Service_type_id INT  PRIMARY KEY,
    Service_name VARCHAR(20)
    );

# locations
drop table if exists locations;
CREATE TABLE if not exists locations(
    Location_id INT PRIMARY KEY,
    Location_name VARCHAR(150),
    Borough VARCHAR(30)
	);
    
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
    
    
DROP TABLE IF EXISTS annual_vehicle_emissions;
CREATE TABLE IF NOT EXISTS annual_vehicle_emissions (
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
    Annual_emissions_lbs_co2 DECIMAL(10, 2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;


# Trips data
drop table if exists trips_data;
CREATE TABLE if not exists trips_data(
	Trip_id INT AUTO_INCREMENT PRIMARY KEY,
    PU_location_id INT,
    DO_location_id INT,
    Trip_distance FLOAT,
    Total_amount DECIMAL,
    Year INT,
    Month INT,
    Day INT,
    Hour INT,
    Trip_time INT,
    Service_type_id INT,
    FOREIGN KEY(PU_location_id) REFERENCES locations(Location_id),
    FOREIGN KEY(DO_location_id) REFERENCES locations(Location_id),
    FOREIGN KEY(Service_type_id) REFERENCES service_types(Service_type_id));

