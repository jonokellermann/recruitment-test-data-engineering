#!/usr/bin/env python
import json
import sqlalchemy
from sqlalchemy import text

from helper_funcs import create_table_object_from_sql_script, insert_df_into_table
from dataframes import (
    create_country_pdf,
    create_city_pdf,
    create_people_pdf,
    create_fact_table,
)

if __name__ == "__main__":
    # connect to the database:
    engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
    connection = engine.connect()

    metadata = sqlalchemy.schema.MetaData(engine)

    # Create 4 tables
    Country = create_table_object_from_sql_script(
        schema_sql_path="country_schema.sql",
        table_name="country",
        connection=connection,
        metadata=metadata,
        engine=engine,
    )

    City = create_table_object_from_sql_script(
        schema_sql_path="city_schema.sql",
        table_name="city",
        connection=connection,
        metadata=metadata,
        engine=engine,
    )

    People = create_table_object_from_sql_script(
        schema_sql_path="people_schema.sql",
        table_name="people",
        connection=connection,
        metadata=metadata,
        engine=engine,
    )

    Fact = create_table_object_from_sql_script(
        schema_sql_path="fact_schema.sql",
        table_name="fact",
        connection=connection,
        metadata=metadata,
        engine=engine,
    )

    country_pdf = create_country_pdf(places_csv_path="/data/places.csv")
    insert_df_into_table(
        df=country_pdf, table=Country, table_name="country", connection=connection
    )

    city_pdf = create_city_pdf(places_csv_path="/data/places.csv")
    insert_df_into_table(
        df=city_pdf, table=City, table_name="city", connection=connection
    )

    people_pdf = create_people_pdf(people_csv_path="/data/people.csv")
    insert_df_into_table(
        df=people_pdf, table=People, table_name="people", connection=connection
    )

    fact_pdf = create_fact_table(people_pdf, city_pdf)
    insert_df_into_table(
        df=fact_pdf, table=Fact, table_name="fact", connection=connection
    )

    # # output the person count per country to a JSON file
    with open("/data/summary_output.json", "w") as json_file:
        query = """
        SELECT country_name, count(distinct person_id) person_count
        FROM fact JOIN country ON fact.country_id = country.country_id
        GROUP BY country_name
        ORDER BY country_name
        """
        rows = connection.execute(text(query)).fetchall()
        result_dict = {}
        for row in rows:
            result_dict.update({row[0]: row[1]})
        json.dump(result_dict, json_file)
