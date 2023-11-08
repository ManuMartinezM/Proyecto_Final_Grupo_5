
<h1 align='center'>
 <b> DATA DICTIONARY </b>
</h1>

# ALTERNATIVE FUEL VEHICLES (US)
<b>dataset:</b> Alternative Fuel Vehicles US.csv

- Category: Category or type of the vehicle. General body style or form of the vehicle.

- Model: Model name of the vehicle.
- Model Year: Year when the vehicle model was manufactured.
- Manufacturer: Name of the company or manufacturer that produced the vehicle.
- Fuel: Type of alternative fuel the vehicle uses.
- All-Electric Range: Maximum range of the vehicle when operating in all-electric mode (in miles).
- PHEV Total Range: Total range of a Plug-In Hybrid Electric Vehicle (PHEV) in miles, which includes both electric and conventional fuel range.
- Alternative Fuel Economy City: Estimated fuel economy for the vehicle when driving in city conditions using the alternative fuel source (e.g., miles per gallon).
- Alternative Fuel Economy Highway: Estimated fuel economy for the vehicle when driving on the highway using the alternative fuel source (e.g., miles per gallon).
- Alternative Fuel Economy Combined: Estimated combined fuel economy for the vehicle, which may consider both city and highway driving (e.g., miles per gallon).
- Conventional Fuel Economy City: Estimated fuel economy for the vehicle when using conventional fuel (non-alternative fuel) in city conditions (e.g., miles per gallon).
- Conventional Fuel Economy Highway: Estimated fuel economy for the vehicle when using conventional fuel on the highway (e.g., miles per gallon).
- Conventional Fuel Economy Combined: Estimated combined fuel economy for the vehicle when using conventional fuel (e.g., miles per gallon).
- Transmission Type: Type of transmission used in the vehicle.
- Transmission Make: Manufacturer or brand of the transmission, if applicable.
- Engine Type: Type of engine used in the vehicle.
- Engine Size: Size or displacement of the engine, often expressed in liters.
- Engine Cylinder Count: Number of cylinders in the vehicle's engine.
- Number of Passengers: Maximum number of passengers the vehicle can accommodate.
- Heavy-Duty Power System: Indicates if the vehicle has a heavy-duty power system.
- Notes: Additional notes or information about the vehicle, if available.
- Drivetrain: Type of drivetrain, such as "AWD" (All-Wheel Drive) or "FWD" (Front-Wheel Drive).

# CHARGING STATIONS:
<b>dataset:</b> Electric and Alternative Fuel Charging Stations.csv

- Fuel Type Code: The code representing the type of fuel available at the station.
- Station Name: The name of the fuel station.
- Street Address: The address/location of the station.
- Intersection Directions: Directions or landmarks for finding the station, particularly at intersections.
- City: The city where the fuel station is located.
- State: The state in which the station is situated.
- ZIP: The ZIP code for the station's address.
- Plus4: Additional ZIP code digits (if applicable).
- Station Phone: Contact phone number for the station.
- Status Code: Code indicating the status of the station (e.g., operational, temporarily closed).

- Expected Date: Anticipated date for station availability or updates.

