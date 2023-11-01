DROP DATABASE IF EXISTS NYC_TAXIS;
CREATE DATABASE IF NOT EXISTS NYC_TAXIS;
USE NYC_TAXIS;

DROP TABLE IF EXISTS light_duty_vehicles;
CREATE TABLE IF NOT EXISTS light_duty_vehicles (
    Model VARCHAR(255),
    ModelYear INT,
    Manufacturer VARCHAR(255),
    Fuel VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\filtered_light_duty_vehicles.csv' 
INTO TABLE light_duty_vehicles
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

SELECT * FROM light_duty_vehicles;