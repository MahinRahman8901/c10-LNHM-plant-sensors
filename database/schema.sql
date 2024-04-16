CREATE TABLE s_epsilon.Botanist(
    BotanistID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName varchar(20) NOT NULL, 
    LastName varchar(30) NOT NULL,
    Email varchar(50),
    Phone varchar(25)
    )

CREATE TABLE s_epsilon.Location(
    LocationID INT IDENTITY(1,1) PRIMARY KEY,
    Longitude DECIMAL(11,6) NOT NULL,
    Latitude DECIMAL (11,6) NOT NULL,
    Town varchar(50) NOT NULL,
    City varchar(50) NOT NULL,
    CountryCode varchar(50) NOT NULL UNIQUE,
    Continent varchar(15) NOT NULL
)

CREATE TABLE s_epsilon.Plant(
    PlantID INT IDENTITY(1,1) PRIMARY KEY,
    Name varchar(50) NOT NULL,
    ScientificName varchar(50),
    LocationID INT FOREIGN KEY REFERENCES Location(LocationID) NOT NULL,
)

CREATE TABLE s_epsilon.PlantMeasurementRecord(
    MeasurementRecordID INT IDENTITY(1,1) PRIMARY KEY,
    TimeRecorded SMALLDATETIME NOT NULL,
    SoilMoisture DECIMAL(5,2) NOT NULL,
    Temperature DECIMAL(5,2) NOT NULL,
    PlantID INT FOREIGN KEY REFERENCES Plant(PlantID)
)

CREATE TABLE s_epsilon.WateredRecord(
    WateredRecordID INT IDENTITY(1,1) PRIMARY KEY,
    TimeWatered SMALLDATETIME NOT NULL,
    PlantID INT FOREIGN KEY REFERENCES Plant(PlantID)
)

CREATE TABLE s_epsilon.BotanistPlantRecord(
    TimeRecorded SMALLDATETIME NOT NULL,
    PlantID INT FOREIGN KEY REFERENCES Plant(PlantID),
    BotanistID INT FOREIGN KEY REFERENCES Botanist(BotanistID)
)