import csv
import mysql.connector


connection = mysql.connector.connect(
    host='database',
    user='akshara',
    password='ppp',  
    database='test-akshara'    
)

cursor = connection.cursor()


with open('/Users/aksharadesai/Desktop/data-engineering-akshara/data/people.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  
    for row in csv_reader:
        
        if len(row) == 4:
            cursor.execute(
                "INSERT INTO people (first_name, last_name, date_of_birth, city_of_birth) VALUES (%s, %s, %s, %s)",
                (row[0], row[1], row[2], row[3])
            )
        else:
            print(f"Skipping row with unexpected number of columns: {row}")


connection.commit()


cursor.close()
connection.close()

print("Data inserted successfully")
