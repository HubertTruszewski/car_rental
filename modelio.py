import mysql.connector
import json

with open('config.txt') as file:
    config = json.load(file)


def insert_to_database(query):
    my_db = mysql.connector.connect(**config)
    my_cursor = my_db.cursor()
    my_cursor.execute(query)
    my_db.commit()