- Groups With Access Code: Code indicating which groups have access to the station.
- Access Days Time: Information about the days and times the station is accessible.
- Cards Accepted: Types of payment cards accepted at the station.
- BD Blends: Information about the types of biodiesel (BD) blends available.
- NG Fill Type Code: Code representing the natural gas fill type.
- NG PSI: Pressure specifications for natural gas fueling.
- EV Level1 EVSE Num: Number of Level 1 Electric Vehicle Supply Equipment (EVSE) available.
- EV Level2 EVSE Num: Number of Level 2 Electric Vehicle Supply Equipment (EVSE) available.
- EV DC Fast Count: Count of DC fast chargers for electric vehicles.
- EV Other Info: Additional information about electric vehicle charging.
- EV Network: The network associated with electric vehicle charging.
- EV Network Web: Website for the electric vehicle charging network.
- Geocode Status: Status of the geographical coordinates (latitude and longitude).
- Latitude: The geographic latitude of the station.
- Longitude: The geographic longitude of the station.
- Date Last Confirmed: Date of the last confirmation or update.
- ID: A unique identifier for the station.
- Updated At: Timestamp for when the station's information was last updated.
- Owner Type Code: Code representing the owner type of the station.
- Federal Agency ID: Identifier for federal agency ownership.
- Federal Agency Name: Name of the federal agency (if applicable).
- Open Date: Date when the station was opened for operation.
- Hydrogen Status Link: Link to information about the status of hydrogen availability.
- NG Vehicle Class: Classifications for natural gas vehicles.
- LPG Primary: Information about primary propane (LPG) availability.
- E85 Blender Pump: Availability of E85 ethanol blender pumps.
- EV Connector Types: Types of connectors available for electric vehicle charging.
- Country: The country where the station is located.
- Intersection Directions (French): Directions or landmarks in the French language.
- Access Days Time (French): Information about access days and times in the French language.
- BD Blends (French): Information about biodiesel blends in the French language.
- Groups With Access Code (French): Access group codes in the French language.
- Hydrogen Is Retail: Indication of whether hydrogen is available for retail purchase.
- Access Code: Code specifying access conditions for the station.
- Access Detail Code: Code providing details about station access.
- Federal Agency Code: Code representing the federal agency (if applicable).
- Facility Type: Type of facility where the station is located.
- CNG Dispenser Num: Number of compressed natural gas (CNG) dispensers.
- CNG On-Site Renewable Source: Information about on-site renewable energy sources for CNG.
- CNG Total Compression Capacity: Total compression capacity for CNG.
- CNG Storage Capacity: Capacity for storing compressed natural gas (CNG).
- LNG On-Site Renewable Source: Information about on-site renewable energy sources for LNG.
- E85 Other Ethanol Blends: Availability of other ethanol blends aside from E85.
- EV Pricing: Pricing information for electric vehicle charging.
- EV Pricing (French): Pricing information in the French language.
- LPG Nozzle Types: Types of nozzles available for LPG.
- Hydrogen Pressures: Pressure specifications for hydrogen fueling.
- Hydrogen Standards: Standards related to hydrogen fueling.
- CNG Fill Type Code: Code representing the CNG fill type.
- CNG PSI: Pressure specifications for CNG fueling.
- CNG Vehicle Class: Classifications for CNG vehicles.
- LNG Vehicle Class: Classifications for LNG vehicles.
- EV On-Site Renewable Source: Information about on-site renewable energy sources for EV charging.
- Restricted Access: Indication of access restrictions at the station


<h1></h1>

## ELECTRIC CAR DATA
<b>dataset</b>:ElectricCarData_Norm.csv - ElectricCarData_Clean.csv

- Brand: Brand or manufacturer of the electric vehicle.

- Model: Specific model of the electric vehicle.
- AccelSec: Acceleration time from 0 to 100 km/h in seconds.
- TopSpeed_KmH: Top speed of the vehicle in kilometers per hour.
- Range_Km: Estimated range of the vehicle on a single charge in kilometers.
- Efficiency_WhKm: Energy efficiency of the vehicle in watt-hours per kilometer.
- FastCharge_KmH: Speed at which the vehicle can fast-charge in kilometers per hour.
- RapidCharge: Indicates whether the vehicle supports rapid charging (Yes or No).
- PowerTrain: Type of powertrain used in the vehicle.
- PlugType: Type of plug or connector used for charging the vehicle.
- BodyStyle: Body style or configuration of the vehicle (e.g., Sedan, Hatchback).
- Segment: Vehicle segment or category it belongs to.
- Seats: Number of seats in the vehicle.
- PriceEuro: Price of the vehicle in Euros.
<h1></h1>

# LIGHT DUTY VEHICLES
<b>dataset</b>: Light Duty Vehicles.csv

- Vehicle ID: Unique identifier for each vehicle.

