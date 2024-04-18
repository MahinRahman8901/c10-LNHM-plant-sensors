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
import pandas as pd


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


def plant_anomaly_info(conn, anomalies: list[dict]):
    """This function takes in a list of dictionaries which each represent
    the rows from a plant measurement database, where there are anomalies in either 
    the temperature or soil moisture from the last hour.
    This function outputs a list of dictionaries - each representing a unique plant and having
    the total number of anomalies, total number of temperature anomalies and total number
        of soil moisture anomalies (in the last hour).
        e.g. {'plant_id': 47, 'temp_anomaly_num': 1, 'moisture_anomaly_num': 76, 'total_anomaly_num': 77}"""

    plant_id_name_dict = get_plant_id_name_dict(conn)
    print(plant_id_name_dict)

    # dataframe with each row being representing a plant with an anomaly (from the last hour)
    anomaly_df = pd.DataFrame(anomalies)

    plant_ids_with_anomalies = anomaly_df["plant_id"].unique()
    print(plant_ids_with_anomalies)

    anomaly_info = []
    for plant_id in plant_ids_with_anomalies:
        print(type(plant_id))
        print(plant_id_name_dict[plant_id])
        print(type(plant_id_name_dict[plant_id]))

        # Dataframe with anomaly rows for specific plant id
        plant_id_df = anomaly_df[anomaly_df['plant_id'] == plant_id]

        # Number of temperature anomalies
        plant_id_temp_df = plant_id_df[plant_id_df["temperature_anomaly"] == True]
        num_of_temp_anomalies = len(plant_id_temp_df.index)

        # number of moisture anomalies
        plant_id_moisture_df = plant_id_df[plant_id_df["moisture_anomaly"] == True]
        num_of_moisture_anomalies = len(plant_id_moisture_df.index)

        anomaly_info.append({"plant_id": plant_id, "plant_name": plant_id_name_dict[plant_id], "temp_anomaly_num": num_of_temp_anomalies,
                            "moisture_anomaly_num": num_of_moisture_anomalies, "total_anomaly_num": num_of_temp_anomalies+num_of_moisture_anomalies})

    return sorted(
        anomaly_info, key=lambda x: x["total_anomaly_num"], reverse=True)


def get_plant_id_name_dict(conn) -> dict:
    """This function returns a dictionary with the plant ids as keys
    and the plant name as the values """

    with conn.cursor(as_dict=True) as cur:
        query = "SELECT PlantID, Name FROM s_epsilon.Plant;"
        cur.execute(query)
        db_list = cur.fetchall()

    plant_id_name_dict = {}
    for dict in db_list:
        plant_id_name_dict[dict['PlantID']] = dict['Name']

    return plant_id_name_dict


def email_html(anomaly_data: list[dict]) -> str:
    """This function accepts a list of dictionaries of anomaly data for plants
     and returns a html formatted string intended for an email. """

    current_datetime = datetime.datetime.now()
    one_hour_ago = current_datetime - datetime.timedelta(hours=1)

    html_table_sub_string = ""
    for plant in anomaly_data:
        html_table_sub_string += f"""<tr>
                                    <td>{plant["plant_id"]}</td>
                                    <td>{plant["plant_name"]}</td>
                                    <td>{plant["total_anomaly_num"]}</td>
                                    <td>{plant["temp_anomaly_num"]}</td>
                                    <td>{plant["moisture_anomaly_num"]}</td>
                                    </tr>"""

    html_string = f"""

            <!DOCTYPE html>
            <html>
            <head>
                <title>Anomaly Report from the Hour</title>
            </head>
            <body>
                <h1>Anomaly Table</h1>
                <p>Here is a table of measurement anomalies of the plants in the last hour  ({datetime.datetime.strftime(current_datetime, "%H:%M:%S")} to {datetime.datetime.strftime(one_hour_ago, "%H:%M:%S")}).</p>
 
                <table>
                    <tr>
                        <th>Plant ID</th>
                        <th>Plant Name</th>
                        <th>Total Number of Anomalies</th>
                        <th>Number of Temperature Anomalies</th>
                        <th>Number of Soil Moisture Anomalies</th>
                    </tr>
    
                    {html_table_sub_string}
                </table>

            </body>
            </html>
                    """

    return html_string


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
        # Check anomalies
        if anomalies:
            print("Anomalies detected:")
        else:
            print("No anomalies detected.")
    else:
        print("No data retrieved from the database.")

    # The data used in the email
    plant_anomaly_info = plant_anomaly_info(conn, anomalies)

    # The html for the email as a string
    email_html = email_html(plant_anomaly_info)

    conn.close()

    """
    TO DO :

    - CREATE FUNCTION THAT RETURNS DICTIONARY {Plant_id: plant_name}

     - FORMAT EMAIL WITH INFORMATION:
         - TITLE / HEADER
         - TABLE
            - 50 ROWS (FOR EACH PLANT) ORDERED BY MOST ANOMALIES (IN PAST HOUR)
            - 5 COLUMNS: PLANT ID, PLANT NAME, TOTAL NUM OF ANOMALIES, NUM OF TEMP ANOMALIES, NUM OF MOISTURE ANOMALIES

    - CREATE FUNCTION WHICH SENDS AN EMAIL WHEN THE SCRIPT IS RAN
    
    

    """
