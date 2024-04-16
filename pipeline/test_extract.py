"""Tests API requests in extract script"""

from extract import extract_data_for_each_plant, API_URL

plant_test_data = {
    "botanist": {
        "email": "carl.linnaeus@lnhm.co.uk",
        "name": "Carl Linnaeus",
        "phone": "(146)994-1635x35992"
    },
    "last_watered": "Mon, 15 Apr 2024 14:10:54 GMT",
    "name": "Corpse flower",
    "origin_location": [
        "7.65649",
        "4.92235",
        "Efon-Alaaye",
        "NG",
        "Africa/Lagos"
    ],
    "plant_id": 2,
    "recording_taken": "2024-04-16 12:21:22",
    "soil_moisture": 27.36278335759782,
    "temperature": 9.117554081392257
}

output_data = [{'id': 2, 'name': 'Corpse flower',
                'soil_moisture': 27.36278335759782,
                'temperature': 9.117554081392257,
                'recording_taken': '2024-04-16 12:21:22',
                'origin_location': [
                    'Efon-Alaaye',
                    'NG',
                    'Africa/Lagos']}]


plant_data = []


def test_api_call_successful(requests_mock):
    url = f'{API_URL}2'
    requests_mock.get(url, json=plant_test_data)
    extract_data_for_each_plant(2, plant_data)
    assert plant_data == output_data


def test_api_call_unsuccessful(requests_mock, capsys):
    url = f'{API_URL}2'
    requests_mock.get(url, status_code=400)
    extract_data_for_each_plant(2, plant_data)
    captured = capsys.readouterr()
    printed_output = captured.out
    assert "Could not find plant 2" in printed_output
