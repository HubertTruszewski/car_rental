import datetime
import os
from terminaltables import AsciiTable
from modelio import get_list_of_cars, query_to_database
from errors import (NegativeCapacityError, NegativeFuelConsumptionError,
                    NegativeSeatsError, WrongCapacityTypeError,
                    WrongDbIdTypeError, NegativeDbIdError,
                    WrongSeatsTypeError,
                    WrongFuelConsumptionTypeError,
                    WrongDoorsTypeError, NegativeDoorsError,
                    WrongPriceTypeError, NegativePriceError,
                    WrongSideDoorTypeError, WrongSideDoorValueError)


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def change_to_car(element):
    if element[-1] == 0:
        auto = Car(*element[1:-5], element[0])
    elif element[-1] == 1:
        auto = PassengerCar(*element[1:11], element[0])
    else:
        auto = Van(*element[1:9], *element[11:12], element[0])
    return auto


def parameters_menu(parameters: list):
    while True:
        clear_terminal()
        if len(parameters) == 0:
            print('Brak ustawionych kryteriów\n')
        else:
            print('Zadane kryteria:')
            for position, (key, name, value) in enumerate(parameters, start=1):
                if key == 'side_door':
                    text = 'Tak' if value else 'Nie'
                elif key == 'type_id':
                    type_dict = {1: 'Osobowy', 2: 'Dostawczy', 3: 'Inny'}
                    text = type_dict[value]
                else:
                    text = value
                print(f'{position}. {name} = {text}')
            print('\n\n')

        print('1. Dodanie kryteriów\n2. Edycja kryterium')
        print('3. Usunięcie kryterium')
        print('4. Wyszukiwanie z powyższymi kryteriami')
        correct_value = False
        while not correct_value:
            answer = input('Wybór: ')
            if answer.isdigit():
                answer = int(answer)
                if answer == 1:
                    print('1. Marka\n2. Model\n3. Numer rejestracyjny')
                    print('4. Liczba miejsc')
                    print('5. Zużycie paliwa\n6. Liczba drzwi\n7. Kolor')
                    print('8. Cena\n9. Nadwozie\n10. Klasa\n11. Pojemność')
                    print('12. Boczne drzwi\n13. Typ')
                    param_choose = input('Wybór: ')
                    if param_choose.isdigit():
                        param_choose = int(param_choose)
                        if param_choose > 13:
                            print('Niepoprawna wartość, spróbuj ponownie')
                        else:
                            if param_choose == 12:
                                print('Dozwolone wartości: 0=Nie, 1=Tak')
                            if param_choose == 13:
                                print('Dozwolone wartości: 1=Osobowy, 2=Dostawczy, 3=Inny')
                            param_value = input('Wartość parametru: ')
                            if param_choose == 1:
                                parameters.append(('mark', 'Marka', param_value))
                            if param_choose == 2:
                                parameters.append(('model', 'Model', param_value))
                            if param_choose == 3:
                                parameters.append(('registration_number',
                                                   'Numer rejestracyjny',
                                                   param_value))
                            if param_choose == 4:
                                parameters.append(('seats',
                                                   'Liczba miejsc', param_value))
                            if param_choose == 5:
                                parameters.append(('fuel_consumption',
                                                   'Zużycie paliwa', param_value))
                            if param_choose == 6:
                                parameters.append(('doors', 'Drzwi', param_value))
                            if param_choose == 7:
                                parameters.append(('color', 'Kolor', param_value))
                            if param_choose == 8:
                                parameters.append(('price', 'Cena', param_value))
                            if param_choose == 9:
                                parameters.append(('body', 'Nadwozie',
                                                   param_value))
                            if param_choose == 10:
                                parameters.append(('classification', 'Klasa',
                                                   param_value))
                            if param_choose == 11:
                                parameters.append(('capacity', 'Pojemność',
                                                   param_value))
                            if param_choose == 12:
                                correct_param_value = False
                                while not correct_param_value:
                                    if param_value in {'0', '1'}:
                                        param_value = int(param_value)
                                        parameters.append(('side_door', 'Drzwi boczne',
                                                           param_value))
                                        correct_param_value = True
                                    else:
                                        print('Niepoprawna wartość, spróbuj ponownie')
                            if param_choose == 13:
                                correct_param_value = False
                                while not correct_param_value:
                                    if param_value in {'1', '2', '3'}:
                                        param_value = int(param_value)
                                        if param_value == 3:
                                            param_value = 0
                                        parameters.append(('type_id', 'Typ', param_value))
                                        correct_param_value = True
                                    else:
                                        print('Niepoprawna wartość, spróbuj ponownie')
                                        param_value = input('Wybór: ')
                        break
                    else:
                        print('Niepoprawna wartość, spróbuj ponownie')
                elif answer == 2:
                    print('Podaj numer z listy parametru do zmiany:')
                    correct_value = False
                    while not correct_value:
                        answer = input('Numer kryterium: ')
                        if answer.isdigit():
                            answer = int(answer)
                            if answer == 0:
                                break
                        else:
                            print('Niepoprawna wartość, spróbuj ponownie')
                            continue
                        value = input('Nowa wartość parametru: ')
                        try:
                            key, name = parameters[answer-1][:2]
                            parameters[answer-1] = (key, name, value)
                            correct_value = True
                        except IndexError:
                            print('Nie ma takiej pozycji na liście, spróbuj ponownie')
                    break
                elif answer == 3:
                    print('Podaj numer z listy parametru do usunięcia:')
                    correct_value = False
                    while not correct_value:
                        answer = input('Numer kryterium: ')
                        if answer.isdigit():
                            answer = int(answer)
                            if answer == 0:
                                break
                        else:
                            print('Niepoprawna wartość, spróbuj ponownie')
                        try:
                            parameters.pop(answer-1)
                            correct_value = True
                        except IndexError:
                            print('Nie ma takiej pozycji na liście, spróbuj ponownie')
                    break
                elif answer == 4:
                    return
                else:
                    print('Nieprawidłowa wartość, spróbuj ponownie')
            else:
                print('Nieprawidłowa wartość, spróbuj ponownie')
        continue


