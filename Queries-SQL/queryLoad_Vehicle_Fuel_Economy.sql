USE NYC_TAXIS;

drop table if exists vehicle_fuel_economy;
CREATE TABLE if not exists vehicle_fuel_economy(
    ID INT PRIMARY KEY,
    Model VARCHAR(50),
    Co2 FLOAT(6,2));

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\PF\\clean_Vehicle Fuel Economy Data.csv'
INTO TABLE vehicle_fuel_economy  
FIELDS TERMINATED BY ';' ENCLOSED BY '' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

SELECT * FROM vehicle_fuel_economy;
