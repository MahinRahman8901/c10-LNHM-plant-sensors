import csv
import numpy as np
import boto3
import datetime
from decimal import Decimal

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect


def get_database_connection(config):
    '''This function returns a database connection.'''

    return connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=int(config["DB_PORT"]),
    )


def fetch_data_from_last_hour(conn):
    """Retrieves data from the last hour from the database"""
    with conn.cursor(as_dict=True) as cur:
        query = "SELECT * FROM s_epsilon.PlantMeasurementRecord WHERE TimeRecorded >= DATEADD(hour, -1, GETDATE())"
        cur.execute(query)
        return cur.fetchall()


def search_anomalies(data: list[dict]):
    """Filters through the data and finds any anomalies via
    standard deviation"""

    anomalies = []
    moisture_values = [row['SoilMoisture'] for row in data]
    temperature_values = [row['Temperature'] for row in data]
    moisture_deviation = np.std(moisture_values)
    temperature_deviation = np.std(temperature_values)

    for row in data:
        moisture_anomaly = False
        temperature_anomaly = False
        if abs(row['SoilMoisture'] - np.mean(moisture_values)) > 2 * moisture_deviation:
            moisture_anomaly = True
        if abs(row['Temperature'] - np.mean(temperature_values)) > 2 * temperature_deviation:
            temperature_anomaly = True
        if moisture_anomaly or temperature_anomaly:
            anomalies.append({
                'timestamp': row['TimeRecorded'],
                'plant_id': row['PlantID'],
                'moisture_anomaly': moisture_anomaly,
                'temperature_anomaly': temperature_anomaly,
                'moisture_value': row['SoilMoisture'],
                'temperature_value': row['Temperature']
            })

    return anomalies


if __name__ == "__main__":
    load_dotenv()

    # Establish database connection
    conn = get_database_connection(ENV)

    # Fetch data from the database
    data = fetch_data_from_last_hour(conn)

    # Check if data is retrieved properly
    if data:
        print("Data retrieved successfully.")
        anomalies = search_anomalies(data)
        # Check if anomalies are found
        if anomalies:
            print("Anomalies detected:", anomalies)
        else:
            print("No anomalies detected.")
    else:
        print("No data retrieved from the database.")

    conn.close()
