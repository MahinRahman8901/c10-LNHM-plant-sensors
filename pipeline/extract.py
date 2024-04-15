import requests
import time

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

            plant_data.append(data_to_append)
        else:
            print("Could not find plant ", plant_id)
    return plant_data


if __name__ == "__main__":
    res = extract_plant_data()
    print(res)