"""Extract script to collect data from plants api"""

import logging
import csv
import requests

API_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'


def extract_plant_data() -> list[dict]:
    """Scrapes information from api and returns a list of dictionaries"""

    plant_data = []
    for plant_id in range(1, 51):
        extract_data_for_each_plant(plant_id, plant_data)
    return plant_data


def extract_data_for_each_plant(plant_id, plant_data) -> None:
    """Extracts data for each plant and appends to plant_data list"""

    url = f"{API_URL}{plant_id}"
    response = requests.get(url)
    if response.status_code == 200:
        plant_info = response.json()
        data_to_append = {
            'id': plant_info.get('plant_id'),
            'name': plant_info.get('name'),
            'soil_moisture': plant_info.get('soil_moisture'),
            'temperature': plant_info.get('temperature'),
            'recording_taken': plant_info.get('recording_taken'),
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
                data_to_append['origin_location'] = origin_location[-3:]

        plant_data.append(data_to_append)
    else:
        print(f"Could not find plant {plant_id}")


def create_csv_file(data: str, filename: str):
    """Creates csv file where all data collated
    from the api is stored and can be viewed"""
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def main():
    """Main function"""
    print("Fetching data...")
    plant_data = extract_plant_data()
    logging.info(" Successfully collected data")
    create_csv_file(plant_data, 'plants_data.csv')
    logging.info(" Saved to csv file")


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    main()
