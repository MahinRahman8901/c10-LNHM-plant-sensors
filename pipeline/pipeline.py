"""Extract script to collect data from plants api"""

import logging
import csv
import aiohttp
import asyncio
import logging
import pandas as pd
from csv import DictReader
from datetime import datetime
from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect


API_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'
CSV = "plants_data.csv"


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


def create_csv_file(data: list[dict], filename: str):
    """Creates CSV file where all data collated from the API is stored"""
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


async def main():
    """Main function"""
    print("Fetching data...")
    plant_data = await extract_plant_data()
    logging.info("Successfully collected data")
    if plant_data:
        create_csv_file(plant_data, 'plants_data.csv')
        logging.info("Saved to CSV file")
    else:
        logging.warning("No data found, CSV file not created")


def clean_data_from_csv(filename: str):
    """Uses pandas to clean and make all values consistent
    in the csv file"""

    plant_df = pd.read_csv(filename)

    plant_df['origin_location'] = plant_df['origin_location'].apply(eval)

    # Round numerical values to 2 decimal places
    plant_float_columns = plant_df.select_dtypes(include=['float64']).columns
    plant_df[plant_float_columns] = plant_df[plant_float_columns].round(2)

    # Makes name value consistent and gets rid of punctuation
    plant_df['name'] = plant_df['name'].str.title().str.replace(r'[^\w\s]', '')

    # Ensure each location has 4 elements (town, country_code, continent, city)
    plant_df['origin_location'] = plant_df['origin_location'].apply(
        lambda x: x + [None] * (4 - len(x)) if len(x) < 4 else x[:4])

    # Split the origin location into town, country_code, continent, and city
    origin_df = pd.DataFrame(plant_df['origin_location'].tolist(), columns=[
                             'town', 'country_code', 'continent', 'city'])

    # Split the continent values at '/' and put them in the city column
    origin_df['city'] = origin_df['continent'].apply(
        lambda x: x.split('/')[-1])
    origin_df['continent'] = origin_df['continent'].apply(
        lambda x: x.split('/')[0])

    plant_df = pd.concat([plant_df, origin_df], axis=1)

    # Drop the original origin_location column
    plant_df.drop(columns=['origin_location'], inplace=True)

    # Save the cleaned data to a new CSV file
    plant_df.to_csv(filename, index=False)


def get_database_connection(config):
    '''This function returns a database connection.'''

    return connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=int(config["DB_PORT"]),
    )


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


def read_csv(csv_file_path: str) -> list[dict[str]]:
    '''This function reads a csv file and outputs a list of dictionaries - 
     Each dictionary corresponds to a row in the csv file where the keys are
     the elements in the first row of the file.
     Example: {'gertrude.jekyll@lnhm.co.uk': 1, 'carl.linnaeus@lnhm.co.uk': 2,
       'eliza.andrews@lnhm.co.uk': 3}'''
    with open(csv_file_path, 'r') as f:
        data = DictReader(f)
        data_list = list(data)

    return data_list


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


if __name__ == "__main__":

    load_dotenv()

    # Extract
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

    # Transform
    logging.basicConfig(level=logging.INFO)
    clean_data_from_csv(CSV)
    logging.info("Data successfully cleaned.")

    # Load
    connection = get_database_connection(ENV)
    print('--- CONNECTED TO DATABASE ---')

    # data from csv as list of dictionaries
    plant_data = read_csv("plants_data.csv")
    # the values section of the insert query string
    insert_query_string = db_query_string(plant_data, connection)
    db_inserting_data(insert_query_string, connection)
    print('--- INSERTED INTO DATABASE ---')