- Fuel ID: Unique identifier for the type of fuel.
- Fuel Configuration ID: Unique identifier for the fuel configuration.
- Manufacturer ID: Unique identifier for the manufacturer.
- Category ID: Unique identifier for the category of the vehicle.
- Model: Name of the vehicle model.
- Model Year: Year the vehicle was manufactured.
- Alternative Fuel Economy City: City fuel economy for alternative fuel vehicles.
- Alternative Fuel Economy Highway: Highway fuel economy for alternative fuel vehicles.
- Alternative Fuel Economy Combined: Combined fuel economy for alternative fuel vehicles.
- Conventional Fuel Economy City: City fuel economy for conventional fuel vehicles.
- Conventional Fuel Economy Highway: Highway fuel economy for conventional fuel vehicles.
- Conventional Fuel Economy Combined: Combined fuel economy for conventional fuel vehicles.
- Transmission Type: Type of transmission (e.g., automatic, manual).
- Engine Type: Type of engine used in the vehicle.
- Engine Size: Size of the vehicle's engine.
- Engine Cylinder Count: Number of cylinders in the engine.
- Engine Description: Description of the vehicle's engine.
- Manufacturer: Name of the vehicle manufacturer.
- Manufacturer URL: Manufacturer's website URL.
- Category: Category of the vehicle (e.g., sedan, wagon).
- Fuel Code: Code for the type of fuel.
- Fuel: Type of fuel used in the vehicle.
- Fuel Configuration Name: Name of the fuel configuration.
- Electric-Only Range: Electric-only range for hybrid or electric vehicles.
- PHEV Total Range: Total range for plug-in hybrid electric vehicles.
- PHEV Type: Type of plug-in hybrid electric vehicle.
- Notes: Any additional notes or information about the vehicle.
- Drivetrain: The type of drivetrain used in the vehicle.
<h1></h1>

#  YELLOW TAXIS Trip Records
<b>dataset:</b> yellow_tripdata_2022-06.parquet -  yellow_tripdata_2023-06.parquet

- VendorID: A code indicating the TPEP provider that provided the record.

  + 1= Creative Mobile Technologies, LLC.
  + 2= VeriFone Inc.
- tpep_pickup_datetime: The date and time when the meter was engaged.
- tpep_dropoff_datetime: The date and time when the meter was disengaged.
- Passenger_count: The number of passengers in the vehicle(This is a driver-entered value).
- Trip_distance: The elapsed trip distance in miles reported by the taximeter.
- PULocationID: TLC Taxi Zone in which the taximeter was engaged
- DOLocationID: TLC Taxi Zone in which the taximeter was disengaged
- RateCodeID: The final rate code in effect at the end of the trip.
   + 1= Standard rate
   + 2=JFK
   + 3=Newark
   + 4=Nassau or Westchester
   + 5=Negotiated fare
   + 6=Group ride
- Store_and_fwd_flag: This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka “store and forward,” because the vehicle did not have a connection to the server.
   + Y= store and forward trip
   + N= not a store and forward trip
- Payment_type: A numeric code signifying how the passenger paid for the trip.
   + 1= Credit card
   + 2= Cash
   + 3= No charge
   + 4= Dispute
   + 5= Unknown
   + 6= Voided trip
- Fare_amount: The time-and-distance fare calculated by the meter.
- Extra: Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.
- MTA_tax: $0.50 MTA tax that is automatically triggered based on the metered rate in use.
- Improvement_surcharge: $0.30 improvement surcharge assessed trips at the flag drop. The
- improvement surcharge: began being levied in 2015.
- Tip_amount: Tip amount (This field is automatically populated for credit card tips. Cash tips are not included.)
- Tolls_amount: Total amount of all tolls paid in trip.
- Total_amount: The total amount charged to passengers. Does not include cash tips.
- Congestion_Surcharge: Total amount collected in trip for NYS congestion surcharge.
- Airport_fee: $1.25 for pick up only at LaGuardia and John F. Kennedy Airports

<h1></h1>

# FHV Trip Records
<b>dataset:</b> fhv_tripdata_2022-06.parquet - fhv_tripdata_2023-06.parquet
- Dispatching_base_num: The TLC Base License Number of the base that dispatched the trip

- Pickup_datetime: The date and time of the trip pick-up.
- DropOff_datetime: The date and time of the trip dropoff.
- PULocationID: TLC Taxi Zone in which the trip began.
- DOLocationID: TLC Taxi Zone in which the trip ended.
- SR_Flag: Indicates if the trip was a part of a shared ride chain offered by a High Volume FHV company (e.g. Uber Pool, Lyft Line). For shared
trips, the value is 1. For non-shared rides, this field is null.

   + NOTE: For most High Volume FHV companies, only shared rides that
