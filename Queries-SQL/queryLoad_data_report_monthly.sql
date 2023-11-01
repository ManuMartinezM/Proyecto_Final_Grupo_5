drop database if exists NYC_TAXIS;
create database if not exists NYC_TAXIS;
USE NYC_TAXIS;

drop table if exists data_report_monthly;
CREATE TABLE if not exists data_report_monthly(
	ID INT PRIMARY KEY,
    License_Class VARCHAR(50),
    Year INT,
    Month int,
    Total_Trips INT,
    Total_Shared_Trips INT,
    Unique_Vehicles VARCHAR(50));

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\KPI_2_ShareTrips.csv'
INTO TABLE data_report_monthly  
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT * FROM data_report_monthly;