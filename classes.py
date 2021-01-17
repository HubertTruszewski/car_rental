import datetime
from terminaltables import AsciiTable
from modelio import get_car_by_id, get_list_not_paid_rentals, get_list_of_cars
from modelio import query_to_database, get_list_of_reservations, clear_terminal
from modelio import get_list_of_id_free_cars, get_list_of_rentals
from errors import (NegativeCapacityError, NegativeFuelConsumptionError,
                    NegativeSeatsError, WrongCapacityTypeError, WrongDateType,
                    WrongDbIdTypeError, NegativeDbIdError,
                    WrongSeatsTypeError,
                    WrongFuelConsumptionTypeError,
                    WrongDoorsTypeError, NegativeDoorsError,
                    WrongPriceTypeError, NegativePriceError,
                    WrongSideDoorTypeError, WrongSideDoorValueError)


def input_true_or_false():
    """Asks user for answer where 0=False, 1=True and returns answer as bool"""
    correct_value = False
    while not correct_value:
        answer = input('Wybór: ')
        if answer == '0':
            return False
        elif answer == '1':
            return True
        else:
            print('Niepoprawny wybór, spróbuj ponownie!')


def input_date(input_text, empty=False, defaultdate=None):
    """Asks user to input a correct date in isoformat and returns this value"""
    correct_value = False
    date = None
    while not correct_value:
        date = input(input_text)
        if empty and date == '':
            return defaultdate
        try:
            date = datetime.date.fromisoformat(date)
            correct_value = True
        except ValueError as e:
            print('Niepoprawna wartość. Szczegóły: '+str(e))
            print('Spróbuj ponownie')
    return date


def input_start_and_end_date(start_date_text, end_date_text,
                             empty=False, defaultstartdate=None,
                             defaultenddate=None):
    """Ask user to input two dates in isoformat
    and returns values if startdate is before enddate"""
    correct_dates = False
    startdate = None
    enddate = None
    while not correct_dates:
        startdate = input_date(start_date_text, empty, defaultstartdate)
        enddate = input_date(end_date_text, empty, defaultenddate)
        if startdate > enddate:
            print('Data końcowa nie może być wcześniej niż początkowa.')
            print('Spróbuj ponownie')
        else:
            correct_dates = True
    return startdate, enddate


def print_table(header, content):
    """Returns a table with given data"""
    table_data = []
    table_data.append(header)
    table_data += content
    table = AsciiTable(table_data)
    return table.table


def print_as_table_with_title(title, content):
    """Returns a table with given data and title"""
    table = AsciiTable(content)
    table.title = title
    table.inner_heading_row_border = False
    return table.table


def select_from_list(list):
    """Asks user to choose option from given list
    and returns value from this position"""
    correct_value = False
    while not correct_value:
        answer = input('Wybór: ')
        if answer.isdigit():
            answer = int(answer)
            if answer == 0:
                return
            try:
                value_to_return = list[answer-1]
                correct_value = True
                return value_to_return
            except IndexError:
                print('Nie ma takiej pozycji na liscie, spróbuj ponownie')
        else:
            print('Niepoprawna wartość, spróbuj ponownie')


def change_to_car(element):
    """Changes given tuple to proper type of car and returns this object"""
    if element[-1] == 0:
        auto = Car(*element[1:9], element[0])
    elif element[-1] == 1:
        auto = PassengerCar(*element[1:11], element[0])
    else:
        auto = Van(*element[1:9], *element[11:13], element[0])
    return auto


def change_to_reservation(element):
    """Returns a Reservation class object made from given tuple"""
    reservation = Reservation(*element[1:6], element[0], element[6])
    return reservation


def change_to_rental(element):
    """Returns a Rental class object made from given tuple"""
    rental = Rental(*element[1:9], element[0])
    return rental


def parameters_menu(parameters):
    """Parameters menu for auto where user can add,
    edit and delete parameters to search"""
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
                    type_dict = {1: 'Osobowy', 2: 'Dostawczy', 0: 'Inny'}
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
                                print('Dozwolone wartości: 1=Osobowy, \
                                      2=Dostawczy, 3=Inny')
                            param_value = input('Wartość parametru: ')
                            if param_choose == 1:
                                parameters.append(('mark', 'Marka',
                                                   param_value))
                            if param_choose == 2:
                                parameters.append(('model', 'Model',
                                                   param_value))
                            if param_choose == 3:
                                parameters.append(('registration_number',
                                                   'Numer rejestracyjny',
                                                   param_value))
                            if param_choose == 4:
                                parameters.append(('seats',
                                                   'Liczba miejsc',
                                                   param_value))
                            if param_choose == 5:
                                parameters.append(('fuel_consumption',
                                                   'Zużycie paliwa',
                                                   param_value))
                            if param_choose == 6:
                                parameters.append(('doors', 'Drzwi',
                                                   param_value))
                            if param_choose == 7:
                                parameters.append(('color', 'Kolor',
                                                   param_value))
                            if param_choose == 8:
                                parameters.append(('price', 'Cena',
                                                   param_value))
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
                                        parameters.append(('side_door',
                                                           'Drzwi boczne',
                                                           param_value))
                                        correct_param_value = True
                                    else:
                                        print('Niepoprawna wartość, \
                                              spróbuj ponownie')
                            if param_choose == 13:
                                correct_param_value = False
                                while not correct_param_value:
                                    if param_value in {'1', '2', '3'}:
                                        param_value = int(param_value)
                                        if param_value == 3:
                                            param_value = 0
                                        parameters.append(('type_id', 'Typ',
                                                           param_value))
                                        correct_param_value = True
                                    else:
                                        print('Niepoprawna wartość, \
                                              spróbuj ponownie')
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
                            print('Nie ma takiej pozycji na liście, \
                                  spróbuj ponownie')
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
                            print('Nie ma takiej pozycji na liście, \
                                  spróbuj ponownie')
                    break
                elif answer == 4:
                    return
                else:
                    print('Nieprawidłowa wartość, spróbuj ponownie')
            else:
                print('Nieprawidłowa wartość, spróbuj ponownie')


