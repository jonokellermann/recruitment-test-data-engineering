import csv
import mysql.connector


connection = mysql.connector.connect(
    host='database',
    user='akshara',
    password='ppp',  
    database='test-akshara'  
)

cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS places (
    city VARCHAR(255),
    county VARCHAR(255),
    country VARCHAR(255)
)
""")


with open('/Users/aksharadesai/Desktop/data-engineering-akshara/data/places.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  
    for row in csv_reader:
        print(row)  
        cursor.execute(
            "INSERT INTO places (city, county, country) VALUES (%s, %s, %s)",
            (row[0], row[1], row[2])
        )


connection.commit()


cursor.close()
connection.close()

print("Data inserted successfully into places table")
