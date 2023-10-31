drop database if exists NYC_TAXIS;
create database if not exists NYC_TAXIS;
USE NYC_TAXIS;

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

SELECT * FROM taxi_zone;