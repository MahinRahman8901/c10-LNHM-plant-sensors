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

    # Ensure each location has 4 elements (town, country_code, continent, city)
    plant_df['origin_location'] = plant_df['origin_location'].apply(
        lambda x: x + [None] * (4 - len(x)) if len(x) < 4 else x[:4])

    # Split the origin location into town, country_code, continent, and city
    origin_df = pd.DataFrame(plant_df['origin_location'].tolist(), columns=[
                             'town', 'country_code', 'continent', 'city'])

    # Split the continent values at '/' and put them in the city column
    origin_df['city'] = origin_df['continent'].apply(
        lambda x: x.split('/')[-1])
    origin_df['continent'] = origin_df['continent'].apply(
        lambda x: x.split('/')[0])

    plant_df = pd.concat([plant_df, origin_df], axis=1)

    # Drop the original origin_location column
    plant_df.drop(columns=['origin_location'], inplace=True)

    # Save the cleaned data to a new CSV file
    plant_df.to_csv(filename, index=False)


if __name__ == "__main__":
    clean_data_from_csv(CSV)
