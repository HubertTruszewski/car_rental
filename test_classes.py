import datetime
from terminaltables.ascii_table import AsciiTable
from classes import (Car, PassengerCar, Rental, Reservation, Van, change_to_car, change_to_rental, change_to_reservation,
                     print_as_table_with_title, print_table, select_from_list, input_date, input_true_or_false)
from errors import (NegativeCapacityError, NegativeFuelConsumptionError,
                    NegativeSeatsError, WrongCapacityTypeError, WrongDateType,
                    WrongDbIdTypeError, NegativeDbIdError,
                    WrongSeatsTypeError,
                    WrongFuelConsumptionTypeError,
                    WrongDoorsTypeError, NegativeDoorsError,
                    WrongPriceTypeError, NegativePriceError,
                    WrongSideDoorTypeError, WrongSideDoorValueError)
from pytest import raises
from io import StringIO


def test_input_true_or_false_zero(monkeypatch):
    input_value = StringIO('0')
    monkeypatch.setattr('sys.stdin', input_value)
    result = input_true_or_false()
    assert result is False


def test_input_true_or_false_one(monkeypatch):
    input_value = StringIO('1')
    monkeypatch.setattr('sys.stdin', input_value)
    result = input_true_or_false()
    assert result is True


def test_input_date(monkeypatch):
    input_value = StringIO('2021-02-03')
    monkeypatch.setattr('sys.stdin', input_value)
    result = input_date('Data')
    date = datetime.date(2021, 2, 3)
    assert result == date


def test_print_table():
    header = ['Lp.', 'Nazwa']
    content = [['1.', 'Volvo']]
    table_data = []
    table_data.append(header)
    table_data += content
    table = AsciiTable(table_data)
    result = print_table(header, content)
    assert result == table.table


def test_print_as_table_wiith_title():
    content = ['a', 'b', 'c', 'd']
    table = AsciiTable(content)
    table.title = 'Testowy tytuł'
    table.inner_heading_row_border = False
    result = print_as_table_with_title('Testowy tytuł', content)
    assert result == table.table


def test_select_from_list(monkeypatch):
    choose = StringIO('2')
    monkeypatch.setattr('sys.stdin', choose)
    choose_from = [1, 2, 3, 4, 5]
    result = select_from_list(choose_from)
    assert result == 2


def test_select_from_list_zero(monkeypatch):
    choose = StringIO('0')
    monkeypatch.setattr('sys.stdin', choose)
    choose_from = [1, 2, 3, 4, 5]
    result = select_from_list(choose_from)
    assert result is None


def test_change_to_car_Car():
    element = (1, 'Skoda', 'Octavia', 'WE54373', 3, 7.8, 5, 'czarny', 120, None, None,
               None, None, 0)
    result = change_to_car(element)
    assert type(result) is Car
    assert result.db_id() == 1
    assert result.registration_number() == 'WE54373'
    assert result.price() == 120


def test_change_to_car_PassengerCar():
    element = (1, 'Skoda', 'Octavia', 'WE54373', 3, 7.8, 5, 'czarny', 120, 'sedan', 'C',
               None, None, 1)
    result = change_to_car(element)
    assert type(result) is PassengerCar
    assert result.db_id() == 1
    assert result.registration_number() == 'WE54373'
    assert result.price() == 120
    assert result.classification() == 'C'
    assert result.body() == 'sedan'


def test_change_to_car_Van():
    element = (1, 'Fiat', 'Doblo', 'WZ45654', 3, 7.8, 5, 'biały', 120, None, None,
               1500, 1, 2)
    result = change_to_car(element)
    assert type(result) is Van
    assert result.db_id() == 1
    assert result.registration_number() == 'WZ45654'
    assert result.price() == 120
    assert result.capacity() == 1500
    assert result.side_door() is True


def test_change_to_reservation(monkeypatch):
    element = (3, 'Jan', 'Kowalski', datetime.date(2020, 1, 2), datetime.date(2021, 1, 5),
               5, 'aktywna')

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    result = change_to_reservation(element)
    assert type(result) is Reservation
    assert result.name() == 'Jan'
    assert result.startdate().isoformat() == '2020-01-02'
    assert result.status() == 'aktywna'
    assert result.auto_id() == 5
    assert result.auto().registration_number() == 'WE3452T'


