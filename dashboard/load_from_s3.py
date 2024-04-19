"""Loads data from S3"""
import os
import csv
import datetime
from os import environ as ENV, remove
from fnmatch import fnmatch
import pytz
import pandas as pd
from dotenv import load_dotenv
from boto3 import client

UTC_NOW = datetime.datetime.now(pytz.utc)
CURRENT_TIMESTAMP = UTC_NOW.astimezone(pytz.timezone('Europe/London'))
FORMATTED_TIMESTAMP = CURRENT_TIMESTAMP.strftime('%H:%M:%S')
BUCKET_NAME = 'permian-triassic'
FILE_STRUCTURE = '*/*/*/*'
DIRECTORY = 'archived_data'
COMBINED_FILE = 'COMBINED_ARCHIVED_DATA.csv'


def get_bucket_objects(aws_client, bucket_name: str) -> list[str]:
    '''Return a list of available objects in a bucket.'''

    response = aws_client.list_objects(Bucket=bucket_name)
    objects = response['Contents']
    return [o["Key"] for o in objects]


def filter_objects(bucket_name: str, objects: list, file_structure: str, aws_client) -> list:
    '''Filters data that matches the file structure and has been created within the time interval'''

    return [o for o in objects if fnmatch(o, file_structure)]


def download_plant_data_files(aws_client, rel_obj: list, bucket: str, folder: str) -> None:
    '''Downloads relevant files from S3 to a data/ folder.'''

    if not os.path.exists(folder):
        os.makedirs(folder)

    for obj in rel_obj:
        aws_client.download_file(bucket,
                                 obj,
                                 f'{folder}/{obj.replace("/", "-")}.csv')


def extract(aws_client):
    """Extracts, filters and downloads relevant files"""

    objects = get_bucket_objects(aws_client, BUCKET_NAME)
    data = filter_objects(BUCKET_NAME, objects, FILE_STRUCTURE, aws_client)
    download_plant_data_files(aws_client, data, BUCKET_NAME, DIRECTORY)


def combine_plant_data_files(input_files: list, output_file: str, directory: str) -> None:
    """Loads and combines relevant files from the data/ folder.
    Produces a single combined file in the data/ folder."""

    headers = [
        'MeasurementRecordID', 'TimeRecorded', 'SoilMoisture', 'Temperature', 'PlantID',
        'BotanistID', 'TimeLastWatered', 'BotanistFirstName', 'BotanistLastName',
        'BotanistEmail', 'BotanistPhone', 'PlantName', 'Longitude', 'Latitude',
        'Town', 'City', 'CountryCode', 'Continent'
    ]

    file_path = f'{DIRECTORY}/{COMBINED_FILE}'
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

    dataset = []
    for file in input_files:
        file = f"{directory}/{file}"
        data = pd.read_csv(file)
        dataset.append(data)
        remove(file)
    if dataset:
        pd.concat(dataset).to_csv(
            f"{directory}/{output_file}", index=False, mode='w')


def load_data_from_s3():
    """Loads data from s3 to combined csv file"""

    load_dotenv()
    s3_client = client("s3",
                       aws_access_key_id=ENV["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    extract(s3_client)
    files = os.listdir(DIRECTORY)
    if COMBINED_FILE in files:
        os.remove(f"{DIRECTORY}/{COMBINED_FILE}")

    combine_plant_data_files(files, COMBINED_FILE, DIRECTORY)
    return pd.read_csv("archived_data/COMBINED_ARCHIVED_DATA.csv")
