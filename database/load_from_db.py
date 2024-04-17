"""A lambda function to move data older than 24 hours from the database to an S3 Bucket"""

import os
import json
import logging
import csv
import datetime
import pytz
from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect
from boto3 import client

UTC_NOW = utc_now = datetime.datetime.now(pytz.utc)
CURRENT_TIMESTAMP = utc_now.astimezone(pytz.timezone(
    'Europe/London')).strftime('%Y-%m-%d %H:%M:%S')
BUCKET = 'permian-triassic'
OBJ_NAME = f'data_{CURRENT_TIMESTAMP}'


def handler(event, context) -> dict:
    """event handler"""

    main()

    return {
        'statusCode': 200,
        'body': json.dumps({"response": "Data has been processed"})
    }


def get_db_connection(config):
    """Returns a live database connection."""

    return connect(
        server=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=config["DB_PORT"],
        as_dict=True
    )


def load_data(config):
    """Loads data older than 24 hours"""

    conn = get_db_connection(config)
    with conn.cursor() as cur:
        cur.execute(
            """SELECT * FROM s_epsilon.PlantMeasurementRecord \
                WHERE TimeRecorded < DATEADD(hour, -24, GETDATE());""")
        data = cur.fetchall()
        conn.close()
        return data


def convert_to_csv(data, filename):
    """creates a csv file containing the data"""

    fieldnames = data[0].keys()
    with open(os.path.join('/tmp', filename), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def upload_to_bucket(aws_client, file, bucket, obj_name):
    """uploads data to s3 bucket"""

    aws_client.upload_file(file, bucket, obj_name)


def delete_from_database(config):
    """deletes data older than 24 hours from database"""

    conn = get_db_connection(config)
    with conn.cursor() as cur:
        cur.execute(
            """DELETE FROM s_epsilon.PlantMeasurementRecord \
                WHERE TimeRecorded < DATEADD(hour, -24, GETDATE());""")
        conn.commit()
        conn.close()


def main():
    """main function"""

    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    s3_client = client("s3")

    old_data = load_data(ENV)
    logging.info(" Loaded old data from database")

    csv_file = f'data_{CURRENT_TIMESTAMP}.csv'

    if old_data:
        convert_to_csv(old_data, csv_file)
        upload_to_bucket(s3_client, f'/tmp/{csv_file}', BUCKET, OBJ_NAME)
        logging.info(" Uploaded csv file to s3 bucket successfully")
        delete_from_database(ENV)
        logging.info(" Removed old data from database")
    else:
        logging.info(" No data to upload.")