were requested AND matched to another shared-ride request over
the course of the journey are flagged. However, Lyft (base license
numbers B02510 + B02844) also flags rides for which a shared ride
was requested but another passenger was not successfully matched
to share the trip—therefore, trips records with SR_Flag=1 from those
two bases could indicate EITHER a first trip in a shared trip chain OR
a trip for which a shared ride was requested but never matched.
Users should anticipate an overcount of successfully shared trips
completed by Lyft.


<h1></h1>

# GREEN TAXIS Trips Records
<b>dataset:</b> Green_tripdata_2022-06 - Green_tripdata_2023-06

- VendorID: A code indicating the TPEP provider that provided the record.

- lpep_pickup_datetime: The date and time when the meter was engaged.
- lpep_dropoff_datetime: The date and time when the meter was disengaged.
- passenger_count: The number of passengers in the vehicle.
- trip_distance: The elapsed trip distance in miles reported by the taximeter.
- RatecodeID: The final rate code in effect at the end of the trip.
- store_and_fwd_flag: This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka “store and forward,” because the vehicle did not have a connection to the server.
- PULocationID: TLC Taxi Zone in which the taximeter was engaged
- DOLocationID: TLC Taxi Zone in which the taximeter was disengaged
- payment_type: A numeric code signifying how the passenger paid for the trip.
- fare_amount: The time-and-distance fare calculated by the meter.
- extra: Miscellaneous extras and surcharges.
- MTA_tax: $0.50 MTA tax that is automatically triggered based on the metered rate in use.
- Improvementent_surcharge: $0.30 improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015.
- Tip amount: Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.
- Tolls_amount: Total amount of all tolls paid in trip.
- Total_amount: The total amount charged to passengers. Does not include cash tips.
- Congestion_surcharge: Total amount collected in trip for NYS congestion surcharge.
- ehail_fee: Electronic hailing (E-Hail) allows a passenger to use TLC-licensed apps to hail a taxi.
- Trip_type: A code indicating whether the trip was a street-hail or a dispatch
that is automatically assigned based on the metered rate in use but
can be altered by the driver.

<h1></h1>

# FOR-HIRE VEHICULE HIGH VOLUME Trips Records
<b>dataset:</b> FHVHV_tripdata_2022-06 - FHVHV_tripdata_2023-06

The table is composed of 24 columns:

- Hvfhs_license_num: The TLC license number of the HVFHS base or business

- dispatching_base_num: The TLC Base License Number of the base that dispatched the trip
- originating_base_num: base number of the base that received the original trip request
- request_datetime: date/time when passenger requested to be picked up
- on_scene_datetime: date/time when driver arrived at the pick-up location (Accessible Vehicles-only)
- pickup_datetime: The date and time of the trip pick-up
- dropoff_datetime: The date and time of the trip drop-of
- PULocationID: TLC Taxi Zone in which the trip began
- DOLocationID: TLC Taxi Zone in which the trip ended
- trip_miles: total miles for passenger trip
- trip_time: total time in seconds for passenger trip
- base_passenger_fare: base passenger fare before tolls, tips, taxes, and fees
- tolls: total amount of all tolls paid in trip
- bcf: total amount collected in trip for Black Car Fund
- sales_tax: total amount collected in trip for NYS sales tax
- Congestion_surcharge: Total amount collected in trip for NYS congestion surcharge.
- airport_fee: $2.50 for both drop off and pick up at LaGuardia, Newark, and John
F. Kennedy airports
- tips: total amount of tips received from passenger
- driver_pay: total driver pay (not including tolls or tips and net of commission,
surcharges, or taxes)
- shared_request_flag: Did the passenger agree to a shared/pooled ride, regardless of
whether they were matched? (Y/N)
- shared_match_flag: Did the passenger share the vehicle with another passenger who
booked separately at any point during the trip? (Y/N)
- access_a_ride_flag: Was the trip administered on behalf of the Metropolitan
Transportation Authority (MTA)? (Y/N)
- wav_request_flag: Did the passenger request a wheelchair-accessible vehicle (WAV)?
(Y/N)
- wav_match_flag: Did the trip occur in a wheelchair-accessible vehicle (WAV)? (Y/N)

<h1></h1>