def search_car(reservation_param=[]):
    parameters = []
    while True:
        clear_terminal()
        result = get_list_of_cars(parameters, reservation_param)
        list_of_cars = []
        for element in result:
            auto = change_to_car(element)
            list_of_cars.append(auto)
        table_data = [['Lp.', 'Marka', 'Model', 'Numer\nrejestracyjny',
                       'Liczba\nmiejsc', 'Zużycie paliwa\n[L/100km]',
                       'Liczba\ndrzwi', 'Kolor', 'Cena', 'Nadwozie', 'Klasa',
                       'Pojemność\n[L]', 'Drzwi\nboczne', 'Rodzaj']]
        for position, auto in enumerate(list_of_cars, start=1):
            row = [position] + auto.represent_as_row()
            table_data.append(row)
        table = AsciiTable(table_data)
        print(table.table)
        print('Aby wybrać pojazd wpisz jego numer z tabeli.')
        print('Aby zmienić parametry wyszukiwania wpisz "P"')
        while True:
            answer = input('Wybór: ')
            answer = answer.upper()
            if answer == 'P':
                parameters_menu(parameters)
                break
            elif answer.isdigit():
                answer = int(answer)
                try:
                    if answer == 0:
                        raise IndexError(answer)
                    return list_of_cars[answer-1]
                except IndexError:
                    print('Brak samochodu o takim numerze, spróbuj ponownie')
            else:
                print('Niepoprawna wartość, spróbuj jeszcze raz')
        continue


