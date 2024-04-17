# README

## Pipeline

### Data Extraction Sript

The `extract.py` script fetches plant data from the provided API endpoint. It retrieves information such as soil moisture, temperature, humidity, and light intensity for each plant and stores it in a CSV file.

### Data Cleaning Script

The `transform.py` script utilises pandas to clean and standardise the data extracted from the CSV file. It rounds numerical values to two decimal places, standardises plant names, separates the origin location into individual columns (town, country code, continent, city), and removes any null values. The cleaned data is then saved back to the CSV file.

## BASH Database Scripts

We have also implemented bash scripts in order to simplify and automate connection and manipulation of the database. These will, however, depend on the Environemental Variables. Therefore, make sure that you have a .env file with the correct values for each variable within the file. in order to run these files within the terminal you need to exectute `bash [.sh script]`

### Connection

For this we have a `connect.sh` which connects us directly to the database by running the command.

### Table Creation

For this we have a `create_tables.sh` that runs the `schema.sql` into the database itself and adds all the tables with its corrosponding keys.

### Seeding Data

For this we have a `seed_data.sh` which will run the `seed.sql` script into the database, therefore inserting all the static data into the tables within the database as well.


## About

The Liverpool Natural History Museum is expanding its focus to include botanical science with the introduction of a new botanical wing in 2023. To support this initiative, the museum requires a robust system to monitor the health of plants in their conservatory. This GitHub repository documents the development and implementation of the Plant Health Monitoring System.

## Problem Statement

The current system only provides real-time data via a simple API endpoint, limiting the museum's ability to monitor plant health over time and detect issues promptly. To address this, the museum requires:

- A comprehensive data pipeline hosted in the cloud.
- Short-term and long-term storage solutions for plant data.
- Visualization capabilities to view real-time and historical plant data.

## Hardware

The museum has invested in an array of sensors connected to a Raspberry Pi to monitor environmental factors affecting plant growth. However, the current setup faces challenges such as data reliability issues.

## Deliverables

### Data Pipeline

- Extract data from the provided API endpoint for each plant every minute.
- Clean and verify data before storing it in a fully normalized database.

### Short-Term Storage

- Host the past 24 hours of data in a temporary database solution to manage costs.
- Export older data to long-term storage.

### Long-Term Storage

- Host all data older than 24 hours in a cost-efficient long-term data-storage solution.

### Visualization

- Real-time visualization of plant data.
- Graphical representation of temperature and moisture readings for each plant.
- Access to historical data stored in long-term storage.

## Diagrams 

### ERD Diagram

![ERD Diagram](https://github.com/MahinRahman8901/c10-LNHM-plant-sensors/blob/main/images/ERD.png?raw=true)

### System Architecture Diagram

![System Architecture Diagram](https://github.com/MahinRahman8901/c10-LNHM-plant-sensors/blob/main/images/System%20Architecture.png?raw=true)


To contribute to the project, follow these steps:

1. Clone the repository.
2. Set up the development environment as per the instructions in the `README.md` file.
3. Start working on your assigned tasks or create a new one if needed.
4. Submit a pull request once your changes are ready for review.