def search_car(reservation_param=[]):
    """Displays a table with cars, ask user to choose one
    and returns choosen object"""
    parameters = []
    while True:
        clear_terminal()
        result = get_list_of_cars(parameters, reservation_param)
        list_of_cars = []
        for element in result:
            auto = change_to_car(element)
            list_of_cars.append(auto)
        header = ['Lp.', 'Marka', 'Model', 'Numer\nrejestracyjny',
                  'Liczba\nmiejsc', 'Zużycie paliwa\n[L/100km]',
                  'Liczba\ndrzwi', 'Kolor', 'Cena', 'Nadwozie', 'Klasa',
                  'Pojemność\n[L]', 'Drzwi\nboczne', 'Rodzaj']
        content = []
        for position, auto in enumerate(list_of_cars, start=1):
            content.append([position] + auto.represent_as_row())
        print(print_table(header, content))
        print('Aby wybrać pojazd wpisz jego numer z tabeli.')
        print('Aby zmienić parametry wyszukiwania wpisz "P". Powrót: wpisz 0')
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
                        return
                    return list_of_cars[answer-1]
                except IndexError:
                    print('Brak samochodu o takim numerze, spróbuj ponownie')
            else:
                print('Niepoprawna wartość, spróbuj jeszcze raz')


def search_reservation(data):
    """Displays a table with reservations starting on specified date,
    ask user to choose one ans returns this object"""
    header = ['Lp.', 'Imię', 'Nazwisko', 'Data\npoczątkowa', 'Data\nkońcowa',
              'Marka', 'Model', 'Numer\nrejestracyjny', 'Status']
    result = get_list_of_reservations(data)
    if len(result) == 0:
        print(f'Brak rezerwacji na wskazany dzień ({data})\nWciśnij enter')
        input()
        return
    list_of_reservations = []
    content = []
    for index, element in enumerate(result, start=1):
        reservation = change_to_reservation(element)
        list_of_reservations.append(reservation)
        content.append([index] + reservation.represent_as_row())
    print(print_table(header, content))
    print('\nAby wybrać rezerwację wpisz jej numer z listy')
    return select_from_list(list_of_reservations)


def search_rental():
    header = ['Lp.', 'Imię', 'Nazwisko', 'Data początkowa', 'Data końcowa',
              'Data opłacenia', 'Data zwrotu', 'Marka', 'Model',
              'Numer rejestracyjny', 'Status']
    result = get_list_of_rentals()
    if len(result) == 0:
        print('Brak aktywnych wypożyczeń\nWciśnij enter')
        input()
        return
    list_of_rentals = []
    content = []
    for index, element in enumerate(result, start=1):
        rental = change_to_rental(element)
        list_of_rentals.append(rental)
        content.append([index] + rental.represent_as_row())
    print(print_table(header, content))
    return select_from_list(list_of_rentals)


def search_unpaid_rental(parameters):
    """Displays a table with rentals where given dates is after paidtodate"""
    header = ['Lp.', 'Imię', 'Nazwisko', 'Data początkowa', 'Data końcowa',
              'Data opłacenia', 'Data zwrotu', 'Marka', 'Model',
              'Numer\nrejestracyjny', 'Status']
    result = get_list_not_paid_rentals(parameters)
    if len(result) == 0:
        print('Brak wypożyczeń z przekroczonym czasem opłacenia.')
        print('Wciśnij enter')
        input()
        return
    list_of_rentals = []
    content = []
    for index, element in enumerate(result, start=1):
        rental = change_to_rental(element)
        list_of_rentals.append(rental)
        content.append([index] + rental.represent_as_row())
    print(print_table(header, content))
    print('\nWciśnij enter')
    input()


def input_seats_value(auto, text_input, empty, changed_values=None):
    """Asks user to input correct seats value and returns it"""
    correct_value = False
    seats = None
    while not correct_value:
        seats = input(text_input)
        if seats == '' and empty:
            return
        try:
            auto.set_seats(seats)
            correct_value = True
        except WrongSeatsTypeError:
            print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
        except NegativeSeatsError:
            print('Liczba miejsc nie może być ujemna, spróbuj ponownie')
    if changed_values is not None:
        changed_values['seats'] = seats


def input_fuel_consumption_value(auto, text_input, empty, changed_values=None):
    """Asks user to input correct fuel consumption value and returns it"""
    correct_value = False
    fuel_consumption = None
    while not correct_value:
        fuel_consumption = input(text_input)
        if fuel_consumption == '' and empty:
            return
        try:
            auto.set_fuel_consumption(fuel_consumption)
            correct_value = True
        except WrongFuelConsumptionTypeError:
            print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
        except NegativeFuelConsumptionError:
            print('Zużycie paliwa nie może być ujemne, spróbuj ponownie')
    if changed_values is not None:
        changed_values['fuel_consumption'] = fuel_consumption


def input_doors_value(auto, text_input, empty, changed_values=None):
    """Asks user to input correct doors value and returns it"""
    correct_value = False
    doors = None
    while not correct_value:
        doors = input(text_input)
        if doors == '' and empty:
            return
        try:
            auto.set_doors(doors)
            correct_value = True
        except WrongDoorsTypeError:
            print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
        except NegativeDoorsError:
            print('Liczba drzwi nie może być ujemna')
    if changed_values is not None:
        changed_values['doors'] = doors


