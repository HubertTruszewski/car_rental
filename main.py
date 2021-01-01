import os
from terminaltables import AsciiTable
from classes import Car, PassengerCar, Van
from modelio import get_list_of_cars


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
    clear_terminal()
    correct_value = False
    print('Jaki typ pojazdu dodać?\n1. Samochód osobowy')
    print('2. Samochód dostawczy\n3. Inny')
    while not correct_value:
        answer = input('Wybór: ')
        if answer.isdigit():
            answer = int(answer)
            if answer in {1, 2, 3}:
                if answer == 1:
                    auto = PassengerCar()
                elif answer == 2:
                    auto = Van()
                else:
                    auto = Car()
                auto.add_to_database()
                return
            else:
                print('Niepoprawna wartość, spróbuj jeszcze raz')
        else:
            print('Niepoprawna wartość, spróbuj jeszcze raz')


def manipulate_car():
    parameters = {}
    while True:
        result = get_list_of_cars(parameters)
        list_of_cars = []
        for element in result:
            if element[-1] == 0:
                auto = Car(*element[1:-5], element[0])
            elif element[-1] == 1:
                auto = PassengerCar(*element[1:11], element[0])
            else:
                auto = Van(*element[1:9], *element[11:12], element[0])
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
            elif answer.isdigit():
                answer = int(answer)
                try:
                    if answer == 0:
                        raise IndexError(answer)
                    display_car(list_of_cars[answer-1])
                    return
                except IndexError:
                    print('Brak samochodu o takim numerze, spróbuj ponownie')
            else:
                print('Niepoprawna wartość, spróbuj jeszcze raz')


def parameters_menu(parameters: dict):
    pass


def display_car(auto: Car):
    clear_terminal()
    auto.print_as_table()
    print('\n1.Edytuj dane pojazdu\n2.Usuwanie pojazdu\n9.Powrót')
    correct_value = False
    while not correct_value:
        answer = input('Wybór: ')
        if answer.isdigit():
            answer = int(answer)
            if answer in {1, 2, 9}:
                if answer == 1:
                    auto.edit_values()
                if answer == 2:
                    auto.delete_from_database()
                    return
                else:
                    return
            else:
                print('Niepoprawna wartość, spróbuj ponownie')
        else:
            print('Niepoprawna wartość, spróbuj ponownie')


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
            return
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
