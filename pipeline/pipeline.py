"""Main Pipeline Script"""

import aiohttp
import asyncio
import pandas as pd
import logging

from csv import DictReader
from datetime import datetime
from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect


API_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'


def get_database_connection(config):
    '''This function returns a database connection.'''

    return connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=int(config["DB_PORT"]),
    )


async def extract_plant_data() -> list[dict]:
    """Scrapes information from API asynchronously and returns a list of dictionaries"""

    plant_data = []
    async with aiohttp.ClientSession() as session:
        tasks = [extract_data_for_each_plant(
            session, plant_id) for plant_id in range(1, 51)]
        plant_data = await asyncio.gather(*tasks)
    return [data for data in plant_data if data is not None]


async def extract_data_for_each_plant(session, plant_id) -> dict:
    """Extracts data for each plant asynchronously"""

    url = f"{API_URL}{plant_id}"
    async with session.get(url) as response:
        if response.status == 200:
            plant_info = await response.json()
            data_to_append = {
                'id': plant_info.get('plant_id'),
                'name': plant_info.get('name'),
                'soil_moisture': plant_info.get('soil_moisture'),
                'temperature': plant_info.get('temperature'),
                'recording_taken': plant_info.get('recording_taken'),
                'last_watered': plant_info.get('last_watered'),
                'botanist_name': plant_info['botanist']['name'],
                'botanist_email': plant_info['botanist']['email'],
                'botanist_phone': plant_info['botanist']['phone']
            }

            if 'light_intensity' in plant_info:
                data_to_append['light_intensity'] = plant_info['light_intensity']

            if 'humidity' in plant_info:
                data_to_append['humidity'] = plant_info['humidity']

            if 'origin_location' in plant_info:
                origin_location = plant_info['origin_location']
                if len(origin_location) >= 3:
                    data_to_append['latitude'] = origin_location[0]
                    data_to_append['longitude'] = origin_location[1]
                    data_to_append['origin_location'] = origin_location[-3:]

            return data_to_append
        else:
            print(f"Could not find plant {plant_id}")


def clean_data(plant_data: list[dict]) -> list[dict]:
    """Cleans the plant data"""

    # Convert numerical values to float and round to 2 decimal places
    for plant in plant_data:
        plant['soil_moisture'] = round(float(plant['soil_moisture']), 2)
        plant['temperature'] = round(float(plant['temperature']), 2)

    # Make name consistent and remove punctuation
    for plant in plant_data:
        plant['name'] = plant['name'].title().replace(r'[^\w\s]', '')

    return plant_data


def get_botanist_id_dictionary(conn) -> dict:
    """Given a database connection (designed for our specific plants database), this
    function creates a dictionary with the keys being the botanist's emails and the value's
    being the botanist's id."""

    botanist_dict = {}

    with conn.cursor(as_dict=True) as cursor:
        cursor.execute('SELECT * FROM s_epsilon.Botanist')
        for row in cursor:
            botanist_dict[row['Email']] = row['BotanistID']
    return botanist_dict


def db_query_string(data: list[dict], conn) -> str:
    '''This outputs the data from a list of dictionaries in the form
    of a string with the specific structure:
    (value_1, value_2, ...),
    (value_1, value_2, ...),
    ...
    where each set of parentheses represents an element (dictionary in the list).'''

    botanist_dict = get_botanist_id_dictionary(conn)

    output_string = ""
    for row in data:
        # TimeRecorded, SoilMoisture, Temperature, TimeLastWatered, PlantID, BotanistID
        output_string += f"""( '{row['recording_taken']}', {float(row['soil_moisture'])},
          {float(row['temperature'])}, '{str(datetime.strptime(row['last_watered'], '%a, %d %b %Y %H:%M:%S %Z'))}',
            {int(row['id'])}, {int(botanist_dict[row['botanist_email']])} ),"""

    # Removing final unnecessary comma
    return output_string[:-1]


def db_inserting_data(query_string: str, conn) -> None:
    """This function inserts data into the PlantMeasurementRecord table, using the 
    inputted query string for the data."""

    with conn.cursor(as_dict=True) as cursor:
        cursor.execute(f"""INSERT INTO s_epsilon.PlantMeasurementRecord (TimeRecorded, SoilMoisture,
                        Temperature, TimeLastWatered, PlantID, BotanistID)
                       VALUES {query_string}""")
        conn.commit()


async def main():
    """Main function"""

    # Extract
    print("Fetching data...")
    plant_data = await extract_plant_data()
    logging.info("Successfully collected data")
    print("--- Collecting Data ---")

    # Transform
    cleaned_data = clean_data(plant_data)
    logging.info("Data successfully cleaned")
    print("--- Cleaning Data ---")

    # Connect
    connection = get_database_connection(ENV)
    logging.info("Connected to the database")
    print("--- Connecting to Database ---")

    # Load
    query_string = db_query_string(cleaned_data, connection)
    db_inserting_data(query_string, connection)
    logging.info("Data inserted into the database")
    print("--- Inserting into Database ---")

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
