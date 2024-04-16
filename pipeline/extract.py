import requests
import time
import csv
import schedule

API_URL = 'https://data-eng-plants-api.herokuapp.com/plants/'


def extract_plant_data() -> dict:
    """Scrapes information from api and return a dictionary"""

    plant_data = []
    for plant_id in range(1, 51):
        url = f"{API_URL}{plant_id}"
        response = requests.get(url)
        if response.status_code == 200:
            plant_info = response.json()
            data_to_append = {
                'id': plant_info.get('plant_id'),
                'name': plant_info.get('name'),
                'soil_moisture': plant_info.get('soil_moisture'),
                'temperature': plant_info.get('temperature'),
                'recording_taken': plant_info.get('recording_taken')
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
            print("Could not find plant ", plant_id)
    return plant_data


def create_csv_file(data: str, filename: str):
    """Creates csv file where all data collated
    from the api is stored and can be viewed"""
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def job():
    print("Fetching data...")
    plant_data = extract_plant_data()
    create_csv_file(plant_data, 'plants_data.csv')


if __name__ == "__main__":
    schedule.every().minute.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
