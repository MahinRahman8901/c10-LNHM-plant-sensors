import altair as alt
import pandas as pd


def get_latest_readings(df):
    """Gets latest readings of each plant"""
    df_sorted = df.sort_values(by='TimeRecorded', ascending=False)
    return df_sorted.groupby('PlantID').first().reset_index()


def latest_readings_temp(latest_readings):
    """Creates graph of overall latest temperture readings"""
    max_y = latest_readings['Temperature'].max() + 0.5
    min_y = latest_readings['Temperature'].min() - 0.5

    chart = alt.Chart(latest_readings).mark_point(size=100, filled=True).encode(
        x=alt.X('PlantID:N', title="Plant ID"),
        y=alt.Y('Temperature:Q', scale=alt.Scale(
            domainMin=min_y, domainMax=max_y)),
        color=alt.Color("PlantID:N", title="Plant Name", scale=alt.Scale(scheme='category20'),
                        legend=None),
        tooltip=['Temperature', 'PlantName', "PlantID"]).properties(
        title='Latest Overall Temperature Readings 🌡️')
    chart = chart.configure_title(
        fontSize=18, offset=20, orient='top', anchor='start')

    return chart


def latest_readings_soil(latest_readings):
    "Creates graph of overall latest soil moisture readings"
    max_y = latest_readings['SoilMoisture'].max() + 0.5
    min_y = latest_readings['SoilMoisture'].min() - 0.5

    chart = alt.Chart(latest_readings).mark_point(size=100, filled=True).encode(
        x=alt.X('PlantID:N', title="Plant ID"),
        y=alt.Y('SoilMoisture:Q', scale=alt.Scale(
            domainMin=min_y, domainMax=max_y), title="Soil Moisture"),
        color=alt.Color("PlantID:N", title="Plant Name", scale=alt.Scale(scheme='category20'),
                        legend=None),
        tooltip=['SoilMoisture', 'PlantName', "PlantID"]).properties(
        title='Latest Overall Soil Moisture Readings 💧')
    chart = chart.configure_title(
        fontSize=18, offset=20, orient='top', anchor='start')

    return chart


def get_temperature_over_last_24h(specific_plant_data):
    """Creates graph of temperature over last 24h for specific plant ID"""
    plant_id = specific_plant_data['PlantID'].iloc[0]
    chart = alt.Chart(specific_plant_data).mark_line().encode(
        x=alt.X('TimeRecorded:T', title='Time Recorded'),
        y=alt.Y('Temperature:Q'),
        color=alt.Color("PlantID:N", title="Plant ID", scale=alt.Scale(scheme='category20'),
                        legend=None),
        tooltip=[
            alt.Tooltip('TimeRecorded:T', title='Time Recorded',
                        format='%Y-%m-%d %H:%M:%S'),
            alt.Tooltip('Temperature:Q', title='Temperature'),
            alt.Tooltip('PlantID:N', title='Plant ID')]).properties(
        title=f'Temperature Over the Past 24h for Plant {plant_id} 🌡️')
    chart = chart.configure_title(
        fontSize=18, offset=20, orient='top', anchor='start')
    return chart


def get_moisture_over_last_24h(specific_plant_data):
    """Creates graph of moisture over last 24h for specific plant ID"""
    plant_id = specific_plant_data['PlantID'].iloc[0]
    chart = alt.Chart(specific_plant_data).mark_line().encode(
        x=alt.X('TimeRecorded:T', title='Time Recorded'),
        y=alt.Y('SoilMoisture:Q', title='Soil Moisture'),
        color=alt.Color("PlantID:N", title="Plant Name", scale=alt.Scale(scheme='category20'),
                        legend=None),
        tooltip=[
            alt.Tooltip('TimeRecorded:T', title='Time Recorded',
                        format='%Y-%m-%d %H:%M:%S'),
            alt.Tooltip('SoilMoisture:Q', title='Soil Moisture'),
            alt.Tooltip('PlantID:N', title='Plant ID')]).properties(
        title=f'Moisture Levels Over the Past 24h for Plant {plant_id} 💧')
    chart = chart.configure_title(
        fontSize=18, offset=20, orient='top', anchor='start')
    return chart


def get_moisture_over_time(specific_archived_data):
    """Creates graph of moisture over time for specific plant ID"""
    plant_id = specific_archived_data['PlantID'].iloc[0]
    chart = alt.Chart(specific_archived_data).mark_line().encode(
        x=alt.X('TimeRecorded:T', title="Time Recorded",
                axis=alt.Axis(tickCount="day")),
        y=alt.Y('SoilMoisture:Q', title="Soil Moisture"),
        color=alt.Color("PlantID:N", title="Plant Name", scale=alt.Scale(scheme='category20'),
                        legend=None),
        tooltip=[
            alt.Tooltip('TimeRecorded:T', title='Time Recorded',
                        format='%Y-%m-%d %H:%M:%S'),
            alt.Tooltip('SoilMoisture:Q', title='Soil Moisture'),
            alt.Tooltip('PlantID:N', title='Plant ID')]).properties(
        title=f'Moisture Levels Over Time for Plant {plant_id} 💧')
    chart = chart.configure_title(
        fontSize=18, offset=20, orient='top', anchor='start')
    return chart


def get_temperature_over_time(specific_archived_data):
    """Creates graph of temperature over time for specific plant ID"""
    plant_id = specific_archived_data['PlantID'].iloc[0]
    chart = alt.Chart(specific_archived_data).mark_line().encode(
        x=alt.X('TimeRecorded:T', axis=alt.Axis(
            tickCount="day"), title="Time Recorded"),
        y=alt.Y('Temperature:Q'),
        color=alt.Color("PlantID:N", title="Plant Name", scale=alt.Scale(scheme='category20'),
                        legend=None),
        tooltip=[
            alt.Tooltip('TimeRecorded:T', title='Time Recorded',
                        format='%Y-%m-%d %H:%M:%S'),
            alt.Tooltip('Temperature:Q', title='Soil Moisture'),
            alt.Tooltip('PlantID:N', title='Plant ID')]).properties(
        title=f'Temperature Over Time for Plant {plant_id} 🌡️')
    chart = chart.configure_title(
        fontSize=18, offset=20, orient='top', anchor='start')
    return chart
