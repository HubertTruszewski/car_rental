import mysql.connector
import json


with open('config.txt') as file:
    config = json.load(file)


def query_to_database(query):
    my_db = mysql.connector.connect(**config)
    my_cursor = my_db.cursor()
    my_cursor.execute(query)
    my_db.commit()


def get_list_of_cars(parameters):
    my_db = mysql.connector.connect(**config)
    my_cursor = my_db.cursor()
    query = 'SELECT * FROM cars'
    if len(parameters) > 0:
        query += ' WHERE'
        for key in parameters:
            value = parameters[key]
            query += ' {}="{}" AND'.format(key, value)
        query = query[:-4]
    my_cursor.execute(query)
    myresult = my_cursor.fetchall()
    return myresult
