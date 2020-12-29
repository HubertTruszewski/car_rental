from modelio import insert_to_database


class NegativeSeatsError(ValueError):
    pass


class WrongSeatsType(TypeError):
    pass


class NegativeFuelConsumptionError(ValueError):
    pass


class NegativeDoorsError(ValueError):
    pass


class NegativePriceError(ValueError):
    pass


class WrongPriceType(TypeError):
    pass


class NegativeCapacityError(ValueError):
    pass


class WrongCapacityType(TypeError):
    pass


class Car:
    def __init__(self, mark=None, model=None, registration_number=None,
                 seats=None, fuel_consumption=None, doors=None,
                 color=None, price=None, db_id=None):
        self._db_id = db_id
        self._mark = mark
        self._model = model
        self._registration_number = registration_number
        self._seats = seats
        self._fuel_consumption = fuel_consumption
        self._doors = doors
        self._color = color
        self._price = price
        self._type_id = 0

    def db_id(self):
        return self._db_id

    def mark(self):
        return self._mark

    def model(self):
        return self._model

    def registration_number(self):
        return self._registration_number

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
        self._db_id = db_id

    def set_mark(self, mark):
        self._mark = mark

    def set_model(self, model):
        self._model = model

    def set_registration_number(self, registration_number):
        self._registration_number = registration_number

    def set_seats(self, seats):
        self._seats = seats

    def set_fuel_consumption(self, fuel_consumption):
        self._fuel_consumption = fuel_consumption

    def set_doors(self, doors):
        self._doors = doors

    def set_color(self, color):
        self._color = color

    def set_price(self, price):
        self._price = price

    def add_to_database(self):
        query = 'INSERT INTO cars (mark, model, registration_number, seats, '
        query += 'fuel_consumption, doors, color, price, type_id) VALUES '
        query += '("{}", "{}", "{}", {}, {}, {}, "{}", {}, {})'
        query = query.format(self._mark, self._model,
                             self._registration_number, self._seats,
                             self._fuel_consumption, self._doors,
                             self._color, self._price, self._type_id)
        print(query)
        insert_to_database(query)


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
        self._capacity = capacity

    def set_side_door(self, side_door):
        self._side_door = bool(side_door)

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
