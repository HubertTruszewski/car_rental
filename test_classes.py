# import datetime
from classes import Car, PassengerCar, Van
from errors import (NegativeCapacityError, NegativeFuelConsumptionError,
                    NegativeSeatsError, WrongCapacityTypeError,
                    WrongDbIdTypeError, NegativeDbIdError,
                    WrongSeatsTypeError,
                    WrongFuelConsumptionTypeError,
                    WrongDoorsTypeError, NegativeDoorsError,
                    WrongPriceTypeError, NegativePriceError,
                    WrongSideDoorTypeError, WrongSideDoorValueError)
from pytest import raises


def test_create_car_without_values():
    auto = Car()
    assert auto.type_id() == 0
    assert auto.mark() is None
    assert auto.model() is None
    assert auto.registration_number() is None
    assert auto.seats() is None
    assert auto.fuel_consumption() is None
    assert auto.doors() is None
    assert auto.color() is None
    assert auto.price() is None


def test_create_car_with_values():
    auto = Car('Skoda', 'Superb', 'WM7529E', 5, 8.9, 5, 'biały', 200)
    assert auto.type_id() == 0
    assert auto.mark() == 'Skoda'
    assert auto.model() == 'Superb'
    assert auto.registration_number() == 'WM7529E'
    assert auto.seats() == 5
    assert auto.fuel_consumption() == 8.9
    assert auto.doors() == 5
    assert auto.color() == 'biały'
    assert auto.price() == 200


def test_car_set_db_id():
    auto = Car()
    auto.set_db_id(1)
    assert auto.db_id() == 1


def test_car_set_db_id_str():
    auto = Car()
    auto.set_db_id('12')
    assert auto.db_id() == 12


def test_car_set_db_id_not_number():
    auto = Car()
    with raises(WrongDbIdTypeError):
        auto.set_db_id('abc')


def test_car_set_db_id_negative_number():
    auto = Car()
    with raises(NegativeDbIdError):
        auto.set_db_id('-7')


def test_car_set_seats():
    auto = Car()
    auto.set_seats(4)
    assert auto.seats() == 4


def test_car_set_seats_str():
    auto = Car()
    auto.set_seats('5')
    assert auto.seats() == 5


def test_car_set_seats_not_number():
    auto = Car()
    with raises(WrongSeatsTypeError):
        auto.set_seats('abc')


def test_car_set_seats_negative_value():
    auto = Car()
    with raises(NegativeSeatsError):
        auto.set_seats('-9')


def test_car_set_fuel_consumption():
    auto = Car()
    auto.set_fuel_consumption(8.8)
    assert auto.fuel_consumption() == 8.8


def test_car_set_fuel_consumption_str():
    auto = Car()
    auto.set_fuel_consumption('3.9')
    assert auto.fuel_consumption() == 3.9


def test_car_set_fuel_consumption_not_number():
    auto = Car()
    with raises(WrongFuelConsumptionTypeError):
        auto.set_fuel_consumption('abc')


def test_car_set_fuel_consumption_negative():
    auto = Car()
    with raises(NegativeFuelConsumptionError):
        auto.set_fuel_consumption('-4.3')


def test_car_set_doors():
    auto = Car()
    auto.set_doors(5)
    assert auto.doors() == 5


def test_car_set_doors_str():
    auto = Car()
    auto.set_doors(3)
    assert auto.doors() == 3


def test_car_set_doors_not_number():
    auto = Car()
    with raises(WrongDoorsTypeError):
        auto.set_doors('abc')


def test_car_set_doors_negative():
    auto = Car()
    with raises(NegativeDoorsError):
        auto.set_doors('-6')


def test_car_set_price():
    auto = Car()
    auto.set_price(120)
    assert auto.price() == 120.0


def test_car_set_price_str():
    auto = Car()
    auto.set_price('123.98')
    assert auto.price() == 123.98


def test_car_set_price_not_number():
    auto = Car()
    with raises(WrongPriceTypeError):
        auto.set_price('abc')


def test_car_set_price_negative():
    auto = Car()
    with raises(NegativePriceError):
        auto.set_price('-150.98')


def test_van_set_capacity():
    auto = Van()
    auto.set_capacity(600)
    assert auto.capacity() == 600


