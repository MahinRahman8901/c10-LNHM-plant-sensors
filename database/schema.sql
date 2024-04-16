CREATE TABLE Botanist(
    BotanistID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName varchar(20) NOT NULL, 
    LastName varchar(30) NOT NULL,
    Email varchar(50),
    Phone varchar(25)
    )

CREATE TABLE Location(
    LocationID INT IDENTITY(1,1) PRIMARY KEY,
    Town varchar(50) NOT NULL,
    City varchar(50) NOT NULL,
    CountryCode varchar(50) NOT NULL UNIQUE,
    Continent varchar(15) NOT NULL
)

CREATE TABLE Plant(
    PlantID INT IDENTITY(1,1) PRIMARY KEY,
    Name varchar(50) NOT NULL,
    ScientificName varchar(50),
    LocationID INT FOREIGN KEY REFERENCES Location(LocationID) NOT NULL,
    BotanistID INT FOREIGN KEY REFERENCES Botanist(BotanistID) NOT NULL
)

CREATE TABLE PlantMeasurementRecord(
    MeasurementRecordID INT IDENTITY(1,1) PRIMARY KEY,
    TimeRecorded SMALLDATETIME NOT NULL,
    SoilMoisture DECIMAL(5,2) NOT NULL,
    Temperature DECIMAL(5,2) NOT NULL,
    PlantID INT FOREIGN KEY REFERENCES Plant(PlantID)
)

CREATE TABLE WateredRecord(
    WateredRecordID INT IDENTITY(1,1) PRIMARY KEY,
    TimeWatered SMALLDATETIME NOT NULL,
    PlantID INT FOREIGN KEY REFERENCES Plant(PlantID)
)


INSERT INTO Botanist(FirstName, LastName, Email, Phone)
VALUES ('Isaac', 'Coleman', 'hopefullyidontmessthingsup@gmail.com', '46466')

INSERT INTO Location(Town, City, CountryCode, Continent)
VALUES ('South Whittier', 'LosAngeles', 'US', 'America')

INSERT INTO Plant(Name, ScientificName, LocationID, BotanistID)
VALUES ('Venus flytrap', 'NULL',1, 1)

INSERT INTO PlantMeasurementRecord(TimeRecorded, SoilMoisture, Temperature, PlantID)
VALUES ('2024-03-14 12:30:45', 30.25, 11.34, 1)

INSERT INTO WateredRecord(TimeWatered, PlantID)
VALUES ('2024-03-14 12:30:45', 1)