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


def search_car():
    parameters = []
    while True:
        clear_terminal()
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


def display_car():
    auto = search_car()
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
            display_car()
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