class Car:
    def __init__(self, mark=None, model=None, registration_number=None,
                 seats=None, fuel_consumption=None, doors=None,
                 color=None, price=None, db_id=None):

        if mark:
            self.set_mark(mark)
        else:
            self._mark = None

        if model:
            self.set_model(model)
        else:
            self._model = None

        if registration_number:
            self.set_registration_number(registration_number)
        else:
            self._registration_number = None

        if seats:
            self.set_seats(seats)
        else:
            self._seats = None

        if fuel_consumption:
            self.set_fuel_consumption(fuel_consumption)
        else:
            self._fuel_consumption = None

        if doors:
            self.set_doors(doors)
        else:
            self._doors = None

        if color:
            self.set_color(color)
        else:
            self._color = None

        if price:
            self.set_price(price)
        else:
            self._price = None

        if db_id:
            self.set_db_id(db_id)
        else:
            self._db_id = None
        self._type_id = 0

    def db_id(self):
        return self._db_id

    def mark(self):
        return self._mark

    def model(self):
        return self._model

    def registration_number(self):
        return self._registration_number

    def seats(self):
        return self._seats

    def fuel_consumption(self):
        return self._fuel_consumption

    def doors(self):
        return self._doors

    def color(self):
        return self._color

    def price(self):
        return self._price

    def type_id(self):
        return self._type_id

    def set_db_id(self, db_id):
        try:
            db_id = int(db_id)
        except Exception:
            raise WrongDbIdTypeError(db_id)
        if db_id < 1:
            raise NegativeDbIdError(db_id)
        self._db_id = db_id

    def set_mark(self, mark):
        mark = mark.title()
        self._mark = mark

    def set_model(self, model):
        model = model.title()
        self._model = model

    def set_registration_number(self, registration_number):
        registration_number = registration_number.upper()
        self._registration_number = registration_number

    def set_seats(self, seats):
        try:
            seats = int(seats)
        except Exception:
            raise WrongSeatsTypeError(seats)
        if seats < 0:
            raise NegativeSeatsError(seats)
        self._seats = seats

    def set_fuel_consumption(self, fuel_consumption):
        try:
            fuel_consumption = float(fuel_consumption)
        except Exception:
            raise WrongFuelConsumptionTypeError(fuel_consumption)
        if fuel_consumption < 0:
            raise NegativeFuelConsumptionError(fuel_consumption)
        self._fuel_consumption = fuel_consumption

    def set_doors(self, doors):
        try:
            doors = int(doors)
        except Exception:
            raise WrongDoorsTypeError(doors)
        if doors < 0:
            raise NegativeDoorsError(doors)
        self._doors = doors

    def set_color(self, color):
        color = color.lower()
        self._color = color

    def set_price(self, price):
        try:
            price = float(price)
        except Exception:
            raise WrongPriceTypeError(price)
        if price < 0:
            raise NegativePriceError(price)
        self._price = price

    def insert_values(self):
        mark = input('Marka: ')
        self.set_mark(mark)
        model = input('Model: ')
        self.set_model(model)
        registration_number = input('Numer rejestracyjny: ')
        self.set_registration_number(registration_number)
        correct_value = False
        while not correct_value:
            seats = input('Liczba miejsc: ')
            try:
                self.set_seats(seats)
                correct_value = True
            except WrongSeatsTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeSeatsError:
                print('Liczba miejsc nie może być ujemna, spróbuj ponownie')

        correct_value = False
        while not correct_value:
            fuel_consumption = input('Zużycie paliwa: ')
            try:
                self.set_fuel_consumption(fuel_consumption)
                correct_value = True
            except WrongFuelConsumptionTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeFuelConsumptionError:
                print('Zużycie paliwa nie może być ujemne, spróbuj ponownie')

        correct_value = False
        while not correct_value:
            doors = input('Liczba drzwi: ')
            try:
                self.set_doors(doors)
                correct_value = True
            except WrongDoorsTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeDoorsError:
                print('Liczba drzwi nie może być ujemna')

        color = input('Kolor: ')
        self.set_color(color)

        correct_value = False
        while not correct_value:
            price = input('Cena: ')
            try:
                self.set_price(price)
                correct_value = True
            except WrongPriceTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativePriceError:
                print('Cena nie może byc ujemna, spróbuj ponownie')

    def insert_edited_values(self):
        changed_values = {}
        mark = input('Marka [{}]: '.format(self._mark))
        if mark != '':
            self.set_mark(mark)
            changed_values['mark'] = self._mark

        model = input('Model [{}]: '.format(self._model))
        if model != '':
            self.set_model(model)
            changed_values['model'] = self._model

        text = 'Numer rejestracyjny [{}]: '.format(self._registration_number)
        registration_number = input(text)
        if registration_number != '':
            self.set_registration_number(registration_number)
            changed_values['registration_number'] = registration_number

        correct_value = False
        while not correct_value:
            seats = input('Liczba miejsc [{}]: '.format(self._seats))
            if seats == '':
                break
            try:
                self.set_seats(seats)
                correct_value = True
                changed_values['seats'] = self._seats
            except WrongSeatsTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeSeatsError:
                print('Liczba miejsc nie może być ujemna, spróbuj ponownie')

        correct_value = False
        while not correct_value:
            text = 'Zużycie paliwa [{}]: '.format(self._fuel_consumption)
            fuel_consumption = input(text)
            if fuel_consumption == '':
                break
            try:
                self.set_fuel_consumption(fuel_consumption)
                correct_value = True
                changed_values['fuel_consumption'] = self._fuel_consumption
            except WrongFuelConsumptionTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeFuelConsumptionError:
                print('Zużycie paliwa nie może być ujemne, spróbuj ponownie')

        correct_value = False
        while not correct_value:
            doors = input('Liczba drzwi [{}]: '.format(self._doors))
            if doors == '':
                break
            try:
                self.set_doors(doors)
                correct_value = True
                changed_values['doors'] = self._doors
            except WrongDoorsTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeDoorsError:
                print('Liczba drzwi nie może być ujemna')

        color = input('Kolor [{}]: '.format(self._color))
        if color != '':
            self.set_color(color)
            changed_values['color'] = self._color

        correct_value = False
        while not correct_value:
            price = input('Cena [{}]: '.format(self._price))
            if price == '':
                break
            try:
                self.set_price(price)
                correct_value = True
                changed_values['price'] = self._price
            except WrongPriceTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativePriceError:
                print('Cena nie może byc ujemna, spróbuj ponownie')
        return changed_values

    def edit_values(self):
        changed_values = self.insert_edited_values()
        self.print_as_table()
        if len(changed_values) == 0:
            print('Nie zmieniono żadnych danych\nNaciśnij enter')
            input()
            return
        correct_value = False
        while not correct_value:
            answer = input('\nCzy zmienić dane na powyższe? 0=Nie, 1=Tak: ')
            if answer.isdigit():
                answer = int(answer)
                if answer in {0, 1}:
                    if answer == 0:
                        print('Anulowano zmianę danych\nNaciśnij enter')
                        input()
                        return
                    else:
                        query = self.generate_set_query(changed_values)
                        query_to_database(query)
                        correct_value = True
                        print('Zmieniono dane pojazdu\nNaciśnij enter')
                        input()
                else:
                    print('Dozwolone wartości to 0 lub 1, spróbuj ponownie')
            else:
                print('Wprowadzona wartość musi być cyfrą, spróbuj ponownie')

    def represent_as_row(self):
        row = [
            self._mark, self._model,
            self._registration_number, self._seats,
            self._fuel_consumption, self._doors,
            self._color, self._price, 'n/d',
            'n/d', 'n/d', 'n/d', 'Inny'
        ]
        return row

    def rows_to_table(self):
        rows = [
                    ['Marka', self._mark],
                    ['Model', self._model],
                    ['Numer rejestracyjny', self._registration_number],
                    ['Miejsca', self._seats],
                    ['Zużycie paliwa', self._fuel_consumption],
                    ['Drzwi', self._doors],
                    ['Kolor', self._color],
                    ['Cena', self._price]
                ]
        return rows

    def print_as_table(self):

        rows = self.rows_to_table()
        table = AsciiTable(rows, title='Dane pojazdu')
        table.inner_heading_row_border = False
        table.inner_row_border = False
        print(table.table)

    def generate_insert_query(self):
        query = 'INSERT INTO cars (mark, model, registration_number, seats, '\
                'fuel_consumption, doors, color, price, type_id) VALUES '\
                '("{}", "{}", "{}", {}, {}, {}, "{}", {}, {})'
        query = query.format(self._mark, self._model,
                             self._registration_number, self._seats,
                             self._fuel_consumption, self._doors,
                             self._color, self._price, self._type_id)
        return query

    def generate_delete_query(self):
        return f'DELETE FROM cars WHERE db_id={self._db_id}'

    def generate_set_query(self, values: dict):
        query = 'UPDATE cars SET '
        for key in values:
            value = values[key]
            query += '{}="{}", '.format(key, value)
        query = query[:-2]
        query += ' WHERE db_id={}'.format(self._db_id)
        return query

    def add_to_database(self):
        self.insert_values()
        self.print_as_table()
        correct_value = False
        while not correct_value:
            answer = input('\nCzy dodać pojazd do bazy? 0=Nie, 1=Tak: ')
            if answer.isdigit():
                answer = int(answer)
                if answer in {0, 1}:
                    if answer == 0:
                        print('Anulowano dodanie do bazy\nNaciśnij enter')
                        correct_value = True
                        input()
                        # return
                    else:
                        query = self.generate_insert_query()
                        query_to_database(query)
                        correct_value = True
                        print('Dodano samochód do bazy\nNaciśnij enter')
                        input()
                else:
                    print('Dozwolone wartości to 0 lub 1, spróbuj ponownie')
            else:
                print('Wprowadzona wartość musi być cyfrą, spróbuj ponownie')

    def delete_from_database(self):
        correct_value = False
        while not correct_value:
            answer = input('Czy usunąć ten samochód z bazy? 0=Nie, 1=Tak: ')
            if answer.isdigit():
                answer = int(answer)
                if answer == 0:
                    print('Anulowano usunięcie z bazy\nWciśnij enter')
                    input()
                    return
                elif answer == 1:
                    query = self.generate_delete_query()
                    query_to_database(query)
                    print('Usunięto samochód z bazy\nWciśnij enter')
                    input()
                    return
                else:
                    print('Niepoprawna wartość, spróbuj ponownie')
            else:
                print('Niepoprawna wartość, spróbuj ponownie')


