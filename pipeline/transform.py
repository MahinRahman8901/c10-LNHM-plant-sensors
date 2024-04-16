import pandas as pd

CSV = "plants_data.csv"


def clean_data_from_csv(filename: str):
    """Uses pandas to clean and make all values consistent
    in the csv file"""

    plant_df = pd.read_csv(filename)

    plant_df['origin_location'] = plant_df['origin_location'].apply(eval)

    # Round numerical values to 2 decimal places
    plant_float_columns = plant_df.select_dtypes(include=['float64']).columns
    plant_df[plant_float_columns] = plant_df[plant_float_columns].round(2)

    # Makes name value consistent and gets rid of punctuation
    plant_df['name'] = plant_df['name'].str.title().str.replace(r'[^\w\s]', '')

    # Separates the origin location into singular columns
    plant_df[['town', 'country_code', 'continent', 'city']] = pd.DataFrame(
        plant_df['origin_location'].tolist(), index=plant_df.index)

    # Drops the origin location after it has been cleaned and separated
    plant_df.drop(columns=['origin_location'], inplace=True)

    # Drops any null values if exists
    plant_df.dropna(inplace=True)

    plant_df.to_csv(filename, index=False)


if __name__ == "__main__":
    clean_data_from_csv(CSV)
