class Car:
    def __init__(self, mark, model, registration_number,
                 seats, fuel_consumption, doors, color, price, db_id=None):
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


class PassengerCar(Car):
    def __init__(self, mark, model, registration_number, seats,
                 fuel_consumption, doors, color, price,
                 body, classification, isofix, db_id=None):
        super().__init__(mark, model, registration_number, seats,
                         fuel_consumption, doors, color, price, db_id)
        self._body = body
        self._classification = classification
        self._isofix = bool(isofix)
        self._type_id = 1

    def body(self):
        return self._body

    def classification(self):
        return self._classification

    def isofix(self):
        return self._isofix


class Van(Car):
    def __init__(self, mark, model, registration_number, seats,
                 fuel_consumption, doors, color, price, capacity,
                 side_door, db_id=None):
        super().__init__(mark, model, registration_number, seats,
                         fuel_consumption, doors, color, price, db_id)
        self._capacity = capacity
        self._side_door = bool(side_door)
        self._type_id = 2

    def capacity(self):
        return self._capacity

    def side_door(self):
        return self._side_door
