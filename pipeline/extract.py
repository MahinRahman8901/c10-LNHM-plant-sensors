"""Extract script to collect data from plants api"""

import logging
import csv
import aiohttp
import asyncio

API_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
