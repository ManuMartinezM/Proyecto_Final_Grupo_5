
<h1 align='center'>
 <b> DATA DICTIONARY </b>
</h1>


# Charging Stations:
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

# Alternative Fuel Vehicles
<b>dataset:</b> Alternative Fuel Vehicles US.csv


- Category: category based on the automotive body-style

- Model: car model

- Model Year: the year used to designate a discrete vehicle model, irrespective of the calendar year in which the vehicle was actually produced

- Manufacturer: the business entity (the company or brand) that produced the vehicle.

- Fuel: the car energy source

- All-Electric Range: the maximum driving range of an electric vehicle using only power from its on-board battery pack to traverse a given driving cycle
- PHEV Total Range: the maximum driving range of a Plug-in hybrid electric car. 
- Alternative Fuel Economy City: miles per gallon (MPG), to indicate how efficiently the vehicle consumes the alternative fuel in city driving scenarios.
- Alternative Fuel Economy Highway: This column provides the fuel efficiency of the vehicle using an alternative fuel source on the highway.
- Alternative Fuel Economy Combined: the combined fuel efficiency when using an alternative fuel source.
- Conventional Fuel Economy City: It contains information about the fuel efficiency of the vehicle when using conventional fuel (gasoline or diesel) in city driving conditions.
- Conventional Fuel Economy Highway: provides the fuel efficiency of the vehicle with conventional fuel on the highway.
- Conventional Fuel Economy Combined: This column specifies the combined fuel efficiency with conventional fuel. 
- Transmission Type:  indicates the type of transmission the vehicle has, such as "Automatic" or "Manual."
- Transmission Make: the manufacturer of the vehicle's transmission.
- Engine Type:specifies the type of engine, the motor.
- Engine Size: contains the engine's size, measured in liters or kilowatts(electric motor).
- Engine Cylinder Count: it provides the number of cylinders in the engine.
- Number of Passengers: specifies the seating capacity of the vehicle in terms of the number of passengers it can accommodate.
- Heavy-Duty Power System: to vehicles designed for heavy-duty or industrial use, the column contains information about their power systems.
- Notes: additional notes or remarks related to the vehicle, such as special features or comments.
- Drivetrain: the category that indicates the group of drivetrain parts that interact with the engine to move the wheels and various parts of the car to thrust it into motion.

<h1></h1>

#  Yellow Taxi Trip Records
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