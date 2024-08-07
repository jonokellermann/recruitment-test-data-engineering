import pandas as pd
from sqlalchemy import create_engine
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

places = pd.read_csv('/data/places.csv')
people = pd.read_csv('/data/people.csv')

places.to_sql('places', con=engine, index=False, if_exists='append')
people.to_sql('people', con=engine, index=False, if_exists='append')
