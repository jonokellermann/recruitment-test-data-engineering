#!/usr/bin/env python
import pandas as pd
import json
import sqlalchemy
import uuid

from helper_funcs import create_table_object_from_sql_script, insert_df_into_table

if __name__ == "__main__":
    # connect to the database:
    engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
    connection = engine.connect()

    metadata = sqlalchemy.schema.MetaData(engine)

    # Create two tables: people and places
    People = create_table_object_from_sql_script(
        schema_sql_path="people_schema.sql",
        table_name="people",
        connection=connection,
        metadata=metadata,
        engine=engine,
    )

    Places = create_table_object_from_sql_script(
        schema_sql_path="places_schema.sql",
        table_name="places",
        connection=connection,
        metadata=metadata,
        engine=engine,
    )

    # read and insert the people.csv data file into the table
    people_pdf = pd.read_csv("/data/people.csv")
    # add an unique identifier column, used as a primary key
    people_pdf["id"] = [str(uuid.uuid4()) for _ in range(len(people_pdf))]
    insert_df_into_table(df=people_pdf, table=People, connection=connection)

    # read and insert the places.csv data file into the table
    places_pdf = pd.read_csv("/data/places.csv")
    insert_df_into_table(df=places_pdf, table=Places, connection=connection)

    # Get number of people by country
    joined_pdf = places_pdf.merge(
        people_pdf, how="left", left_on="city", right_on="place_of_birth"
    )
    result = joined_pdf.groupby("country").agg({"id": "nunique"}).to_dict()["id"]

    # output the table to a JSON file
    with open("/data/people_by_country.json", "w") as json_file:
        json.dump(result, json_file)
