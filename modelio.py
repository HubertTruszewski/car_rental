import mysql.connector
import json


with open('config.txt') as file:
    config = json.load(file)


def query_to_database(query):
    my_db = mysql.connector.connect(**config)
    my_cursor = my_db.cursor()
    my_cursor.execute(query)
    my_db.commit()


def get_list_of_cars(parameters, reservation_param):
    my_db = mysql.connector.connect(**config)
    my_cursor = my_db.cursor()
    if len(reservation_param) > 0:
        query = 'SELECT c.db_id, c.mark, c.model, c.registration_number, c.seats, '\
                'c.fuel_consumption, c.doors, c.color, c.price, c.body, c.classification, '\
                'c.capacity, c.side_door, c.type_id FROM cars as c '\
                'WHERE c.db_id not in (SELECT r.auto_id from '\
                'reservations as r where (r.startdate BETWEEN "{startdate}" '\
                'AND "{enddate}") OR (r.enddate BETWEEN "{startdate}" AND "{enddate}") OR '\
                '(r.startdate <= "{startdate}" AND r.enddate >= "{enddate}")) and c.db_id NOT IN '\
                '(SELECT re.auto_id from rentals as re where (re.startdate BETWEEN "{startdate}" '\
                'AND "{enddate}") OR (re.enddate BETWEEN "{startdate}" AND "{enddate}") OR '\
                '(re.startdate <= "{startdate}" AND re.enddate >= "{enddate}"))'
        query = query.format(**reservation_param)
    else:
        query = 'SELECT * FROM cars as c'
    if len(parameters):
        query += ' WHERE'
        for key, _, value in parameters:
            if type(value) is str:
                query += ' c.{}="{}" AND'.format(key, value)
            else:
                query += ' c.{}={} AND'.format(key, value)
        query = query[:-4]
    my_cursor.execute(query)
    myresult = my_cursor.fetchall()
    return myresult


def get_list_of_reservations(data):
    my_db = mysql.connector.connect(**config)
    my_cursor = my_db.cursor()
    query = 'SELECT r.db_id, r.firstname, r.surname, r.startdate, r.enddate, r.auto_id, '\
            'r.status FROM reservations as r WHERE r.startdate="{}"'.format(data)
    my_cursor.execute(query)
    myresult = my_cursor.fetchall()
    return myresult


def get_car_by_id(id):
    my_db = mysql.connector.connect(**config)
    my_cursor = my_db.cursor()
    query = 'SELECT * FROM cars WHERE db_id={}'.format(id)
    my_cursor.execute(query)
    myresult = my_cursor.fetchall()
    return myresult


def get_list_of_id_free_cars(reservation_param):
    my_db = mysql.connector.connect(**config)
    my_cursor = my_db.cursor()

    query = 'SELECT c.db_id, c.mark, c.model, c.registration_number, c.seats, '\
            'c.fuel_consumption, c.doors, c.color, c.price, c.body, c.classification, '\
            'c.capacity, c.side_door, c.type_id FROM cars as c '\
            'WHERE c.db_id not in (SELECT r.auto_id from '\
            'reservations as r where r.db_id!={res_id} AND ((r.startdate BETWEEN "{startdate}" '\
            'AND "{enddate}") OR (r.enddate BETWEEN "{startdate}" AND "{enddate}") OR '\
            '(r.startdate <= "{startdate}" AND r.enddate >= "{enddate}"))) and c.db_id NOT IN '\
            '(SELECT re.auto_id from rentals as re where (re.startdate BETWEEN "{startdate}" '\
            'AND "{enddate}") OR (re.enddate BETWEEN "{startdate}" AND "{enddate}") OR '\
            '(re.startdate <= "{startdate}" AND re.enddate >= "{enddate}"))'
    query = query.format(**reservation_param)
    my_cursor.execute(query)
    results = my_cursor.fetchall()
    list_of_id = [int(id[0]) for id in results]
    return list_of_id