class PassengerCar(Car):
    def __init__(self, mark=None, model=None, registration_number=None,
                 seats=None, fuel_consumption=None, doors=None, color=None,
                 price=None, body=None, classification=None, db_id=None):
        super().__init__(mark, model, registration_number, seats,
                         fuel_consumption, doors, color, price, db_id)
        if body:
            self.set_body(body)
        else:
            self._body = None
        if classification:
            self.set_classification(classification)
        else:
            self._classification = None
        self._type_id = 1

    def body(self):
        return self._body

    def classification(self):
        return self._classification

    def set_body(self, body):
        body = body.lower()
        self._body = body

    def set_classification(self, classification):
        classification = classification.upper()
        self._classification = classification

    def represent_as_row(self):
        row = [
            self._mark, self._model,
            self._registration_number, self._seats,
            self._fuel_consumption, self._doors,
            self._color, self._price, self._body,
            self._classification, 'n/d', 'n/d', 'Osobowy'
        ]
        return row

    def rows_to_table(self):
        rows = super().rows_to_table()
        rows += [
            ['Nadwozie', self._body],
            ['Klasa', self._classification]
        ]
        return rows

    def insert_edited_values(self):
        changed_values = super().insert_edited_values()

        body = input('Nadwozie [{}]: '.format(self._body))
        if body != '':
            self.set_body(body)
            changed_values['body'] = self._body

        classification = input('Klasa [{}]: '.format(self._classification))
        if classification != '':
            self.set_classification(classification)
            changed_values['classification'] = self._classification

        return changed_values

    def insert_values(self):
        super().insert_values()
        body = input('Nadwozie: ')
        self.set_body(body)
        classification = input('Klasa: ')
        self.set_classification(classification)

    def generate_insert_query(self):
        query = 'INSERT INTO cars (mark, model, registration_number, seats, '\
                'fuel_consumption, doors, color, price, body, '\
                'classification, type_id) VALUES '\
                '("{}", "{}", "{}", {}, {}, {}, "{}", {}, "{}", "{}", {})'

        query = query.format(self._mark, self._model,
                             self._registration_number,
                             self._seats, self._fuel_consumption, self._doors,
                             self._color, self._price, self._body,
                             self._classification, self._type_id)
        return query


