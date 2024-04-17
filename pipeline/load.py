'''A load script as part of the data pipeline. This script moves the data from the csv file, produced by the
transform script, to a database.'''

from csv import DictReader
from datetime import datetime
from dotenv import load_dotenv
from os import environ as ENV
#from pymssql import connect


def get_database_connection(config):
    '''This function returns a database connection.'''

    return connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=int(config["DB_PORT"]),
    )

def read_csv(csv_file_path:str) -> list[dict[str]]:
    '''This function reads a csv file and outputs a list of dictionaries - 
     Each dictionary corresponds to a row in the csv file where the keys are
     the elements in the first row of the file.'''
    
    with open(csv_file_path, 'r') as f:
        data = DictReader(f)
        data_list = list(data)

    return data_list


def get_botanist_id_dictionary(conn) -> dict:
    """Given a database connection (designed for our specific plants database), this
    function creates a dictionary with the keys being the botanist's emails and the value's
    being the botanist's id."""




def db_insert_query(data:list[dict]) -> str:
    '''This outputs the data from a list of dictionaries in the form
    of a string with the specific structure:
    (value_1, value_2, ...),
    (value_1, value_2, ...),
    ...
    where each set of parentheses represents an element (dictionary in the list).'''

    
    output_string = ""
    for row in list:
        # TimeRecorded, SoilMoisture, Temperature, TimeLastWatered, PlantID, BotanistID

        #f"{row['recording_taken']}, {float(row['soil_moisture'])}, {float(row['temperature'])}, {str(datetime.strptime(row['last_watered'], "%a, %d %b %Y %H:%M:%S %Z"))},
        #{row['id'], }"

        # ADD BOTANIST ID + (), ( DONT FORGET FINAL LINE WHICH DOESNT NEED ')

        pass






if __name__ == "__main__":

    load_dotenv()

    print('before connection')
    #conn = get_database_connection(ENV)
    print('after connection')

    data = read_csv("plants_data.csv")

    print(data[1])
    #print(len(data))

    last_watered = 'Tue, 16 Apr 2024 14:10:54 GMT'

    last_watered_updated = str(datetime.strptime(last_watered, "%a, %d %b %Y %H:%M:%S %Z"))

    print(last_watered_updated)
    print(type(last_watered_updated))
  

 
    