def input_price_value(auto, text_input, empty, changed_values=None):
    """Asks user to input correct price value and returns it"""
    correct_value = False
    price = None
    while not correct_value:
        price = input(text_input)
        if price == '' and empty:
            return
        try:
            auto.set_price(price)
            correct_value = True
        except WrongPriceTypeError:
            print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
        except NegativePriceError:
            print('Cena nie może byc ujemna, spróbuj ponownie')
    if changed_values is not None:
        changed_values['price'] = price


def input_capacity_value(auto, text_input, empty, changed_values=None):
    """Asks user to input correct capacity value and returns it"""
    correct_value = False
    capacity = None
    while not correct_value:
        capacity = input(text_input)
        if capacity == '' and empty:
            return
        try:
            auto.set_capacity(capacity)
            correct_value = True
        except WrongCapacityTypeError:
            print('Wprowadzona wartość musi być liczbą, spróbuj ponownie')
        except NegativeCapacityError:
            print('Pojemność nie może być ujemna, spróbuj ponownie')
    if changed_values is not None:
        changed_values['capacity'] = capacity


def insert_side_door_value(self, text_input, empty, changed_values=None):
    """Asks user to input correct side_door value and returns it"""
    correct_value = False
    side_door = None
    while not correct_value:
        side_door = input(text_input)
        if side_door == '' and empty:
            return
        try:
            self.set_side_door(side_door)
            correct_value = True
            correct_value['side_door'] = self._side_door
        except WrongSideDoorTypeError:
            print('Wprowadzona wartość musi być liczbą 0 lub 1,'
                  ' spróbuj ponownie')
        except WrongSideDoorValueError:
            print('Wprowadzona liczba musi być 0 lub 1, spróbuj ponownie')
    if changed_values is not None:
        changed_values['side_door'] = side_door


