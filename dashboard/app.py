"""Streamlit App"""

from os import environ as ENV
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from charts import (latest_readings_temp, latest_readings_soil,
                    get_latest_readings, get_moisture_over_last_24h,
                    get_temperature_over_last_24h, get_moisture_over_time,
                    get_temperature_over_time)
from load_from_db import get_db_connection, format_data, load_data
from load_from_s3 import load_data_from_s3


def set_page_config():
    """Set page config"""
    st.set_page_config(
        layout="wide",
        page_title="LMNH Plant Health",
        page_icon="🌱")

    st.sidebar.title("Dashboard")
    st.sidebar.subheader("Select Plant ID")

    st.subheader("🌱 LMNH Plant Health 🌱")


def get_extreme_values(data, column):
    """Function to get the lowest and highest values along with their corresponding PlantIDs."""

    min_value = data[column].min()
    min_index = data[column].idxmin()
    min_plant_id = data.loc[min_index, 'PlantID']

    max_value = data[column].max()
    max_index = data[column].idxmax()
    max_plant_id = data.loc[max_index, 'PlantID']

    return min_value, min_plant_id, max_value, max_plant_id


def get_specific_plant(data):
    """Filter for a specific Plant ID"""
    plants = data['PlantID'].unique()
    return st.sidebar.selectbox('Plant ID', plants)


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_connection(ENV)

    plant_data = pd.DataFrame(format_data(load_data(ENV)))

    set_page_config()

    plant_id = get_specific_plant(plant_data)
    specific_plant_data = plant_data[plant_data['PlantID'] == plant_id]
    latest_readings = get_latest_readings(plant_data)

    archived_data = load_data_from_s3()
    specific_archived_data = archived_data[archived_data['PlantID'] == plant_id]

    chart_1 = latest_readings_temp(latest_readings)
    chart_2 = latest_readings_soil(latest_readings)
    chart_3 = get_moisture_over_last_24h(specific_plant_data)
    chart_4 = get_temperature_over_last_24h(specific_plant_data)
    chart_5 = get_moisture_over_time(specific_archived_data)
    chart_6 = get_temperature_over_time(specific_archived_data)

    lowest_moisture, lowest_moisture_id, highest_moisture, highest_moisture_id = get_extreme_values(
        latest_readings, 'SoilMoisture')
    lowest_temp, lowest_temp_id, highest_temp, highest_temp_id = get_extreme_values(
        latest_readings, 'Temperature')

    one, two, three = st.columns(3)
    with one:
        st.metric("Number of Plants 🌿", plant_data["PlantID"].nunique())
    with two:
        st.metric("Number of Botanists 👩‍🌾 ",
                  plant_data["BotanistEmail"].nunique())
    with three:
        st.metric("Number of Origins 🌎", plant_data["City"].nunique())

    one, two, three, four,  = st.columns(4)
    with one:
        st.metric(label="Highest Moisture 💧",
                  value=f"🪴 {highest_moisture_id}: {highest_moisture}")
    with two:
        st.metric(label="Lowest Moisture 💧",
                  value=f"🪴 {lowest_moisture_id}: {lowest_moisture}")
    with three:
        st.metric(label="Highest Temperature 🌡️",
                  value=f"🪴 {highest_temp_id}: {highest_temp}")
    with four:
        st.metric(label="Lowest Temperature 🌡️",
                  value=f"🪴 {lowest_temp_id}: {lowest_temp}")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.altair_chart(chart_1, use_container_width=True)
    st.altair_chart(chart_2, use_container_width=True)
    st.altair_chart(chart_4, use_container_width=True)
    st.altair_chart(chart_3, use_container_width=True)
    st.altair_chart(chart_6, use_container_width=True)
    st.altair_chart(chart_5, use_container_width=True)
