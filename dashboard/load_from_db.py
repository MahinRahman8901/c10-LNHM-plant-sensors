"""Loads data from database"""
from decimal import Decimal
from pymssql import connect


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
            """SELECT PMR.*,
       Bot.FirstName AS BotanistFirstName,
       Bot.LastName AS BotanistLastName,
       Bot.Email AS BotanistEmail,
       Bot.Phone AS BotanistPhone,
       Plant.Name AS PlantName,
       Loc.Longitude,
       Loc.Latitude,
       Loc.Town,
       Loc.City,
       Loc.CountryCode,
       Loc.Continent
FROM s_epsilon.PlantMeasurementRecord PMR
JOIN s_epsilon.Botanist Bot ON PMR.BotanistID = Bot.BotanistID
JOIN s_epsilon.Plant Plant ON PMR.PlantID = Plant.PlantID
JOIN s_epsilon.Location Loc ON Plant.LocationID = Loc.LocationID;""")
        data = cur.fetchall()
        conn.close()
        return data


def format_data(data):
    """Converts Decimal to float"""
    for entry in data:
        for key, value in entry.items():
            if isinstance(value, Decimal):
                entry[key] = float(value)
    return data
