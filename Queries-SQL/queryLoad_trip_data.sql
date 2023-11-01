drop database if exists NYC_TAXIS;
create database if not exists NYC_TAXIS;
USE NYC_TAXIS;

drop table if exists trips_data;
CREATE TABLE if not exists trips_data(
	TripID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
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
    FOREIGN KEY(PULocationID) REFERENCES taxi_zone(LocationID),
    FOREIGN KEY(DOLocationID) REFERENCES taxi_zone(LocationID),
    FOREIGN KEY(Type_Service) REFERENCES type_service(Type_ServiceID)
    );
    
drop table if exists type_service;
CREATE TABLE if not exists type_service(
	Type_ServiceID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Service VARCHAR(20)
    );

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_fhvhv_2022-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_fhvhv_2023-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_green_2022-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_green_2023-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_yellow_2022-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_yellow_2023-06.csv'
INTO TABLE trips_data
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\type_services.csv'
INTO TABLE type_service  
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT * FROM data_trips;