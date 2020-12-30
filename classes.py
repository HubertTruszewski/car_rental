from terminaltables import AsciiTable
from modelio import insert_to_database
from errors import (NegativeCapacityError, NegativeFuelConsumptionError,
                    NegativeSeatsError, WrongCapacityTypeError,
                    WrongDbIdTypeError, NegativeDbIdError,
                    WrongSeatsTypeError,
                    WrongFuelConsumptionTypeError,
                    WrongDoorsTypeError, NegativeDoorsError,
                    WrongPriceTypeError, NegativePriceError,
                    WrongSideDoorTypeError, WrongSideDoorValueError)


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
            print(db_id)
            db_id = int(db_id)
        except Exception:
            raise WrongDbIdTypeError(db_id)
        if db_id < 1:
            raise NegativeDbIdError(db_id)
        self._db_id = db_id

    def set_mark(self, mark):
        self._mark = mark

    def set_model(self, model):
        self._model = model

    def set_registration_number(self, registration_number):
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
        mark = mark.title()
        self.set_mark(mark)
        model = input('Model: ')
        model = model.title()
        self.set_model(model)
        registration_number = input('Numer rejestracyjny: ')
        registration_number = registration_number.upper()
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
            doors = input('Liczba miejsc: ')
            try:
                self.set_doors(doors)
                correct_value = True
            except WrongDoorsTypeError:
                print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
            except NegativeDoorsError:
                print('Liczba drzwi nie może być ujemna')

        color = input('Kolor: ')
        color = color.lower()
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
                        input()
                        return
                    else:
                        query = self.generate_insert_query()
                        insert_to_database(query)
                        correct_value = True
                        print('Dodano samochód do bazy\nNaciśnij enter')
                        input()
                else:
                    print('Dozwolone wartości to 0 lub 1, spróbuj ponownie')
            else:
                print('Wprowadzona wartość musi być cyfrą, spróbuj ponownie')


class PassengerCar(Car):
    def __init__(self, mark=None, model=None, registration_number=None,
                 seats=None, fuel_consumption=None, doors=None, color=None,
                 price=None, body=None, classification=None, db_id=None):
        super().__init__(mark, model, registration_number, seats,
                         fuel_consumption, doors, color, price, db_id)
        self._body = body
        self._classification = classification
        self._type_id = 1

    def body(self):
        return self._body

    def classification(self):
        return self._classification

    def set_body(self, body):
        self._body = body

    def set_classification(self, classification):
        self._classification = classification

    def insert_values(self):
        super().insert_values()
        body = input('Nadwozie: ')
        self.set_body(body)
        classification = input('Klasa: ')
        self.set_classification(classification)

    def add_to_database(self):
        query = 'INSERT INTO cars (mark, model, registration_number, seats, '
        query += 'fuel_consumption, doors, color, price, '
        query += 'body, classification, type_id) VALUES '
        query += '("{}", "{}", "{}", {}, {}, {}, "{}", {}, "{}", "{}", {})'
        query = query.format(self._mark, self._model,
                             self._registration_number, self._seats,
                             self._fuel_consumption, self._doors,
                             self._color, self._price, self._body,
                             self._classification, self._type_id)
        print(query)
        insert_to_database(query)


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

    def add_to_database(self):
        query = 'INSERT INTO cars (mark, model, registration_number, seats, '
        query += 'fuel_consumption, doors, color, price, '
        query += 'capacity, side_door, type_id) VALUES '
        query += '("{}", "{}", "{}", {}, {}, {}, "{}", {}, "{}", "{}", {})'
        query = query.format(self._mark, self._model,
                             self._registration_number, self._seats,
                             self._fuel_consumption, self._doors,
                             self._color, self._price, self._capacity,
                             int(self._side_door), self._type_id)
        print(query)
        insert_to_database(query)