class Van(Car):
    def __init__(self, mark=None, model=None, registration_number=None,
                 seats=None, fuel_consumption=None, doors=None,
                 color=None, price=None, capacity=None,
                 side_door=None, db_id=None):
        super().__init__(mark, model, registration_number, seats,
                         fuel_consumption, doors, color, price, db_id)
        self._capacity = capacity
        self._side_door = bool(side_door)
        self._type_id = 2

    def capacity(self):
        return self._capacity

    def side_door(self):
        return self._side_door

    def set_capacity(self, capacity):
        try:
            capacity = float(capacity)
        except Exception:
            raise WrongCapacityTypeError(capacity)
        if capacity < 0:
            raise NegativeCapacityError(capacity)
        self._capacity = capacity

    def set_side_door(self, side_door):
        try:
            side_door = int(side_door)
        except Exception:
            raise WrongSideDoorTypeError(side_door)
        if side_door not in {0, 1}:
            raise WrongSideDoorValueError(side_door)
        self._side_door = bool(side_door)

    def represent_as_row(self):
        row = [
            self._mark, self._model,
            self._registration_number, self._seats,
            self._fuel_consumption, self._doors,
            self._color, self._price, 'n/d',
            'n/d', self._capacity,
            'Tak' if self._side_door else 'Nie',
            'Dostawczy'
        ]
        return row

    def rows_to_table(self):
        rows = super().rows_to_table()
        rows += [
            ['Pojemność', self._capacity],
            ['Boczne drzwi', 'Tak' if self._side_door else 'Nie']
        ]
        return rows

    def insert_edited_values(self):
        changed_values = super().insert_edited_values()

        correct_value = False
        while not correct_value:
            capacity = input('Pojemność [{}]: '.format(self._capacity))
            if capacity == '':
                break
            try:
                self.set_capacity(capacity)
                correct_value = True
                changed_values['capacity'] = self._capacity
            except WrongCapacityTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeCapacityError:
                print('Pojemność nie może być ujemna, spróbuj ponownie')

        correct_value = False
        while not correct_value:
            word = 'Tak' if self._side_door else 'Nie'
            text = 'Czy posiada boczne drzwi? 0=Nie, 1=Tak [{}]: '.format(word)
            side_door = input(text)
            if side_door == '':
                break
            try:
                self.set_side_door(side_door)
                correct_value = True
                correct_value['side_door'] = self._side_door
            except WrongSideDoorTypeError:
                print('Wprowadzona wartość musi być liczbą 0 lub 1,'
                      ' spróbuj ponownie')
            except WrongSideDoorValueError:
                print('Wprowadzona liczba musi być 0 lub 1, spróbuj ponownie')

        return changed_values

    def insert_values(self):
        super().insert_values()
        correct_value = False
        while not correct_value:
            capacity = input('Pojemność: ')
            try:
                self.set_capacity(capacity)
                correct_value = True
            except WrongCapacityTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeCapacityError:
                print('Pojemność nie może być ujemna, spróbuj ponownie')

        correct_value = False
        while not correct_value:
            side_door = input('Czy posiada boczne drzwi? 0=Nie, 1=Tak: ')
            try:
                self.set_side_door(side_door)
                correct_value = True
            except WrongSideDoorTypeError:
                print('Wprowadzona wartość musi być liczbą 0 lub 1,'
                      ' spróbuj ponownie')
            except WrongSideDoorValueError:
                print('Wprowadzona liczba musi być 0 lub 1, spróbuj ponownie')

    def generate_insert_query(self):
        query = 'INSERT INTO cars (mark, model, registration_number, seats, '\
                'fuel_consumption, doors, color, price, capacity, side_door, '\
                'type_id) VALUES '\
                '("{}", "{}", "{}", {}, {}, {}, "{}", {}, {}, {}, {})'
        query = query.format(self._mark, self._model,
                             self._registration_number, self._seats,
                             self._fuel_consumption, self._doors,
                             self._color, self._price, self._capacity,
                             int(self._side_door), self._type_id)
        return query


