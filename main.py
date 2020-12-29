import os
from classes import (NegativeCapacityError,
                     NegativePriceError,
                     NegativeFuelConsumptionError)
from classes import Car, PassengerCar, Van


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_logo():
    print("""
   #    #     # ####### ####### #     #
  # #   #     #    #    #        #   #
 #   #  #     #    #    #         # #
#     # #     #    #    #####      #
####### #     #    #    #         # #
#     # #     #    #    #        #   #
#     #  #####     #    ####### #     #""")


def print_line(number):
    print('-' * number)


def print_main_menu():
    print("Witaj w programie Autex!")
    print("Proszę wybrać jedną z dostępnych opcji")
    print("1. Auta")
    print("2. Rezerwacje")
    print("3. Wypożyczenia")
    print("0. Wyjście z programu")


def add_car():
    fuel_consumption = None
    price = None
    capacity = None
    side_door = None
    print('Jaki rodzaj samochodu dodać?\n1. Samochód osobowy\n2. Samochód dostawczy\
          \n3. Inny')
    answer = 0
    while not answer:
        answer = input("Wybór: ")
        if answer.isdigit():
            answer = int(answer)
            if answer not in {1, 2, 3}:
                print('Możliwe opcje to 1, 2, 3; spróbuj jeszcze raz')
                answer = 0
                continue
        else:
            print('Niepoprawna wartość, spróbuj jeszcze raz')
            answer = 0
            continue
        mark = input('Marka pojazdu: ')
        model = input('Model pojazdu: ')
        registration_number = input('Numer rejestracyjny: ')
        seats = 0

        while not seats:
            seats = input("Liczba miejsc: ")
            if seats.isdigit():
                seats = int(seats)
                if seats == 0:
                    print('Niepoprawna wartość, spróbuj jeszcze raz')
            else:
                print("Niepoprawna wartość, spróbuj ponownie")
                seats = 0

        correct_fuel_consumption = False
        while not correct_fuel_consumption:
            try:
                fuel_consumption = float(input('Spalanie: '))
                if fuel_consumption < 0:
                    raise NegativeFuelConsumptionError(fuel_consumption)
                correct_fuel_consumption = True
            except NegativeFuelConsumptionError:
                print('Spalanie nie może być ujemne, spróbuj jeszcze raz')
                continue
            except Exception:
                print('Niepoprawna wartość, spróbuj jeszcze raz')
                continue

        doors = 0
        while not doors:
            doors = input("Liczba drzwi: ")
            if doors.isdigit():
                doors = int(doors)
                if doors == 0:
                    print('Niepoprawna wartość, spróbuj jeszcze raz')
            else:
                print("Niepoprawna wartość, spróbuj jeszcze raz")
                doors = 0

        color = input('Kolor: ')
        correct_price = False
        while not correct_price:
            try:
                price = float(input('Cena: '))
                if price < 0:
                    raise NegativePriceError(price)
                correct_price = True
            except NegativePriceError:
                print('Cena nie może być ujemna, spróbuj jeszcze raz!')
            except Exception:
                print('Niepoprawna wartość, spróbuj jeszcze raz')
        if answer == 1:
            body = input('Nadwozie: ')
            classification = input('Klasa: ')
            auto = PassengerCar(mark, model, registration_number, seats,
                                fuel_consumption, doors, color, price,
                                body, classification)
            auto.add_to_database()
        if answer == 2:
            correct_capacity = False
            while not correct_capacity:
                try:
                    capacity = float(input('Pojemność: '))
                    if capacity < 0:
                        raise NegativeCapacityError(capacity)
                    correct_capacity = True
                except NegativeCapacityError:
                    print('Pojemność nie może być ujemna, spróbuj jeszcze raz')
                except Exception:
                    print('Niepoprawna wartość, spróbuj jeszcze raz')
            correct_side_door = False
            while not correct_side_door:
                side_door = input('Czy posiada boczne drzwi? 1=Tak, 0=Nie: ')
                if side_door.isdecimal():
                    side_door = int(side_door)
                    if side_door != 0 and side_door != 1:
                        print('Poprawne dane to 0 lub 1, spróbuj jeszcze raz')
                    else:
                        correct_side_door = True
                else:
                    print('Niepoprawna wartość, spróbuj jeszcze raz')
            auto = Van(mark, model, registration_number, seats,
                       fuel_consumption, doors, color, price,
                       capacity, side_door)
            auto.add_to_database()
        if answer == 3:
            auto = Car(mark, model, registration_number, seats,
                       fuel_consumption, doors, color, price)
            auto.add_to_database()


def manipulate_car():
    pass


def search_car(parameters):
    pass


def auto_menu():
    clear_terminal()
    print("MENU - AUTA")
    print("Proszę wybrać jedną z dostępnych opcji:")
    print("1. Dodanie nowego samochodu")
    print("2. Wyszukiwanie pojazdu, edycja danych, usuwanie")
    print("9. Powrót do głównego menu")

    answer = 0

    while not answer:
        try:
            answer = int(input("Wybór: "))
        except Exception:
            print('Podana wartość musi być liczbą, spróbuj jeszcze raz')
            answer = 0
            continue
        if answer == 1:
            add_car()
        elif answer == 2:
            manipulate_car()
        elif answer == 9:
            return
        else:
            print("Niepoprawny wybór, spróbuj jeszcze raz:")
            answer = 0


def reservation_menu():
    pass


def rental_menu():
    pass


def main_menu():

    answer = 0

    while not answer:
        clear_terminal()
        print_logo()
        print_line(40)
        print_main_menu()

        try:
            answer = int(input("Wybór: "))
        except Exception:
            print('Niepoprawna wartość, spróbuj jeszcze raz')
            continue
        if answer == 1:
            auto_menu()
        elif answer == 2:
            reservation_menu()
        elif answer == 3:
            rental_menu()
        elif answer == 0:
            break
        else:
            print("Niepoprawny wybór, spróbuj jeszcze raz:")
            answer = 0
        answer = 0
        continue


if __name__ == "__main__":
    main_menu()
