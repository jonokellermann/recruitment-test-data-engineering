
# DROP TABLES
people_table_drop = "DROP TABLE IF EXISTS people; "
places_table_drop =  "DROP TABLE IF EXISTS places; "

# CREATE TABLES
staging_people_table_create= ("""
    CREATE TEMPORARY TABLE IF NOT EXISTS people (
      id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
      given_name VARCHAR (50),
      family_name VARCHAR (50),
      date_of_birth DATE,
      place_of_birth VARCHAR (125),
      INDEX (place_of_birth)
    );
""")

staging_places_table_create = ("""
    CREATE TEMPORARY TABLE IF NOT EXISTS places (
      id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
      city VARCHAR (50),
      county VARCHAR (50),
      country VARCHAR (50),
      INDEX (city, country)
    );
""")

population_query = ("""
  SELECT
      pl.country as country,
      COUNT(p.given_name) as population
  FROM 
      (SELECT DISTINCT city, county, country FROM places) AS  pl
      LEFT JOIN (SELECT DISTINCT given_name,family_name,date_of_birth,place_of_birth FROM people) AS  p ON pl.city = p.place_of_birth
  GROUP BY pl.country
""")

# QUERY LISTS
create_table_queries = [staging_people_table_create, staging_places_table_create]
drop_table_queries = [people_table_drop, places_table_drop]