# REPORT MONTHLY
<b>dataset:</b> data_reports_monthly.csv

-	Month/Year: The month and year in which the data was collected.

-	License Class: The classification or category of the taxi license used.

-	Trips Per Day: The average number of trips made by a taxi on a specific day.

-	Farebox Per Day: The average revenue generated by a taxi on a specific day.

-	Unique Drivers: The number of unique drivers who operated taxis in the time period.

-	Unique Vehicles: The number of unique vehicles used as taxis in the time period.

-	Vehicles Per Day: The average number of taxi vehicles in circulation on a specific day.

-	Avg Days Vehicles on Road: The average number of days a taxi vehicle is in service.

-	Avg Hours Per Day Per Vehicle: The average number of hours a taxi vehicle is in service per day.

-	Avg Days Drivers on Road: The average number of days a taxi driver is on duty.

-	Avg Hours Per Day Per Driver: The average number of hours a taxi driver is on duty per day.

-	Avg Minutes Per Trip: The average number of minutes a taxi trip lasts.

-	Percent of Trips Paid with Credit Card: The percentage of trips paid with credit card.

-	Trips Per Day Shared: The average number of trips shared per day.
<h1></h1>

#  TAXI ZONE LOOKUP
<b>dataset:</b> taxi+_zone_lookup.csv

- LocationID: It is a unique identifier.

- Borough: Name of the district within New York City.

- Zone: Name of a zone or area within a specific borough.

- service_zone: Describe the service zone or service category associated with a location.

<h1></h1>

# TAXI ZONE
<b>dataset:</b> taxi_zones.dbf

- OBJECTID – Unique identifier or “Object ID” for each record or row in the data set.

- Shape Leng: Represents the geospatial length associated with a location.

- Shape Area: Represent the geospatial area associated with a location.

- Zone: Name of a zone or area within a specific borough.

- LocationID: It is a unique identifier.

- Borough: Name of the district within New York City.


<h1></h1>

# VEHICLE FUEL ECONOMY
<b>dataset:</b> Vehicle Fuel Economy Data.csv

-	Year: The year of manufacture of the vehicle.

-	Manufacturer: The manufacturer or brand of the vehicle.

-	Model: The specific model of the vehicle.

-	barrels08: The number of barrels of fuel consumed by the vehicle in city (city) in a year.

-	barrelsA08: The number of barrels of fuel consumed by the vehicle on the road (highway) in a year.

-	charge240: Electrical charge in the 240 volt range.

-	city08: Fuel consumption in miles per gallon (MPG) in the city.

-	city08U: Fuel consumption in miles per gallon in the city (adjusted).

-	cityA08: Fuel consumption in miles per gallon in the city (alternative).

-	cityA08U: Fuel consumption in miles per gallon in the city (alternate, adjusted).

-	cityCD: Fuel consumption in miles per gallon (MPG) in the city (diesel).

-	cityE: Fuel consumption in miles per gallon in the city (electric).

-	cityUF: Fuel consumption in miles per gallon in the city (alternative fuel).

-	co2: Carbon dioxide (CO2) emissions in grams per mile.

-	co2A: CO2 emissions in grams per mile (alternative).

-	co2TailpipeAGpm: CO2 emissions in grams per mile (tailpipe, alternative to gasoline).

-	co2TailpipeGpm: CO2 emissions in grams per mile (tailpipe, gasoline).

-	comb08: Combined fuel consumption in miles per gallon (MPG).

-	comb08U: Combined fuel consumption in miles per gallon (adjusted).

-	combA08: Combined fuel consumption in miles per gallon (alternative).

-	combA08U: Combined fuel consumption in miles per gallon (alternate, adjusted).

-	combE: Combined fuel consumption in miles per gallon (electric).

-	combinedCD: Combined fuel consumption in miles per gallon (diesel).

-	combinedUF: Combined fuel consumption in miles per gallon (alternative fuel).

-	cylinders: The number of cylinders in the vehicle's engine.

-	displ: The displacement of the engine in liters.

-	drive: The type of drive of the vehicle.

-	engId: Engine identifier.

-	eng_dscr: Engine description.

-	feScore: Fuel efficiency score.

-	fuelCost08: Estimated annual fuel cost for the vehicle.