class Car:
    """"
    Class Car. Contains attributes:
    :param mark: mark of car
    :type mark: str

    :param model: model of car
    :type model: str

    :param registration_number: registration_number of car
    :type registration_number: str

    :param seats: amount of seats
    :type seats: int

    :param fuel_consumption: fuel consumtion for 100km in liters
    :type fuel_consumption: float

    :param doors: amount of doors
    :type doors: int

    :param color: color of car
    :type color: str

    :param price: price for one day rental
    :type price: float

    :param db_id: database id of the car
    :type db_id: int
    """
    def __init__(self, mark=None, model=None, registration_number=None,
                 seats=None, fuel_consumption=None, doors=None,
                 color=None, price=None, db_id=None):
        """Constructor for Car class, by default all values are None"""
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
        """Returns a database id of car"""
        return self._db_id

    def mark(self):
        """Returns a mark of car"""
        return self._mark

    def model(self):
        """Returns a model of car"""
        return self._model

    def registration_number(self):
        """Returns a resgistration number of car"""
        return self._registration_number

    def seats(self):
        """Returns a seats number of car"""
        return self._seats

    def fuel_consumption(self):
        """Returns a fuel consumption of car"""
        return self._fuel_consumption

    def doors(self):
        """Returns a doors number of car"""
        return self._doors

    def color(self):
        """Returns a color of car"""
        return self._color

    def price(self):
        """Returns a price of car"""
        return self._price

    def type_id(self):
        """Returns a type id of car"""
        return self._type_id

    def set_db_id(self, db_id):
        """Lets to set a database id of car"""
        try:
            db_id = int(db_id)
        except Exception:
            raise WrongDbIdTypeError(db_id)
        if db_id < 1:
            raise NegativeDbIdError(db_id)
        self._db_id = db_id

    def set_mark(self, mark):
        """Lets to set a mark of car"""
        mark = mark.title()
        self._mark = mark

    def set_model(self, model):
        """Lets to set a model of car"""
        model = model.title()
        self._model = model

    def set_registration_number(self, registration_number):
        """Lets to set a registration number of car"""
        registration_number = registration_number.upper()
        self._registration_number = registration_number

    def set_seats(self, seats):
        """Lets to set a seats number of car"""
        try:
            seats = int(seats)
        except Exception:
            raise WrongSeatsTypeError(seats)
        if seats < 0:
            raise NegativeSeatsError(seats)
        self._seats = seats

    def set_fuel_consumption(self, fuel_consumption):
        """Lets to set a fuel consumption of car"""
        try:
            fuel_consumption = float(fuel_consumption)
        except Exception:
            raise WrongFuelConsumptionTypeError(fuel_consumption)
        if fuel_consumption < 0:
            raise NegativeFuelConsumptionError(fuel_consumption)
        self._fuel_consumption = fuel_consumption

    def set_doors(self, doors):
        """Lets to set a door number of car"""
        try:
            doors = int(doors)
        except Exception:
            raise WrongDoorsTypeError(doors)
        if doors < 0:
            raise NegativeDoorsError(doors)
        self._doors = doors

    def set_color(self, color):
        """Lets to set a color of car"""
        color = color.lower()
        self._color = color

    def set_price(self, price):
        """Lets to set a price of car"""
        try:
            price = float(price)
        except Exception:
            raise WrongPriceTypeError(price)
        if price < 0:
            raise NegativePriceError(price)
        self._price = price

    def insert_values(self):
        """Lets user to input attributes values of car"""
        mark = input('Marka: ')
        self.set_mark(mark)
        model = input('Model: ')
        self.set_model(model)
        registration_number = input('Numer rejestracyjny: ')
        self.set_registration_number(registration_number)
        input_seats_value(self, 'Miejsca: ', False)
        input_fuel_consumption_value(self, 'Zużycie paliwa: ', False)
        input_doors_value(self, 'Drzwi: ', False)
        color = input('Kolor: ')
        self.set_color(color)
        input_price_value(self, 'Cena: ', False)

    def insert_edited_values(self):
        """Lets user to input edited attributes values of car"""
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
        input_seats_value(self, 'Liczba miejsc [{}]: '.format(self._seats),
                          True, changed_values)
        input_fuel_consumption_value(self, 'Zużycie paliwa [{}]: \
                                           '.format(self._fuel_consumption),
                                     True, changed_values)
        input_doors_value(self, 'Drzwi [{}]: '.format(self._doors),
                          True, changed_values)
        color = input('Kolor [{}]: '.format(self._color))
        if color != '':
            self.set_color(color)
            changed_values['color'] = self._color
        input_price_value(self, 'Cena [{}]: '.format(self._price),
                          True, changed_values)
        return changed_values

    def edit_values(self):
        """Call inset_edited_values, displays details of car
        and ask user to confirm editing"""
        changed_values = self.insert_edited_values()
        self.print_as_table()
        if len(changed_values) == 0:
            print('Nie zmieniono żadnych danych\nNaciśnij enter')
            input()
            return
        print('\nCzy zmienić dane pojazdu na powyższe? 0=Nie, 1=Tak')
        answer = input_true_or_false()
        if not answer:
            print('Anulowano zmianę danych\nNaciśnij enter')
            input()
        else:
            query = self.generate_set_query(changed_values)
            query_to_database(query)
            print('Zmieniono dane pojazdu\nNaciśnij enter')
            input()

    def represent_as_row(self):
        """Returns a row to display in table"""
        row = [
            self._mark, self._model,
            self._registration_number, self._seats,
            self._fuel_consumption, self._doors,
            self._color, self._price, 'n/d',
            'n/d', 'n/d', 'n/d', 'Inny'
        ]
        return row

    def rows_to_table(self):
        """Returns a table body with attributes values"""
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
        """Prints car details as table"""
        rows = self.rows_to_table()
        print(print_as_table_with_title('Dane pojazdu', rows))

    def generate_insert_query(self):
        """Generates a INSERT query to database and returns it"""
        query = 'INSERT INTO cars (mark, model, registration_number, seats, '\
                'fuel_consumption, doors, color, price, type_id) VALUES '\
                '("{}", "{}", "{}", {}, {}, {}, "{}", {}, {})'
        query = query.format(self._mark, self._model,
                             self._registration_number, self._seats,
                             self._fuel_consumption, self._doors,
                             self._color, self._price, self._type_id)
        return query

    def generate_delete_query(self):
        """Generates a DELETE query to database and returns it"""
        return f'DELETE FROM cars WHERE db_id={self._db_id}'

    def generate_set_query(self, values):
        """Generates a SET query to db with given changes and returns it"""
        query = 'UPDATE cars SET '
        for key in values:
            value = values[key]
            query += '{}="{}", '.format(key, value)
        query = query[:-2]
        query += ' WHERE db_id={}'.format(self._db_id)
        return query

    def add_to_database(self):
        """Call insert_values function, displays a car as table,
        asks user to confirm and adds to database"""
        self.insert_values()
        self.print_as_table()
        print('\nCzy dodać pojazd do bazy? 0=Nie, 1=Tak: ')
        answer = input_true_or_false()
        if not answer:
            print('Anulowano dodanie do bazy\nNaciśnij enter')
            input()
        else:
            query = self.generate_insert_query()
            query_to_database(query)
            print('Dodano samochód do bazy\nNaciśnij enter')
            input()

    def delete_from_database(self):
        """Ask user to confirm deleting car and send query to database"""
        print('Czy usunąć ten samochód z bazy? 0=Nie, 1=Tak: ')
        answer = input_true_or_false()
        if not answer:
            print('Anulowano usunięcie z bazy\nWciśnij enter')
            input()
        else:
            query = self.generate_delete_query()
            query_to_database(query)
            print('Usunięto samochód z bazy\nWciśnij enter')
            input()


