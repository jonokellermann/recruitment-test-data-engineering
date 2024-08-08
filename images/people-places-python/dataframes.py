"""Module containing functions that create dataframes."""
import pandas as pd


def assign_unique_id(unique_value, length_of_id):
    """Assign a unique id of type string to a value.

    Args:
        unique_value (str): A string value
        length_of_id (int): the length of the unique id

    Returns:
        str: A unique id of type string of a series of numbers.
    """
    import hashlib

    m = hashlib.sha256()
    # remove whitespace and lowercase the string
    unique_value = str(unique_value).strip().lower()
    string = unique_value.encode("utf-8")
    m.update(string)
    return str(int(m.hexdigest(), 16))[0:length_of_id]


def create_country_pdf(places_csv_path, country_id_length=5):
    """Create a normalized dataframe for country from places.csv file.

    Args:
        places_csv_path (str): the path to places.csv (/data/places.csv)
        country_id_length (int, Defaults to 5): the length of country_id

    Returns:
        PandasDF
    """
    # Read places.csv into a Panda DF
    places_pdf = pd.read_csv(places_csv_path, encoding="utf-8")

    # Create a dataframe for unique country and its country_id
    country_pdf = pd.DataFrame(places_pdf["country"].unique(), columns=["country_name"])
    country_pdf["country_id"] = country_pdf["country_name"].apply(
        lambda x: assign_unique_id(x, country_id_length)
    )
    country_pdf = country_pdf[["country_id", "country_name"]]
    return country_pdf


def create_city_pdf(places_csv_path, city_id_length=8):
    """Create a normalized dataframe for city from places.csv file.

    Args:
        places_csv_path (str): the path to places.csv (/data/places.csv)
        city_id_length (int, Defaults to 8): the length of city_id

    Returns:
        PandasDF
    """
    # Read places.csv into a Panda DF
    places_pdf = pd.read_csv(places_csv_path, encoding="utf-8")
    city_pdf = places_pdf.copy().drop_duplicates()
    city_pdf["city_id"] = city_pdf["city"].apply(
        lambda x: assign_unique_id(x, city_id_length)
    )
    # Get country id from 'country' table
    country_pdf = create_country_pdf(places_csv_path, country_id_length=5)
    city_pdf = city_pdf.merge(
        country_pdf, how="left", left_on="country", right_on="country_name"
    )
    city_pdf = city_pdf[["city_id", "city", "county", "country_id"]]
    return city_pdf


def create_people_pdf(people_csv_path, person_id_length=12):
    """Create a normalized dataframe for people from people.csv file.

    Args:
        people_csv_path (str): the path to people.csv (/data/people.csv)
        person_id_length (int, Defaults to 12): the length of person_id

    Returns:
        PandasDF
    """
    # Read people.csv into a Panda DF
    people_pdf = pd.read_csv(people_csv_path, encoding="utf-8")

    # Add an unique id to each record
    people_pdf["person_id_raw"] = (
        people_pdf["given_name"].astype("str")
        + people_pdf["family_name"].astype("str")
        + people_pdf["date_of_birth"].astype("str")
        + people_pdf["place_of_birth"].astype("str")
    )
    people_pdf["person_id"] = people_pdf["person_id_raw"].apply(
        lambda x: assign_unique_id(x, person_id_length)
    )
    people_pdf.drop("person_id_raw", axis=1, inplace=True)
    return people_pdf


def create_fact_table(people_pdf, city_pdf):
    """Create a fact table that has person_id, city_id and country_id.

    Args:
        people_pdf (PandasDF): the normalized pdf of the people table
        city_pdf (PandasDF): the normalized pdf of the city table

    Returns:
        PandasDF
    """
    fact_table_pdf = people_pdf.merge(
        city_pdf, how="left", left_on="place_of_birth", right_on="city"
    )
    fact_table_pdf = fact_table_pdf[["person_id", "city_id", "country_id"]]
    return fact_table_pdf