def test_van_set_capacity_str():
    auto = Van()
    auto.set_capacity('600.9')
    assert auto.capacity() == 600.9


def test_van_set_capacity_not_number():
    auto = Van()
    with raises(WrongCapacityTypeError):
        auto.set_capacity('abc')


def test_van_set_capacity_negative():
    auto = Van()
    with raises(NegativeCapacityError):
        auto.set_capacity('-123')


def test_van_set_side_door():
    auto = Van()
    auto.set_side_door(0)
    assert auto.side_door() is False


def test_van_set_side_door_true():
    auto = Van()
    auto.set_side_door(1)
    assert auto.side_door() is True


def test_van_set_side_door_str_false():
    auto = Van()
    auto.set_side_door('0')
    assert auto.side_door() is False


def test_van_set_side_door_str_true():
    auto = Van()
    auto.set_side_door(1)
    assert auto.side_door() is True


def test_van_set_side_door_str():
    auto = Van()
    with raises(WrongSideDoorTypeError):
        auto.set_side_door('a')


def test_van_set_side_door_out_of_range():
    auto = Van()
    with raises(WrongSideDoorValueError):
        auto.set_side_door('3')


def test_car_represent_as_row():
    auto = Car('Skoda', 'Fabia', 'WE3748r', 5, 7.8, 5, 'czarny', 200)
    result = auto.represent_as_row()
    row = ['Skoda', 'Fabia', 'WE3748R', 5, 7.8, 5, 'czarny', 200,
           'n/d', 'n/d', 'n/d', 'n/d', 'Inny']
    assert result == row


def test_car_rows_to_table():
    auto = Car('Ford', 'Mondeo', 'WS2387H', 5, 9.5, 5, 'srebrny', 230)
    result = auto.rows_to_table()
    rows = [
        ['Marka', 'Ford'],
        ['Model', 'Mondeo'],
        ['Numer rejestracyjny', 'WS2387H'],
        ['Miejsca', 5],
        ['Zużycie paliwa', 9.5],
        ['Drzwi', 5],
        ['Kolor', 'srebrny'],
        ['Cena', 230]
    ]
    assert rows == result


def test_car_generate_insert_query():
    auto = Car('Skoda', 'Octavia', 'WZ3265E', 5, 7.8, 5, 'czerwony', 200.87)
    result = auto.generate_insert_query()
    query = 'INSERT INTO cars (mark, model, registration_number, seats, '\
            'fuel_consumption, doors, color, price, type_id) VALUES '\
            '("Skoda", "Octavia", "WZ3265E", 5, 7.8, 5, "czerwony", 200.87, 0)'
    assert result == query


def test_car_generate_delete_query():
    auto = Car('Skoda', 'Octavia', 'WZ3265E', 5, 7.8, 5, 'czerwony', 200, 12)
    result = auto.generate_delete_query()
    query = 'DELETE FROM cars WHERE db_id=12'
    assert result == query


def test_car_generate_set_query():
    auto = Car('Skoda', 'Octavia', 'WZ3265E', 5, 7.8, 5, 'czerwony', 200, 12)
    values = {'mark': 'Opel', 'model': 'Astra', 'seats': '7'}
    result = auto.generate_set_query(values)
    query = 'UPDATE cars SET mark="Opel", '\
            'model="Astra", seats="7" WHERE db_id=12'
    assert result == query


def test_car_generate_set_query_one_change():
    auto = Car('Skoda', 'Octavia', 'WZ3265E', 5, 7.8, 5, 'czerwony', 200, 12)
    values = {'mark': 'Opel'}
    result = auto.generate_set_query(values)
    query = 'UPDATE cars SET mark="Opel" WHERE db_id=12'
    assert result == query


def test_passengercar_represent_as_row():
    auto = PassengerCar('Nissan', 'Juke', 'We48482', 5, 9.8, 5, 'czarny',
                        200, 'hatchback', 'D')
    result = auto.represent_as_row()
    row = ['Nissan', 'Juke', 'WE48482', 5, 9.8, 5, 'czarny', 200, 'hatchback',
           'D', 'n/d', 'n/d', 'Osobowy']
    assert row == result