class PassengerCar(Car):
    """
    Class Car. Inherits from Car. Contains attributes:
    :param mark: mark of car
    :type mark: str

    :param model: model of car
    :type model: str

    :param registration_number: registration_number of car
    :type registration_number: str

    :param seats: amount of seats
    :type seats: int

    :param fuel_consumption: fuel consumtion for 100km in liters
    :type fuel_consumption: float

    :param doors: amount of doors
    :type doors: int

    :param color: color of car
    :type color: str

    :param price: price for one day rental
    :type price: float

    :param db_id: database id of the car
    :type db_id: int

    :param body: body type of car
    :type body: str

    :param classfication: classification of car
    :type classification: str
    """
    def __init__(self, mark=None, model=None, registration_number=None,
                 seats=None, fuel_consumption=None, doors=None, color=None,
                 price=None, body=None, classification=None, db_id=None):
        """Constructor for PassengerCar class, default all values are None"""
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
        """Returns a body value of car"""
        return self._body

    def classification(self):
        """Return a classification value of car"""
        return self._classification

    def set_body(self, body):
        """Lets to set body value of PassengerCar"""
        body = body.lower()
        self._body = body

    def set_classification(self, classification):
        """Lets to set classification value of PassengerCar"""
        classification = classification.upper()
        self._classification = classification

    def represent_as_row(self):
        """Returns a row to represent car in table"""
        row = [
            self._mark, self._model,
            self._registration_number, self._seats,
            self._fuel_consumption, self._doors,
            self._color, self._price, self._body,
            self._classification, 'n/d', 'n/d', 'Osobowy'
        ]
        return row

    def rows_to_table(self):
        """Returns rows to represent car as table"""
        rows = super().rows_to_table()
        rows += [
            ['Nadwozie', self._body],
            ['Klasa', self._classification]
        ]
        return rows

    def insert_edited_values(self):
        """Lets user to input edited attributes values of car"""
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
        """Lets user to input attributes values of car"""
        super().insert_values()
        body = input('Nadwozie: ')
        self.set_body(body)
        classification = input('Klasa: ')
        self.set_classification(classification)

    def generate_insert_query(self):
        """Generates a INSERT query to database and returns it"""
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
    """
    Class Van. Inherits from Car. Caontains attributes:
    :param mark: mark of car
    :type mark: str

    :param model: model of car
    :type model: str

    :param registration_number: registration_number of car
    :type registration_number: str

    :param seats: amount of seats
    :type seats: int

    :param fuel_consumption: fuel consumtion for 100km in liters
    :type fuel_consumption: float

    :param doors: amount of doors
    :type doors: int

    :param color: color of car
    :type color: str

    :param price: price for one day rental
    :type price: float

    :param db_id: database id of the car
    :type db_id: int

    :param capacity: capacity in liters of car
    :type capacity: float

    :param side_door: if the car has a side door
    :type side_door: bool
    """
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
        """Returns a capacity value of car"""
        return self._capacity

    def side_door(self):
        """Returns a side_door value of car as bool"""
        return self._side_door

    def set_capacity(self, capacity):
        """Lets to set a capacity value of car"""
        try:
            capacity = float(capacity)
        except Exception:
            raise WrongCapacityTypeError(capacity)
        if capacity < 0:
            raise NegativeCapacityError(capacity)
        self._capacity = capacity

    def set_side_door(self, side_door):
        """Lets to set a side_door value of car"""
        try:
            side_door = int(side_door)
        except Exception:
            raise WrongSideDoorTypeError(side_door)
        if side_door not in {0, 1}:
            raise WrongSideDoorValueError(side_door)
        self._side_door = bool(side_door)

    def represent_as_row(self):
        """"Returns a row to represent car in table"""
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
        """"Returns rows to represent car as table"""
        rows = super().rows_to_table()
        rows += [
            ['Pojemność', self._capacity],
            ['Boczne drzwi', 'Tak' if self._side_door else 'Nie']
        ]
        return rows

    def insert_edited_values(self):
        """Lets user to input edited attributes values of car"""
        changed_values = super().insert_edited_values()

        input_capacity_value(self, 'Pojemność [{}]: '.format(self._capacity),
                             True, changed_values)
        word = 'Tak' if self._side_door else 'Nie'
        text = 'Czy posiada boczne drzwi? 0=Nie, 1=Tak [{}]: '.format(word)
        insert_side_door_value(self, text, True, changed_values)

        return changed_values

    def insert_values(self):
        """Lets user to input attributes values of car"""
        super().insert_values()
        input_capacity_value(self, 'Pojemność: ', False)
        insert_side_door_value(self, 'Czy posiada boczne drzwi? 0=Nie, \
                                      1=Tak: ', False)

    def generate_insert_query(self):
        """Generates INSERT query to database and returns it"""
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
    """
    Class Reservation. Contains attributes:

    :param name: client's firstname
    :type name: str

    :param surname: cliens's surname
    :type surname: str

    :param startdate: first day of reservation
    :type startdate: datetime.date

    :param enddate: last day of reservation
    :type enddate: datetime.date

    :param auto_id: db_id of reserved car
    :type auto_id: int

    :param auto: auto object for reservation
    :type auto: Car, PassengerCar, Van

    :param db_id: database id of reservation
    :type db_id: int

    :param status: status of reservation
    :type status: str
    :values status: aktywna, anulowana, odebrana
    """
    def __init__(self, name=None, surname=None, startdate=None,
                 enddate=None, auto_id=None, db_id=None, status=None):
        """Constructor of Rservation class object,
        default all values are None"""
        if db_id:
            self.set_db_id(db_id)
        else:
            self._db_id = None
        if name:
            self.set_name(name)
        else:
            self._name = None
        if surname:
            self.set_surname(surname)
        else:
            self._surname = None
        if startdate:
            self.set_startdate(startdate)
        else:
            self._startdate = None
        if enddate:
            self.set_enddate(enddate)
        else:
            self._enddate = None
        if auto_id:
            self.set_auto_id(auto_id)
            result = get_car_by_id(self._auto_id)
            self._auto = change_to_car(*result)
        else:
            self._auto_id = None
        if status:
            self._status = status
        else:
            self._status = None

    def db_id(self):
        """Returns a dabatase id of reservation"""
        return self._db_id

    def name(self):
        """Returns a client's firstname"""
        return self._name

    def surname(self):
        """Returns a client's surname"""
        return self._surname

    def startdate(self):
        """Returns a startdate of reservation"""
        return self._startdate

    def enddate(self):
        """Returns a enddate of reservation"""
        return self._enddate

    def auto_id(self):
        """Returns an auto database id for reservation"""
        return self._auto_id

    def status(self):
        """Returns status of reservation"""
        return self._status

    def auto(self):
        """Returns an auto object for reservation"""
        return self._auto

    def set_db_id(self, db_id):
        """Lets to set database id for reservation"""
        try:
            db_id = int(db_id)
        except ValueError:
            raise WrongDbIdTypeError(db_id)
        if db_id < 1:
            raise NegativeDbIdError(db_id)
        self._db_id = db_id

    def set_name(self, name):
        """Lets to set client's firstname for reservation"""
        name = name.title()
        self._name = name

    def set_surname(self, surname):
        """Lets to set client's surname for reservation"""
        surname = surname.title()
        self._surname = surname

    def set_startdate(self, startdate):
        """Lets to set startdate of reservation"""
        if type(startdate) is not datetime.date:
            raise WrongDateType(startdate)
        self._startdate = startdate

    def set_enddate(self, enddate):
        """Lets to set enddate of reservation"""
        if type(enddate) is not datetime.date:
            raise WrongDateType(enddate)
        self._enddate = enddate

    def set_auto_id(self, auto_id):
        """Lets to set an auto database id for reservation"""
        try:
            auto_id = int(auto_id)
        except ValueError:
            raise WrongDbIdTypeError(auto_id)
        if auto_id < 1:
            raise NegativeDbIdError(auto_id)
        self._auto_id = auto_id

    def generate_insert_query(self):
        """Returns INSERT query generated for object"""
        query = 'INSERT INTO reservations (firstname, surname, startdate, '\
                'enddate, auto_id, status) VALUES '\
                '("{}", "{}", "{}", "{}", {}, "{}")'
        query = query.format(self._name, self._surname, self._startdate,
                             self._enddate, self._auto_id, self._status)
        return query

    def generate_cancel_query(self):
        """Returns query to cancel reservation in database'"""
        return f'UPDATE reservations SET status="anulowana" '\
               f'WHERE db_id={self._db_id}'

    def generate_update_query(self, values):
        """Returns UPDATE query with given changed values"""
        query = 'UPDATE reservations SET '
        for key in values:
            value = values.get(key)
            query += '{}="{}", '.format(key, value)
        query = query[:-2]
        query += f' WHERE db_id={self._db_id}'
        return query

    def represent_as_row(self):
        """Returns a row to display in table"""
        row = [self._name, self._surname, str(self._startdate),
               str(self._enddate), self._auto.mark(),
               self._auto.model(), self._auto.registration_number(),
               self.status()]
        return row

    def collect(self):
        """Returns query to collect reservation in database"""
        query = f'UPDATE reservations SET status="odebrana" \
                  WHERE db_id={self._db_id}'
        query_to_database(query)

    def print_as_table(self):
        """Prints reservation as table"""
        table_data = [
                    ['Imię', self._name],
                    ['Nazwisko', self._surname],
                    ['Data początkowa', str(self._startdate)],
                    ['Data końcowa', str(self._enddate)],
                    ['Marka samochodu', self._auto.mark()],
                    ['Model', self._auto.model()],
                    ['Numer rejestracyjny', self._auto.registration_number()]
        ]
        print(print_as_table_with_title('Dane rezerwacji', table_data))
        return table_data

    def insert_values(self):
        """Lets user to input reservation data"""
        name = input('Imię: ')
        self.set_name(name)
        surname = input('Nazwisko: ')
        self.set_surname(surname)
        startdate = None
        enddate = None
        startdate, enddate = input_start_and_end_date('Data początkowa: ',
                                                      'Data końcowa: ')
        self.set_enddate(enddate)
        self.set_startdate(startdate)
        reservation_parameters = {'startdate': self._startdate,
                                  'enddate': self._enddate}
        auto = search_car(reservation_parameters)
        if auto is None:
            return 1
        self._auto = auto
        self._auto_id = auto.db_id()
        self._status = 'aktywna'

    def edit_values(self):
        """Lets user to input edited reservation data"""
        changed_values = {}
        name = input('Imię [{}]: '.format(self._name))
        if name != '':
            changed_values['firstname'] = name
        surname = input('Nazwisko [{}]: '.format(self._surname))
        if surname != '':
            changed_values['surname'] = surname
        startdate = self._startdate
        enddate = self._enddate
        changed_date = False
        previous_dates = (self._startdate, self._enddate)
        startdate, enddate = input_start_and_end_date('Data początkowa [{}]: '
                                                      .format(self._startdate),
                                                      'Data końcowa [{}]: '
                                                      .format(self._enddate),
                                                      True, self._startdate,
                                                      self._enddate)
        if previous_dates != (startdate, enddate):
            changed_values['startdate'] = startdate
            changed_values['enddate'] = enddate
            changed_date = True
        self._startdate = startdate
        self._enddate = enddate
        parameters = {'startdate': startdate, 'enddate': enddate,
                      'res_id': self._db_id}
        reservation_parameters = {'startdate': self._startdate,
                                  'enddate': self._enddate}
        list_of_id_free_cars = get_list_of_id_free_cars(parameters)
        changed_auto = False
        if changed_date and self._auto_id not in list_of_id_free_cars:
            print("Wybrany samochód jest już zajęty w wybranym terminie.")
            print("Wybierz inny: (Wciśnij enter)")
            input()
            auto = search_car(reservation_parameters)
            if auto is None:
                return
            changed_auto = True
            self._auto = auto
            self._auto_id = auto.db_id()
            changed_values['auto_id'] = self._auto_id
        if not changed_auto:
            print('Czy chcesz zmienić auto? 0=Nie, 1=Tak')
            answer = input_true_or_false()
            if answer:
                auto = search_car(reservation_parameters)
                self._auto = auto
                self._auto_id = auto.db_id()
                changed_values['auto_id'] = self._auto_id
        clear_terminal()
        self.print_as_table()
        if len(changed_values) == 0:
            print('Nie zmieniono żadnej wartośći\nWciśnij enter')
            input()
            return
        print('Czy potwierdzasz zmianę rezerwacji? 0=Nie, 1=Tak')
        answer = input_true_or_false()
        if not answer:
            print('Anulowano dodanie do bazy, wciśnij enter')
            input()
        else:
            query = self.generate_update_query(changed_values)
            query_to_database(query)
            print('Zmieniono rezerwację. Wciśnij enter')
            input()

    def add_to_database(self):
        """Calls a insert_values, displays a reservation as table,
        asks user to confirm and adds reservation to database"""
        returned_value = self.insert_values()
        if returned_value == 1:
            return
        self.print_as_table()
        print('\nCzy dodać powyższą rezerwację do bazy? 0=Nie, 1=Tak')
        answer = input_true_or_false()
        if answer:
            query = self.generate_insert_query()
            query_to_database(query)
            print('Dodano rezerwację do bazy\nWciśnij enter')
            input()
        else:
            print('Anulowano dodanie do bazy\nWciśnij enter')
            input()

    def cancel_reservation(self):
        """Returns geneated cancel query to database"""
        print('Czy na pewno anulować rezerwację? 0=Nie, 1=Tak')
        answer = input_true_or_false()
        if not answer:
            print('Anulowano anulowanie rezerwacji\nNaciśnij enter')
            input()
        else:
            query = self.generate_cancel_query()
            query_to_database(query)
            print('Anulowano rezerwację\nWciśnij enter')
            input()


