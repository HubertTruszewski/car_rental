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


class Van(Car):
    def __init__(self, mark, model, registration_number, seats,
                 fuel_consumption, doors, color, price, capacity,
                 side_door, db_id=None):
        super().__init__(mark, model, registration_number, seats,
                         fuel_consumption, doors, color, price, db_id)
        self._capacity = capacity
        self._side_door = side_door
        self._type_id = 2