def test_passengercar_rows_to_table():
    auto = PassengerCar('Audi', 'a4', 'GdA45324', 5, 8.7, 3, 'niebieski',
                        200, 'sedan', 'C+')
    result = auto.rows_to_table()
    rows = [
        ['Marka', 'Audi'],
        ['Model', 'A4'],
        ['Numer rejestracyjny', 'GDA45324'],
        ['Miejsca', 5],
        ['Zużycie paliwa', 8.7],
        ['Drzwi', 3],
        ['Kolor', 'niebieski'],
        ['Cena', 200],
        ['Nadwozie', 'sedan'],
        ['Klasa', 'C+']
    ]
    print(result)
    print(rows)
    assert rows == result


def test_passengercar_generate_insert_query():
    auto = PassengerCar('Skoda', 'Karoq', 'Wx5386t', 5, 8.7, 5, 'szary',
                        220, 'SUV', 'd')
    result = auto.generate_insert_query()
    query = 'INSERT INTO cars (mark, model, registration_number, seats, '\
            'fuel_consumption, doors, color, price, body, classification, '\
            'type_id) VALUES ("Skoda", "Karoq", "WX5386T", 5, 8.7, 5, '\
            '"szary", 220.0, "suv", "D", 1)'
    assert result == query


def test_passengercar_generate_delete_query():
    auto = PassengerCar('Skoda', 'Karoq', 'Wx5386t', 5, 8.7, 5, 'szary',
                        220, 'SUV', 'D', 12)
    result = auto.generate_delete_query()
    query = 'DELETE FROM cars WHERE db_id=12'
    assert query == result


def test_van_represent_as_row():
    auto = Van('Fiat', 'Doblo', 'dw9373t', 2, 8.7, 3, 'biały',
               190, 600, True)
    result = auto.represent_as_row()
    row = ['Fiat', 'Doblo', 'DW9373T', 2, 8.7, 3, 'biały', 190,
           'n/d', 'n/d', 600, 'Tak', 'Dostawczy']
    assert row == result


def test_van_rows_to_table():
    auto = Van('Ford', 'Transit', 'WE32654', 3, 10.3, 3, 'żółty',
               250, 600, 0)
    result = auto.rows_to_table()
    rows = [
        ['Marka', 'Ford'],
        ['Model', 'Transit'],
        ['Numer rejestracyjny', 'WE32654'],
        ['Miejsca', 3],
        ['Zużycie paliwa', 10.3],
        ['Drzwi', 3],
        ['Kolor', 'żółty'],
        ['Cena', 250],
        ['Pojemność', 600],
        ['Boczne drzwi', 'Nie']
    ]
    assert result == rows


def test_van_generate_insert_query():
    auto = Van('Ford', 'Transit', 'WE32654', 3, 10.3, 3, 'żółty',
               250, 600, False)
    result = auto.generate_insert_query()
    query = 'INSERT INTO cars (mark, model, registration_number, seats, '\
            'fuel_consumption, doors, color, price, capacity, side_door, '\
            'type_id) VALUES ("Ford", "Transit", "WE32654", 3, 10.3, 3, '\
            '"żółty", 250.0, 600, 0, 2)'
    assert query == result


def test_van_generate_delete_query():
    auto = Van('Ford', 'Transit', 'WE32654', 3, 10.3, 3, 'żółty',
               250, 600, False, 15)
    result = auto.generate_delete_query()
    query = 'DELETE FROM cars WHERE db_id=15'
    assert result == query


# def test_reservation_constructor():
#     reservation = Reservation(2, 'Jan', 'Kowalski', datetime.date(2020, 12, 29),
#                               datetime.date(2021, 1, 1), 3)
#     assert reservation.db_id() == 2
#     assert reservation.name() == 'Jan'
#     assert reservation.surname() == 'Kowalski'
#     assert reservation.startdate().isoformat() == "2020-12-29"
#     assert reservation.enddate().isoformat() == "2021-01-01"
#     assert reservation.auto_id() == 3


# def test_reservations_generate_insert_query():
#     reservation = Reservation('Jan', 'Kowalski', datetime.date(2020, 12, 29),
#                               datetime.date(2021, 1, 1), 3, 1, "aktywna")
#     query = 'INSERT INTO reservations (name, surname, startdate, enddate, auto_id) '\
#             'VALUES ("Jan", "Kowalski", "2020-12-29", "2021-01-01", 3)'
#     result = reservation.generate_insert_query()
#     assert result == query
