import os
from errors import WrongConfigFileFormatError
import mysql.connector
import json


def clear_terminal():
    """Clears the terminal with proper command"""
    os.system('cls' if os.name == 'nt' else 'clear')


def setup_config_file():
    """Create config file if not exist or is incorrect"""
    config = dict()
    host = input('Adres serwera: ')
    username = input('Nazwa użytkownika: ')
    password = input('Hasło: ')
    database = input('Nazwa bazy danych: ')
    config['host'] = host
    config['username'] = username
    config['password'] = password
    config['database'] = database
    file = open('config.txt', 'w')
    json.dump(config, file, indent=4)
    file.close()
    return config


try:
    file = open('config.txt', 'r')
    config = json.load(file)
    file.close()
    if len(config) != 4:
        raise WrongConfigFileFormatError
except FileNotFoundError:
    clear_terminal()
    print('Nie znaleziono pliku konfiguracyjnego.')
    print('Utworzyć teraz? 0=Nie, 1=Tak')
    correct_answer = False
    while not correct_answer:
        answer = input('Wybór: ')
        if answer == '0':
            print('Program nie może działać bez konfiguracji i \
                  zakończy działanie.')
            print('Wciśnij enter')
            input()
            exit()
        elif answer == '1':
            config = setup_config_file()
            correct_answer = True
        else:
            print('Niepoprawny wybór, spróbuj ponownie')
except WrongConfigFileFormatError:
    clear_terminal()
    print('Nieprawidłowy format pliku konfiguracyjnego.')
    print('Utworzyć nowy? 0=Nie, 1=Tak')
    correct_answer = False
    while not correct_answer:
        answer = input('Wybór: ')
        if answer == '0':
            print('Program nie może działać bez konfiguracji '
                  'i zakończy działanie.')
            print('Wciśnij enter')
            input()
            exit()
        elif answer == '1':
            config = setup_config_file()
            correct_answer = True
        else:
            print('Niepoprawny wybór, spróbuj ponownie')
except Exception as e:
    print('Problem z dostępem do konfiguracji! Szczegóły: '+str(e))
    print('Program zakończy działanie\nWciśnij enter')
    input()
    exit()


def my_db_cursor():
    """Connect to database and return a tuple:
    (database_object, cursor_object)"""
    my_db = None
    my_cursor = None
    try:
        my_db = mysql.connector.connect(**config)
        my_cursor = my_db.cursor()
    except mysql.connector.Error as e:
        print('Błąd połączenia z bazą danych! Szczegóły: ' + str(e))
        print('nProgram zakończy działanie\nWciśnij enter')
        input()
        exit()
    return my_db, my_cursor


def query_to_database(query):
    """Send query to database which needs to be commited"""
    my_db, my_cursor = my_db_cursor()
    my_cursor.execute(query)
    my_db.commit()


def get_list_of_cars(parameters, reservation_param):
    """"Return a list of tuples with cars data with specified parameters"""
    my_db, my_cursor = my_db_cursor()
    if len(reservation_param) > 0:
        query = 'SELECT c.db_id, c.mark, c.model, '\
                'c.registration_number, c.seats, '\
                'c.fuel_consumption, c.doors, c.color, c.price, '\
                'c.body, c.classification, '\
                'c.capacity, c.side_door, c.type_id FROM cars as c '\
                'WHERE c.db_id not in (SELECT r.auto_id from '\
                'reservations as r where r.status!="anulowana" AND'\
                '((r.startdate BETWEEN "{startdate}" '\
                'AND "{enddate}") OR (r.enddate BETWEEN "{startdate}" AND'\
                '"{enddate}") OR '\
                '(r.startdate <= "{startdate}" AND r.enddate >= '\
                '"{enddate}"))) and c.db_id NOT IN '\
                '(SELECT re.auto_id from rentals as re where '\
                '(re.startdate BETWEEN "{startdate}" '\
                'AND "{enddate}") OR (re.enddate BETWEEN '\
                '"{startdate}" AND "{enddate}") OR '\
                '(re.startdate <= "{startdate}" '\
                'AND re.enddate >= "{enddate}"))'
        query = query.format(**reservation_param)
    else:
        query = 'SELECT * FROM cars as c'
    if len(parameters) and not len(reservation_param):
        query += ' WHERE'
    if len(parameters) and len(reservation_param):
        query += ' AND'
    if len(parameters):
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
    """Returns a list with tuples with reservations data specified by data"""
    my_db, my_cursor = my_db_cursor()
    query = 'SELECT r.db_id, r.firstname, r.surname, '\
            'r.startdate, r.enddate, r.auto_id, r.status '\
            'FROM reservations as r WHERE r.startdate="{}"'.format(data)
    my_cursor.execute(query)
    myresult = my_cursor.fetchall()
    return myresult


def get_list_of_rentals():
    """Returns a list of tuples with rentals data"""
    my_db, my_cursor = my_db_cursor()
    query = 'SELECT * FROM rentals WHERE status="wypożyczony"'
    my_cursor.execute(query)
    myresult = my_cursor.fetchall()
    return myresult


def get_car_by_id(id):
    """Returns a list of one tuple with car data specified by its db_id"""
    my_db, my_cursor = my_db_cursor()
    query = 'SELECT * FROM cars WHERE db_id={}'.format(id)
    my_cursor.execute(query)
    myresult = my_cursor.fetchall()
    return myresult


def get_list_of_id_free_cars(reservation_param):
    """Returns a list of tuples with cars data
    which are free in specified dates"""
    my_db, my_cursor = my_db_cursor()
    query = 'SELECT c.db_id, c.mark, c.model, c.registration_number, '\
            'c.seats, c.fuel_consumption, c.doors, c.color, '\
            'c.price, c.body, c.classification, '\
            'c.capacity, c.side_door, c.type_id FROM cars as c '\
            'WHERE c.db_id not in (SELECT r.auto_id from '\
            'reservations as r where r.status!="anulowana" '\
            'AND r.db_id!={res_id} AND ((r.startdate BETWEEN "{startdate}" '\
            'AND "{enddate}") OR (r.enddate BETWEEN "{startdate}" AND'\
            '"{enddate}") OR '\
            '(r.startdate <= "{startdate}" AND r.enddate >= "{enddate}"))) '\
            'and c.db_id NOT IN '\
            '(SELECT re.auto_id from rentals as re where '\
            '(re.startdate BETWEEN "{startdate}" '\
            'AND "{enddate}") OR (re.enddate BETWEEN "{startdate}" '\
            'AND "{enddate}") OR '\
            '(re.startdate <= "{startdate}" AND re.enddate >= "{enddate}"))'
    query = query.format(**reservation_param)
    my_cursor.execute(query)
    results = my_cursor.fetchall()
    list_of_id = [int(id[0]) for id in results]
    return list_of_id


def get_list_not_paid_rentals(date):
    """Returns a list of tuples with rentals data
    which paidtodate is before specified date"""
    my_db, my_cursor = my_db_cursor()
    query = f'SELECT * FROM rentals WHERE "{date}">paidtodate '\
            'AND status="wypożyczony"'
    my_cursor.execute(query)
    results = my_cursor.fetchall()
    return results