class Rental:
    """
    Class Rental. Contains attributes:

    :param firstname: client's firstname
    :type firstname: str

    :param surname: cliens's surname
    :type surname: str

    :param startdate: first day of rental
    :type startdate: datetime.date

    :param enddate: last day of rental
    :type enddate: datetime.date

    :param paidtodate: last paid day of rental
    :type paidtodate: datetime.date

    :param returndate: day of return car
    :type returndate: datetime.date

    :param auto_id: db_id of reserved car
    :type auto_id: int

    :param auto: auto object for rental
    :type auto: Car, PassengerCar, Van

    :param db_id: database id of reservation
    :type db_id: int

    :param status: status of reservation
    :type status: str
    :values status: aktywna, anulowana, odebrana
    """
    def __init__(self, firstname=None, surname=None, startdate=None,
                 enddate=None, paidtodate=None, returndate=None,
                 auto_id=None, status=None, db_id=None):
        if firstname:
            self.set_firstname(firstname)
        else:
            self._firstname = None
        if surname:
            self.set_surname(surname)
        else:
            self._surname = None
        if startdate:
            self.set_startdate(startdate)
        else:
            self._startdate = None
        if enddate:
            self.set_enddate(enddate)
        else:
            self._enddate = None
        if paidtodate:
            self.set_paidtodate(paidtodate)
        else:
            self._paidtodate = None
        if returndate:
            self.set_returndate(returndate)
        else:
            self._returndate = None
        if auto_id:
            self.set_auto_id(auto_id)
            result = get_car_by_id(self._auto_id)
            self._auto = change_to_car(*result)
        else:
            self._auto_id = None
        if status:
            self.set_status(status)
        else:
            self._status = None
        if db_id:
            self.set_db_id(db_id)
        else:
            self._db_id = None

    def db_id(self):
        """Returns a database id of rental"""
        return self._db_id

    def firstname(self):
        """Returns a client's firstname for rental"""
        return self._firstname

    def surname(self):
        """Returns a client's surname for rental"""
        return self._surname

    def startdate(self):
        """Returns a startdate of rental"""
        return self._startdate

    def enddate(self):
        """Returns a enddate of rental"""
        return self._enddate

    def paidtodate(self):
        """Returns a paidtodate of rental"""
        return self._paidtodate

    def returndate(self):
        """Returns a returndate of rental"""
        return self._returndate

    def auto_id(self):
        """Returns an auto database id for rental"""
        return self._auto_id

    def auto(self):
        """Returns an auto object for rental"""
        return self._auto

    def status(self):
        """Returns a status of rental"""
        return self._status

    def set_db_id(self, db_id):
        """Lets to set a databse id of rental"""
        try:
            db_id = int(db_id)
        except ValueError:
            raise WrongDbIdTypeError(db_id)
        if db_id < 1:
            raise NegativeDbIdError(db_id)
        self._db_id = db_id

    def set_firstname(self, firstname):
        """Lets to set a client's firstname for rental"""
        firstname = firstname.title()
        self._firstname = firstname

    def set_surname(self, surname):
        """Lets to set a client's surname for rental"""
        surname = surname.title()
        self._surname = surname

    def set_startdate(self, startdate):
        """Lets to set a startdate of rental"""
        if type(startdate) is not datetime.date:
            raise WrongDateType(startdate)
        self._startdate = startdate

    def set_enddate(self, enddate):
        """Lets to set a enddate of rental"""
        if type(enddate) is not datetime.date:
            raise WrongDateType(enddate)
        self._enddate = enddate

    def set_paidtodate(self, paidtodate):
        """Lets to set a paidtodate of rental"""
        if type(paidtodate) is not datetime.date:
            raise WrongDateType(paidtodate)
        self._paidtodate = paidtodate

    def set_returndate(self, returndate):
        """Lets to set a returndate of rental"""
        if type(returndate) is not datetime.date:
            raise WrongDateType(returndate)
        self._returndate = returndate

    def set_auto_id(self, auto_id):
        """Lets to set a auto database id for rental"""
        try:
            auto_id = int(auto_id)
        except ValueError:
            raise WrongDbIdTypeError(auto_id)
        if auto_id < 1:
            raise NegativeDbIdError(auto_id)
        self._auto_id = auto_id

    def set_status(self, status):
        """Lets to set a status of rental"""
        self._status = status

    def generate_insert_query(self):
        """Returns generated INSERT query to databse"""
        query = 'INSERT INTO rentals (firstname, surname, startdate, '\
                'enddate, paidtodate, auto_id, status) '\
                'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'
        query = query.format(self._firstname, self._surname,
                             self._startdate, self._enddate,
                             self._paidtodate, self._auto_id, self._status)
        return query

    def generate_return_query(self):
        """Return generated query to return a car"""
        date = datetime.date.today()
        query = f'UPDATE rentals SET status="zwrócony", '\
                f'returndate="{date}" WHERE db_id={self._db_id}'
        return query

    def represent_as_row(self):
        """Returns a row to represent in table"""
        row = [
                self._firstname,
                self._surname,
                str(self._startdate),
                str(self._enddate),
                str(self._paidtodate),
                str(self._returndate) if self._returndate.isoformat() !=
                '1970-01-01' else 'n/d',
                self._auto.mark(),
                self._auto.model(),
                self._auto.registration_number(),
                self._status
        ]
        return row

    def print_as_table(self):
        """Prints a rental as table"""
        table_data = [
                        ['Imię', self._firstname],
                        ['Nazwisko', self._surname],
                        ['Data początkowa', str(self._startdate)],
                        ['Data końcowa', str(self._enddate)],
                        ['Data opłacenia rezerwacji', str(self._paidtodate)],
                        ['Marka', self._auto.mark()],
                        ['Model', self._auto.model()],
                        ['Numer rejestracyjny',
                         self._auto.registration_number()]
        ]
        print(print_as_table_with_title('Dane rezerwacji', table_data))
        return table_data

    def collect_reservation(self, reservation):
        """Lets to collect reservation
        and optionally edit values from reservation"""
        firstname = input('Imię [{}]: '.format(reservation.name()))
        if firstname == '':
            self.set_firstname(reservation.name())
        else:
            self.set_firstname(firstname)
        surname = input('Nazwisko [{}]: '.format(reservation.surname()))
        if surname == '':
            self.set_surname(reservation.surname())
        else:
            self.set_surname(surname)
        correct_dates = False
        while not correct_dates:
            startdate = reservation.startdate()
            enddate = reservation.enddate()
            self._startdate, self._enddate = input_start_and_end_date(
                                                     'Data początkowa [{}]: '
                                                     .format(startdate),
                                                     'Data końcowa [{}]: '
                                                     .format(enddate), True,
                                                     startdate, enddate)
            correct_value = False
            while not correct_value:
                paiddays = input('Opłacona ilość dni: ')
                if paiddays.isdigit() and paiddays != '0':
                    paiddays = int(paiddays)
                    paiddays -= 1
                    correct_value = True
                    date_delta = datetime.timedelta(days=paiddays)
                    self._paidtodate = self._startdate + date_delta
                else:
                    print('Niepoprawna wartość, spróbuj ponownie')
            if self._paidtodate > self._enddate:
                print('Nie można opłacić więcej dni niż czas trwania '
                      'wypożyczenia, spróbuj ponownie')
            else:
                correct_dates = True
        self._auto = reservation.auto()
        self._auto_id = reservation.auto_id()
        reservation.collect()
        self.print_as_table()
        print('\nCzy dodać powyższe wypożyczenie? 0=Nie, 1=Tak')
        answer = input_true_or_false()
        if not answer:
            print('Anulowano wypożyczenie\nNaciśnij enter')
            input()
        else:
            self._status = 'wypożyczony'
            query = self.generate_insert_query()
            query_to_database(query)
            print('Dodano do bazy\nWciśnij enter')
            input()

    def insert_values(self):
        """Lets user to input rental data"""
        clear_terminal()
        firstname = input('Imię: ')
        self.set_firstname(firstname)
        surname = input('Nazwisko: ')
        self.set_surname(surname)
        correct_dates = False
        while not correct_dates:
            self._startdate,
            self._enddate = input_start_and_end_date('Data początkowa: ',
                                                     'Data końcowa: ')
            correct_value = False
            while not correct_value:
                paiddays = input('Opłacona ilość dni: ')
                if paiddays.isdigit() and paiddays != '0':
                    paiddays = int(paiddays)
                    paiddays -= 1
                    correct_value = True
                    date_delta = datetime.timedelta(days=paiddays)
                    self._paidtodate = self._startdate + date_delta
                else:
                    print('Niepoprawna wartość, spróbuj ponownie')
            if self._paidtodate > self._enddate:
                print('Nie można opłacić więcej dni niż czas trwania \
                       rezerwacji, spróbuj ponownie')
            else:
                correct_dates = True
        date_parameters = {'startdate': self._startdate,
                           'enddate': self._enddate}
        auto = search_car(date_parameters)
        if auto is None:
            return 1
        self._auto_id = auto.db_id()
        self._auto = auto

    def return_car(self):
        """Warns user about dirrefent datesm, asks to confirm
        and changes status in databse"""
        if self._paidtodate != datetime.date.today():
            print('Data opłacenia jest różna od daty dzisiejszej!')
            print('Czy kontynuować? 0=Nie, 1=Tak')
            answer = input_true_or_false()
            if not answer:
                print('Anulowano zwrot pojazdu\nWciśnij enter')
                return
            print('Czy na pewno chcesz zwrócić ten pojazd? 0=Nie, 1=Tak')
            answer = input_true_or_false()
            if not answer:
                print('Anulowano zwrot pojazdu\nWciśnij enter')
                return
        query = self.generate_return_query()
        query_to_database(query)
        print('Zwrócono pojazd\nWciśnij enter')
        input()

    def add_to_database(self):
        """Call insert_values function,
        asks user to confirm and adds rental to database"""
        if self.insert_values() == 1:
            return
        self.print_as_table()
        print('\nCzy dodać powyższe wypożyczenie? 0=Nie, 1=Tak')
        answer = input_true_or_false()
        if not answer:
            print('Anulowano wypożyczenie\nNaciśnij enter')
            input()
        else:
            self._status = 'wypożyczony'
            query = self.generate_insert_query()
            query_to_database(query)
            print('Dodano do bazy\nWciśnij enter')
            input()