-	fuelCostA08: Estimated annual fuel cost (alternative).

-	fuelType: Type of fuel used by the vehicle.

-	fuelType1: Type of primary fuel used by the vehicle.

-	ghgScore: Greenhouse gas emissions score.

-	ghgScoreA: Greenhouse Gas Emissions Score (alternative).

-	highway08: Fuel consumption in miles per gallon on the highway.

-	highway08U: Highway fuel consumption in miles per gallon (adjusted).

-	highwayA08: Fuel consumption in miles per gallon on the highway (alternative).

-	highwayA08U: Highway fuel consumption in miles per gallon (alternate, adjusted).

-	VClass: The class or category of the vehicle (example: sedan, SUV, truck).

-	highwayCD: Fuel consumption in miles per gallon on the highway (diesel).

-	highwayE: Fuel consumption in miles per gallon on the highway (electric).

-	highwayUF: Highway fuel consumption in miles per gallon (alternative fuel).

-	hlv: Payload of light vehicles.

-	hpv: Payload of heavy vehicles.

-	id: Unique vehicle identifier.

-	lv2: Emissions level 2.

-	lv4: Emissions level 4.

-	mpgData: Information about fuel consumption.

-	phevBlended: Plug-in hybrid vehicle indicator.

-	pv2: Greenhouse gas emissions level 2.

-	pv4: Greenhouse gas emissions level 4.

-	range: Driving range of the vehicle.

-	rangeCity: Driving range in city.

-	rangeCityA: City driving range (alternative).

-	rangeHwy: Highway driving range.

-	rangeHwyA: Highway driving range (alternate).

-	trany: The type of vehicle transmission (automatic, manual, etc.).

-	UCity: Fuel consumption in miles per gallon in the city, adjusted for specific factors.

-	UCityA: Fuel consumption in miles per gallon in the city (alternative, adjusted).

-	UHighway: Fuel consumption in miles per gallon on the highway, adjusted for specific factors.

-	UHighwayA: Highway fuel consumption in miles per gallon (alternate, adjusted).

-	youSaveSpend: Information on how much you save or spend on fuel compared to an average vehicle.

-	guzzler: Information about whether the vehicle is considered a "guzzler" (excessive fuel guzzler).

-	trans_dscr: Description of the vehicle transmission.

-	tCharger: Turbo charger indicator.

-	sCharger: Supercharger indicator.

-	atvType: Type of off-road vehicle (if applicable).

-	fuelType2: Secondary fuel type (if applicable).

-	rangeA: Alternative driving range.

-	evMotor: Information about the electric motor (if applicable).

-	mfrCode: Manufacturer code.

-	c240Dsc a: Description of the vehicle with 240 volt electrical charging.

-	charge240b: Information about 240 volt charging (alternative).

-	c240bDscr: Description of 240 volt charging (alternative).

-	createdOn: Data creation date.

-	modifiedOn: Data modification date.

-	startStop: Information about the vehicle's start/stop system.

-	phevCity: City fuel consumption for plug-in hybrid vehicles.

-	phevHwy: Highway fuel consumption for plug-in hybrid vehicles.

-	phevComb: Combined fuel consumption for plug-in hybrid vehicles.

<h1></h1>


# VEHICLE ANNUAL EMISSIONS
<b>dataset:</b> clean_annual_emissions.csv

- vehicle: The make and model of the vehicle, including the model year.

- annual_fuel_use: The annual fuel consumption in gallons for the vehicle. Note that it may be 0 for electric vehicles (EVs).

- annual_electricity_use: The annual electricity consumption in kilowatt-hours (kWh) for the vehicle. This column is only applicable to electric vehicles.

- annual_fuel_elec_cost: The annual cost of fuel or electricity for operating the vehicle. It represents the total cost in dollars.

- annual_operating_cost : The total annual operating cost of the vehicle, including fuel or electricity costs, maintenance, and other expenses, represented in dollars.

- cost_per_mile: The cost per mile to operate the vehicle, which is calculated by dividing the annual operating cost by the mileage.

- annual_emissions_lbs_CO2: The annual emissions of carbon dioxide (CO2) in pounds produced by the vehicle. It reflects the environmental impact of the vehicle's fuel or electricity consumption

<h1></h1>