def test_change_to_rental(monkeypatch):
    element = (1, 'Jan', 'Kowalski', datetime.date(2021, 1, 2),
               datetime.date(2021, 1, 5), datetime.date(2021, 1, 4), datetime.date(1970, 1, 1),
               5, 'wypożyczony')

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    result = change_to_rental(element)
    assert type(result) is Rental
    assert result.db_id() == 1
    assert result.surname() == 'Kowalski'
    assert result.enddate().isoformat() == '2021-01-05'
    assert result.paidtodate().isoformat() == '2021-01-04'
    assert result.returndate().isoformat() == '1970-01-01'
    assert result.status() == 'wypożyczony'
    assert result.auto_id() == result.auto().db_id()
    assert result.auto().model() == 'Superb'


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


def test_car_generate_set_query_three_changes():
    auto = Car('Skoda', 'Octavia', 'WZ3265E', 5, 7.8, 5, 'czerwony', 200, 12)
    values = {'mark': 'Opel', 'model': 'Astra', 'color': 'czarny'}
    result = auto.generate_set_query(values)
    query = 'UPDATE cars SET mark="Opel", model="Astra", color="czarny" WHERE db_id=12'
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


def test_reservation_constructor(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    reservation = Reservation('Jan', 'Kowalski', datetime.date(2020, 12, 29),
                              datetime.date(2021, 1, 1), 5, 6, 'aktywna')
    assert reservation.db_id() == 6
    assert reservation.name() == 'Jan'
    assert reservation.surname() == 'Kowalski'
    assert reservation.startdate().isoformat() == "2020-12-29"
    assert reservation.enddate().isoformat() == "2021-01-01"
    assert reservation.auto_id() == 5
    assert reservation.db_id() == 6
    assert reservation.status() == 'aktywna'


def test_reservation_empty_constructor():
    reservation = Reservation()
    assert reservation.auto_id() is None
    assert reservation.db_id() is None
    assert reservation.name() is None
    assert reservation.surname() is None
    assert reservation.startdate() is None
    assert reservation.enddate() is None
    assert reservation.db_id() is None
    assert reservation.status() is None


def test_reservation_set_db_id():
    reservation = Reservation()
    reservation.set_db_id(3)
    assert reservation.db_id() == 3


def test_reservation_set_db_id_str():
    reservation = Reservation()
    reservation.set_db_id('5')
    assert reservation.db_id() == 5


def test_reservation_set_db_id_not_number():
    reservation = Reservation()
    with raises(WrongDbIdTypeError):
        reservation.set_db_id('abc')


def test_reservaion_set_db_id_negative():
    reservation = Reservation()
    with raises(NegativeDbIdError):
        reservation.set_db_id(-6)


def test_reservation_set_name():
    reservation = Reservation()
    reservation.set_name('Jan')
    assert reservation.name() == 'Jan'


def test_reservation_set_surname():
    reservation = Reservation()
    reservation.set_surname('Kowalski')
    assert reservation.surname() == 'Kowalski'


def test_reservation_set_startdate():
    reservation = Reservation()
    reservation.set_startdate(datetime.date.fromisoformat('2021-01-01'))
    assert reservation.startdate() == datetime.date(2021, 1, 1)


def test_reservation_set_startdate_wrong():
    reservation = Reservation()
    with raises(WrongDateType):
        reservation.set_startdate('2021-01-01')


def test_reservation_set_enddate():
    reservation = Reservation()
    reservation.set_enddate(datetime.date.fromisoformat('2021-01-05'))
    assert reservation.enddate() == datetime.date(2021, 1, 5)


def test_reservation_set_enddate_wrong():
    reservation = Reservation()
    with raises(WrongDateType):
        reservation.set_enddate(2021)


def test_reservaion_set_auto_id():
    reservation = Reservation()
    reservation.set_auto_id(5)
    assert reservation.auto_id() == 5


def test_reservaion_set_auto_id_str():
    reservation = Reservation()
    reservation.set_auto_id('87')
    assert reservation.auto_id() == 87


def test_reservaion_set_auto_id_not_number():
    reservation = Reservation()
    with raises(WrongDbIdTypeError):
        reservation.set_auto_id('abc')


def test_reservaion_set_auto_id_negative():
    reservation = Reservation()
    with raises(NegativeDbIdError):
        reservation.set_auto_id(-7)


def test_reservations_generate_insert_query(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    reservation = Reservation('Jan', 'Kowalski', datetime.date(2020, 12, 29),
                              datetime.date(2021, 1, 1), 3, 1, "aktywna")
    query = 'INSERT INTO reservations (firstname, surname, startdate, enddate, auto_id, status) '\
            'VALUES ("Jan", "Kowalski", "2020-12-29", "2021-01-01", 3, "aktywna")'
    result = reservation.generate_insert_query()
    assert result == query


def test_reservation_generate_canel_query(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    reservation = Reservation('Jan', 'Kowalski', datetime.date(2020, 12, 29),
                              datetime.date(2021, 1, 1), 3, 1, "aktywna")
    result = reservation.generate_cancel_query()
    query = 'UPDATE reservations SET status="anulowana" WHERE db_id=1'
    assert result == query


def test_reservation_generate_update_query(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    reservation = Reservation('Jan', 'Kowalski', datetime.date(2020, 12, 29),
                              datetime.date(2021, 1, 1), 3, 1, "aktywna")
    changed_values = {'firstname': 'Zbigniew', 'surname': 'Nowak', 'startdate': '2020-12-30'}
    result = reservation.generate_update_query(changed_values)
    query = 'UPDATE reservations SET firstname="Zbigniew", surname="Nowak", startdate="2020-12-30" WHERE db_id=1'
    assert query == result


def test_reservation_represent_as_row(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    reservation = Reservation('Jan', 'Kowalski', datetime.date(2020, 12, 29),
                              datetime.date(2021, 1, 1), 3, 1, "aktywna")
    row = ['Jan', 'Kowalski', '2020-12-29', '2021-01-01', 'Skoda', 'Superb', 'WE3452T', 'aktywna']
    result = reservation.represent_as_row()
    assert row == result


def test_reservation_print_as_table(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    reservation = Reservation('Jan', 'Kowalski', datetime.date(2020, 12, 29),
                              datetime.date(2021, 1, 1), 3, 1, "aktywna")
    table = [
            ['Imię', 'Jan'],
            ['Nazwisko', 'Kowalski'],
            ['Data początkowa', '2020-12-29'],
            ['Data końcowa', '2021-01-01'],
            ['Marka samochodu', 'Skoda'],
            ['Model', 'Superb'],
            ['Numer rejestracyjny', 'WE3452T']
    ]
    result = reservation.print_as_table()
    assert result == table


def test_rental_constructor(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    rental = Rental('Jan', 'Kowalski', datetime.date(2020, 12, 29), datetime.date(2021, 1, 1),
                    datetime.date(2021, 1, 1), datetime.date(2021, 1, 1), 3, 'zwrócony', 8)
    assert rental.firstname() == 'Jan'
    assert rental.surname() == 'Kowalski'
    assert rental.startdate() == datetime.date(2020, 12, 29)
    assert rental.enddate() == datetime.date(2021, 1, 1)
    assert rental.paidtodate() == datetime.date(2021, 1, 1)
    assert rental.returndate() == datetime.date(2021, 1, 1)
    assert rental.auto_id() == 3
    assert rental.status() == 'zwrócony'
    assert rental.db_id() == 8


def test_rental_constructor_empty():
    rental = Rental()
    assert rental.firstname() is None
    assert rental.surname() is None
    assert rental.startdate() is None
    assert rental.enddate() is None
    assert rental.paidtodate() is None
    assert rental.returndate() is None
    assert rental.auto_id() is None
    assert rental.status() is None
    assert rental.db_id() is None


def test_rental_set_db_id():
    rental = Rental()
    rental.set_db_id(5)
    assert rental.db_id() == 5


def test_rental_set_db_id_str():
    rental = Rental()
    rental.set_db_id('9')
    assert rental.db_id() == 9


def test_rental_set_db_id_not_number():
    rental = Rental()
    with raises(WrongDbIdTypeError):
        rental.set_db_id('abc')


def test_rental_set_db_id_not_negative():
    rental = Rental()
    with raises(NegativeDbIdError):
        rental.set_db_id('-8')


def test_rental_set_start_date():
    rental = Rental()
    rental.set_startdate(datetime.date(2021, 1, 1))
    assert rental.startdate().isoformat() == '2021-01-01'


def test_rental_set_start_date_str():
    rental = Rental()
    with raises(WrongDateType):
        rental.set_startdate('2021-01-01')


def test_rental_set_end_date():
    rental = Rental()
    rental.set_enddate(datetime.date(2021, 1, 1))
    assert rental.enddate().isoformat() == '2021-01-01'


def test_rental_set_end_date_str():
    rental = Rental()
    with raises(WrongDateType):
        rental.set_enddate('2021-01-01')


def test_rental_set_paidto_date():
    rental = Rental()
    rental.set_paidtodate(datetime.date(2021, 1, 1))
    assert rental.paidtodate().isoformat() == '2021-01-01'


def test_rental_set_paidto_date_str():
    rental = Rental()
    with raises(WrongDateType):
        rental.set_paidtodate('2021-01-01')


def test_rental_set_return_date():
    rental = Rental()
    rental.set_returndate(datetime.date(2021, 1, 1))
    assert rental.returndate().isoformat() == '2021-01-01'


def test_rental_set_return_date_str():
    rental = Rental()
    with raises(WrongDateType):
        rental.set_returndate('2021-01-01')


def test_rental_set_auto_id():
    rental = Rental()
    rental.set_auto_id(5)
    assert rental.auto_id() == 5


def test_rental_set_auto_id_str():
    rental = Rental()
    rental.set_auto_id('10')
    assert rental.auto_id() == 10


def test_rental_set_auto_id_not_number():
    rental = Rental()
    with raises(WrongDbIdTypeError):
        rental.set_auto_id('abc')


def test_rental_set_auto_id_negative():
    rental = Rental()
    with raises(NegativeDbIdError):
        rental.set_auto_id(-10)


def test_rental_generate_insert_query(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    rental = Rental('Jan', 'Kowalski', datetime.date(2020, 12, 29), datetime.date(2021, 1, 1),
                    datetime.date(2021, 1, 1), datetime.date(2021, 1, 1), 3, 'zwrócony', 8)
    result = rental.generate_insert_query()
    query = 'INSERT INTO rentals (firstname, surname, startdate, enddate, paidtodate, auto_id, '\
            'status) VALUES ("Jan", "Kowalski", "2020-12-29", "2021-01-01", "2021-01-01", '\
            '"3", "zwrócony")'
    assert result == query


def test_rental_generate_return_query(monkeypatch):

    class NewDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2021, 1, 1)
    datetime.date = NewDate

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    rental = Rental('Jan', 'Kowalski', datetime.date(2020, 12, 29), datetime.date(2021, 1, 1),
                    datetime.date(2021, 1, 1), datetime.date(2021, 1, 1), 3, 'zwrócony', 8)
    result = rental.generate_return_query()
    query = 'UPDATE rentals SET status="zwrócony", returndate="2021-01-01" WHERE db_id=8'
    assert query == result


def test_rental_represent_as_row(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    rental = Rental('Jan', 'Kowalski', datetime.date(2020, 12, 29), datetime.date(2021, 1, 1),
                    datetime.date(2021, 1, 1), datetime.date(2021, 1, 1), 3, 'zwrócony', 8)
    result = rental.represent_as_row()
    row = ['Jan', 'Kowalski', '2020-12-29', '2021-01-01', '2021-01-01', '2021-01-01',
           'Skoda', 'Superb', 'WE3452T', 'zwrócony']
    assert row == result


def test_rental_print_as_table(monkeypatch):

    def return_auto(id):
        return [(id, 'Skoda', 'Superb', 'WE3452T', 5, 7.6, 5, 'czarny', 190, 'sedan', 'D+', None, None, 1)]
    monkeypatch.setattr('classes.get_car_by_id', return_auto)
    rental = Rental('Jan', 'Kowalski', datetime.date(2020, 12, 29), datetime.date(2021, 1, 1),
                    datetime.date(2021, 1, 1), datetime.date(2021, 1, 1), 3, 'zwrócony', 8)
    result = rental.print_as_table()
    table = [
        ['Imię', 'Jan'],
        ['Nazwisko', 'Kowalski'],
        ['Data początkowa', '2020-12-29'],
        ['Data końcowa', '2021-01-01'],
        ['Data opłacenia rezerwacji', '2021-01-01'],
        ['Marka', 'Skoda'],
        ['Model', 'Superb'],
        ['Numer rejestracyjny', 'WE3452T']
    ]
    assert table == result
