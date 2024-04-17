'''A load script as part of the data pipeline. This script moves the data from the csv file, produced by the
transform script, to a database.'''

from csv import DictReader
from datetime import datetime
from dotenv import load_dotenv
from os import environ as ENV
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


def read_csv(csv_file_path:str) -> list[dict[str]]:
    '''This function reads a csv file and outputs a list of dictionaries - 
     Each dictionary corresponds to a row in the csv file where the keys are
     the elements in the first row of the file.
     Example: {'gertrude.jekyll@lnhm.co.uk': 1, 'carl.linnaeus@lnhm.co.uk': 2, 'eliza.andrews@lnhm.co.uk': 3}'''
    
    with open(csv_file_path, 'r') as f:
        data = DictReader(f)
        data_list = list(data)

    return data_list


def db_query_string(data:list[dict], conn) -> str:
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
        output_string += f"( '{row['recording_taken']}', {float(row['soil_moisture'])}, {float(row['temperature'])}, '{str(datetime.strptime(row['last_watered'], '%a, %d %b %Y %H:%M:%S %Z'))}', {int(row['id'])}, {int(botanist_dict[row['botanist_email']])} ),"


    # Removing final unnecessary comma
    return output_string[:-2]

   
def db_inserting_data(query_string:str, conn):
    """This function inserts data into the PlantMeasurementRecord table, using the 
    inputted query string for the data."""

    with conn.cursor(as_dict=True) as cursor:
        cursor.execute("""INSERT INTO s_epsilon.PlantMeasurementRecord (TimeRecorded, SoilMoisture, Temperature, TimeLastWatered, PlantID, BotanistID)
                       VALUES %s""", query_string)
 
        conn.commit()

if __name__ == "__main__":

    load_dotenv()

    print('before connection')
    conn = get_database_connection(ENV)
    print('after connection')



    botanist_dict = get_botanist_id_dictionary(conn)
    print(f"Botanist Dict: {botanist_dict}")

    
    data = read_csv("plants_data.csv")
    query_string = "('2024-04-17 08:10:20', 35.29, 12.02, '2024-04-16 13:54:32', 1, 1 )"
    print(query_string)
    print('before inserting into db')
    db_inserting_data(query_string, conn)
    print('after inserting into db')



    

