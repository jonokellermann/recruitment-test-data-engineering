#!/usr/bin/envpython

import csv
import json
import sqlalchemy

# connect to the database
engine = sqlalchemy.create_engine(os.getenv('MYSQL_CONNECTION_STRING'))
connection = engine.connect()

metadata = sqlalchemy.schema.MetaData(engine)

# output the table to a JSON file
with engine.connect() as connection:
  query = "SELECT plc.city, count(ppl.given_name) FROM codetest.places plc LEFT JOIN codetest.people ppl ON plc.city = ppl.place_of_birth GROUP BY plc.city;"
  results = connection.execute(query)
  
with open("/data/summary_output.json", "w") as json_file:
  rows = {result[0] : result[1] for result in results}
  print(rows)
  json.dump(rows, json_file)