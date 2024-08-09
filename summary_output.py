import pandas as pd
import mysql.connector
import json


db_config = {
    'user': 'akshara',
    'password': 'ppp',
    'host': 'database',
    'database': 'test-akshara',
}


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Query to get the count of people born in each country
query_country = """
SELECT places.country, COUNT(*) AS count
FROM people
JOIN places ON people.place_of_birth = places.city
GROUP BY places.country;
"""

# Query to get the breakdown of birth years by 5-year buckets by country
query_birth_years = """
SELECT places.country, 
       FLOOR(YEAR(people.date_of_birth)/5)*5 AS birth_period, 
       COUNT(*) AS count
FROM people
JOIN places ON people.place_of_birth = places.city
GROUP BY places.country, birth_period;
"""

# Query to get the count of people by county
query_county = """
SELECT places.county, COUNT(*) AS count
FROM people
JOIN places ON people.place_of_birth = places.city
GROUP BY places.county;
"""

# Query to get the count of people by city
query_city = """
SELECT people.place_of_birth AS city, COUNT(*) AS count
FROM people
GROUP BY people.place_of_birth;
"""

# Query to get the top 10 given_names overall
query_top_given_names = """
SELECT people.given_name, COUNT(*) AS count
FROM people
GROUP BY people.given_name
ORDER BY count DESC
LIMIT 10;
"""

# Query to get the top 10 family_names overall
query_top_family_names = """
SELECT people.family_name, COUNT(*) AS count
FROM people
GROUP BY people.family_name
ORDER BY count DESC
LIMIT 10;
"""

# Query to get the top 10 given_names by country
query_top_given_names_country = """
SELECT places.country, people.given_name, COUNT(*) AS count
FROM people
JOIN places ON people.place_of_birth = places.city
GROUP BY places.country, people.given_name
ORDER BY places.country, count DESC
LIMIT 10;
"""

# Query to get the top 10 family_names by country
query_top_family_names_country = """
SELECT places.country, people.family_name, COUNT(*) AS count
FROM people
JOIN places ON people.place_of_birth = places.city
GROUP BY places.country, people.family_name
ORDER BY places.country, count DESC
LIMIT 10;
"""


cursor.execute(query_country)
country_data = cursor.fetchall()

cursor.execute(query_birth_years)
birth_years_data = cursor.fetchall()

cursor.execute(query_county)
county_data = cursor.fetchall()

cursor.execute(query_city)
city_data = cursor.fetchall()

cursor.execute(query_top_given_names)
top_given_names_data = cursor.fetchall()

cursor.execute(query_top_family_names)
top_family_names_data = cursor.fetchall()

cursor.execute(query_top_given_names_country)
top_given_names_country_data = cursor.fetchall()

cursor.execute(query_top_family_names_country)
top_family_names_country_data = cursor.fetchall()


summary = {
    "country_summary": {row[0]: row[1] for row in country_data},
    "birth_years_summary": {},
    "county_summary": {row[0]: row[1] for row in county_data},
    "city_summary": {row[0]: row[1] for row in city_data},
    "top_given_names": {row[0]: row[1] for row in top_given_names_data},
    "top_family_names": {row[0]: row[1] for row in top_family_names_data},
    "top_given_names_by_country": {},
    "top_family_names_by_country": {},
}

# Aggregate birth years summary
for row in birth_years_data:
    country = row[0]
    period = f"{row[1]}-{row[1]+4}"
    if country not in summary["birth_years_summary"]:
        summary["birth_years_summary"][country] = {}
    summary["birth_years_summary"][country][period] = row[2]

# Aggregate top given names by country
for row in top_given_names_country_data:
    country = row[0]
    name = row[1]
    count = row[2]
    if country not in summary["top_given_names_by_country"]:
        summary["top_given_names_by_country"][country] = []
    summary["top_given_names_by_country"][country].append({"name": name, "count": count})

# Aggregate top family names by country
for row in top_family_names_country_data:
    country = row[0]
    name = row[1]
    count = row[2]
    if country not in summary["top_family_names_by_country"]:
        summary["top_family_names_by_country"][country] = []
    summary["top_family_names_by_country"][country].append({"name": name, "count": count})


with open('/data/summary_output.json', 'w') as f:
    json.dump(summary, f, indent=4)

print("Summary written to /data/summary_output.json")


cursor.close()
connection.close()
