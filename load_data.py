#!/usr/bin/env python
import pandas as pd
import mysql.connector


db_config = {
    'user': 'akshara',
    'password': 'ppp',
    'host': 'database',
    'database': 'test-akshara',
}


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()


def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INT AUTO_INCREMENT PRIMARY KEY,
            given_name VARCHAR(255),
            family_name VARCHAR(255),
            date_of_birth DATE,
            place_of_birth VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS places (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city VARCHAR(255),
            county VARCHAR(255),
            country VARCHAR(255)
        )
    """)


create_tables()


people_df = pd.read_csv('/data/people.csv')
places_df = pd.read_csv('/data/places.csv')


for index, row in people_df.iterrows():
    cursor.execute(
        "INSERT INTO people (given_name, family_name, date_of_birth, place_of_birth) VALUES (%s, %s, %s, %s)",
        (row['given_name'], row['family_name'], row['date_of_birth'], row['place_of_birth'])
    )


for index, row in places_df.iterrows():
    cursor.execute(
        "INSERT INTO places (city, county, country) VALUES (%s, %s, %s)",
        (row['city'], row['county'], row['country'])
    )


connection.commit()
cursor.close()
connection.close()

print("Data loaded successfully into MySQL database.")
