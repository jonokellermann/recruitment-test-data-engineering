import pandas as pd
from sqlalchemy import create_engine
import json
import time

def connect_with_retries(retries=5, delay=5):
    for attempt in range(retries):
        try:
            engine = create_engine('mysql+pymysql://codetest:swordfish@database/codetest')
            connection = engine.connect()
            connection.close()
            return engine
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to the database after several attempts")

engine = connect_with_retries()

query = """
SELECT p.country, COUNT(pe.place_of_birth) as count
FROM places p
JOIN people pe ON p.city = pe.place_of_birth
GROUP BY p.country
"""

result = pd.read_sql_query(query, con=engine)

summary_output = result.to_dict(orient='records')

with open('/data/summary_output.json', 'w') as f:
    json.dump(summary_output, f, indent=4)

print("Summary output written to /data/summary_output.json")