class Reservation:
    def __init__(self, name=None, surname=None, startdate=None,
                 enddate=None, auto_id=None, db_id=None):
        if db_id:
            self._db_id = db_id
        else:
            self._db_id = None
        if name:
            self._name = name
        else:
            self._name = None
        if surname:
            self._surname = surname
        else:
            self._surname = None
        if startdate:
            self._startdate = startdate
        else:
            self._startdate = None
        if enddate:
            self._enddate = enddate
        else:
            self._enddate = None
        if auto_id:
            self._auto_id = auto_id
        else:
            self._auto_id = None

    def db_id(self):
        return self._db_id

    def name(self):
        return self._name

    def surname(self):
        return self._surname

    def startdate(self):
        return self._startdate

    def enddate(self):
        return self._enddate

    def auto_id(self):
        return self._auto_id

    def set_name(self, name):
        name = name.title()
        self._name = name

    def set_surname(self, surname):
        surname = surname.title()
        self._surname = surname

    def set_startdate(self, startdate):
        self._startdate = startdate

    def set_enddate(self, enddate):
        self._enddate = enddate

    def set_auto_id(self, auto_id):
        self._auto_id = auto_id

    def generate_insert_query(self):
        query = 'INSERT INTO reservations (firstname, surname, startdate, '\
                'enddate, auto_id, status) VALUES ("{}", "{}", "{}", "{}", {}, "aktywna")'
        query = query.format(self._name, self._surname, self._startdate, self._enddate,
                             self._auto_id)
        return query

    def print_as_table(self):
        table_data = [
                    ['Imię', self._name],
                    ['Nazwisko', self._surname],
                    ['Data początkowa', self._startdate],
                    ['Data końcowa', self._enddate],
                    ['Marka samochodu', self.auto.mark()],
                    ['Model', self.auto.model()],
                    ['Numer rejestracyjny', self.auto.registration_number()]
        ]
        table = AsciiTable(table_data)
        table.title = 'Dane rezerwacji'
        table.inner_heading_row_border = False
        print(table.table)

    def insert_values(self):
        name = input('Imię: ')
        self.set_name(name)
        surname = input('Nazwisko: ')
        self.set_surname(surname)
        startdate = None
        enddate = None
        correct_values = False
        while not correct_values:
            correct_date_format = False
            while not correct_date_format:
                startdate = input('Data początkowa: ')
                try:
                    startdate = datetime.date.fromisoformat(startdate)
                    correct_date_format = True
                except ValueError as e:
                    print('Niepoprawna wartość. Szczegóły: '+str(e))
                    print('Spróbuj ponownie')
            correct_date_format = False
            while not correct_date_format:
                enddate = input('Data końcowa: ')
                try:
                    enddate = datetime.date.fromisoformat(enddate)
                    correct_date_format = True
                except ValueError as e:
                    print('Niepoprawna wartość. Szczegóły: '+str(e))
                    print('Spróbuj ponownie')
            if startdate > enddate:
                print('Data końca nie może być wcześniej niż data początku. Spróbuj ponownie')
            else:
                correct_values = True
                self.set_enddate(enddate)
                self.set_startdate(startdate)
        reservation_parameters = {'startdate': self._startdate, 'enddate': self._enddate}
        auto = search_car(reservation_parameters)
        self.auto = auto
        self._auto_id = auto.db_id()

    def add_to_database(self):
        self.insert_values()
        self.print_as_table()
        print('\nCzy dodać powyższą rezerwację do bazy? 0=Nie, 1=Tak')
        correct_value = False
        while not correct_value:
            answer = input('Wybór: ')
            if answer in {'0', '1'}:
                answer = int(answer)
                correct_value = True
                if answer == 1:
                    query = self.generate_insert_query()
                    query_to_database(query)
                    print('Dodano rezerwację do bazy\nWciśnij enter')
                    input()
                else:
                    print('Anulowano dodanie do bazy\nWciśnij enter')
                    input()
            else:
                print('Niepoprawna wartość, spróbuj ponownie')
