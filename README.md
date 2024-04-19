# LMNH Plant Pipeline

# README

## Pipeline

The `pipeline.py` script orchestrates the entire data pipeline process. It asynchronously fetches plant data from the provided API endpoint, cleans the data, and inserts it into the database. The script handles extraction, transformation, and loading of data in a seamless manner.

## Overview

The pipeline script consists of several steps:

1. **Extract**: Asynchronously fetches plant data from an external API (`API_URL`) for each plant ID in the range 1 to 50.

2. **Transform**: Cleans the retrieved data, converting numerical values to float and rounding to 2 decimal places. It also standardises plant names and removes punctuation.

3. **Load**: Inserts the cleaned data into a Relational Database. It first establishes a database connection using the provided environment variables and then constructs SQL query strings to insert the data into the database.

## Asynchronous Data Extraction

The script utilises aiohttp library for asynchronous HTTP requests, allowing it to fetch data from the API efficiently. Each plant's data is extracted concurrently, improving the overall performance of the extraction process and overall speed of requests.

## Data Cleaning

After fetching the data, the script performs cleaning operations to ensure consistency and data integrity. It converts numerical values to floats, rounds them to two decimal places, and standardises plant names.

## Database Interaction

The script establishes a database connection using the provided environment variables and inserts the cleaned data into the Database. It constructs SQL query strings dynamically based on the cleaned data and executes them to insert the data into the database.

## Logging and Error Handling

The script utilizes the logging module to log important events and errors during the execution process. This helps in debugging and monitoring the pipeline's performance.

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

## LMNH Plant Health Dashboard (Streamlit)

![Streamlit Dashboard](https://github.com/MahinRahman8901/c10-LNHM-plant-sensors/blob/main/images/Streamlit.png?raw=true)

### Features
- **Real-time Monitoring:** View the latest temperature and soil moisture readings for each plant.
- **Historical Analysis:** Explore temperature and soil moisture trends over the past 24 hours and over time for individual plants.
- **Statistical Insights:** Obtain statistical summaries such as the number of plants, botanists, origins, as well as extreme values for temperature and soil moisture.

### Usage
- Upon launching the app, you'll be presented with a sidebar to select a specific plant ID.
- The main dashboard displays various visualizations including temperature and soil moisture charts.
- Additionally, you can explore statistical summaries and extreme values in the metrics section.

### Data Sources
- **Database:** The app retrieves real-time plant data from a database using SQL queries.
- **S3 Bucket:** Historical plant data is obtained from an S3 bucket, allowing for long-term analysis.



## Setup
To contribute to the project, follow these steps:

1. Clone the repository.
2. Set up the development environment as per the instructions in the `README.md` file.
3. Start working on your assigned tasks or create a new one if needed.
4. Submit a pull request once your changes are ready for review.
