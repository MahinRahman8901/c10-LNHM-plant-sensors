


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
    Country varchar(50) NOT NULL UNIQUE
)

CREATE TABLE Plant(
    PlantID INT IDENTITY(1,1) PRIMARY KEY,
    Name varchar(50) NOT NULL,
    ScientificName varchar(50),
    LocationID INT FOREIGN KEY REFERENCES Location(LocationID),
    BotanistID INT FOREIGN KEY REFERENCES Botanist(BotanistID)
)

CREATE TABLE PlantMeasurementRecord(
    MeasurementRecordID INT IDENTITY(1,1) PRIMARY KEY,
    TimeRecorded SMALLDATETIME NOT NULL,
    SoilMoisture DECIMAL(3,2) NOT NULL,
    Temperature DECIMAL(3,2) NOT NULL,
    PlantID INT FOREIGN KEY REFERENCES Plant(PlantID)
)

CREATE TABLE WateredRecord(
    WateredRecordID INT IDENTITY(1,1) PRIMARY KEY,
    TimeWatered SMALLDATETIME NOT NULL,
    PlantID INT FOREIGN KEY REFERENCES Plant(PlantID)
)

