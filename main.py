import datetime
import os
from classes import Car, PassengerCar, Rental, Reservation, Van, search_rental, search_reservation
from classes import search_unpaid_rental
from classes import search_car


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
#     #  #####     #    ####### #     #"""[1:])


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


def add_reservation():
    reservation = Reservation()
    reservation.add_to_database()


def manipulate_reservation():
    data = datetime.date.today()
    correct_value = False
    while not correct_value:
        answer = input('Na jaki dzień wyświetlić rezerwacje? [{}]: '.format(data))
        if answer != '':
            try:
                data = datetime.date.fromisoformat(answer)
                correct_value = True
            except ValueError as e:
                print('Niepoprawna wartość. Szczegóły: '+str(e))
                print('Spróbuj ponownie')
        else:
            correct_value = True
    reservation = search_reservation(data)
    if reservation is None:
        return
    clear_terminal()
    reservation.print_as_table()
    print('\n1. Edycja rezerwacji\n2. Usuwanie rezerwacji\n9. Powrót')
    correct_value = False
    while not correct_value:
        answer = input('Wybór: ')
        if answer in {'1', '2', '9'}:
            answer = int(answer)
            if answer == 1:
                reservation.edit_values()
            elif answer == 2:
                reservation.cancel_reservation()
            else:
                return
        else:
            print('Niepoprawna wartość, spróbuj ponownie')


def auto_menu():
    clear_terminal()
    print("MENU - AUTA")
    print("Proszę wybrać jedną z dostępnych opcji:")
    print("1. Dodanie nowego samochodu")
    print("2. Wyszukiwanie pojazdu po parametrach, edycja danych, usuwanie")
    print("3. Wyszukiwanie po datach dostępności")
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
    clear_terminal()
    print('MENU - REZERWACJE')
    print('1. Nowa rezerwacja\n2. Wyświetlenie, edycja, anulowanie rezerwacji\n3. Powrót')
    correct_value = False
    while not correct_value:
        answer = input('Wybór: ')
        if answer in {'1', '2', '9'}:
            answer = int(answer)
            correct_value = True
            if answer == 1:
                add_reservation()
            if answer == 2:
                manipulate_reservation()
            else:
                return
        else:
            print('Niepoprawna wartość, spróbuj ponownie')


def collection_reservation():
    data = datetime.date.today()
    correct_value = False
    while not correct_value:
        answer = input('Na jaki dzień wyświetlić rezerwacje? [{}]: '.format(data))
        if answer != '':
            try:
                data = datetime.date.fromisoformat(answer)
                correct_value = True
            except ValueError as e:
                print('Niepoprawna wartość. Szczegóły: '+str(e))
                print('Spróbuj ponownie')
        else:
            correct_value = True
    reservation: Reservation = search_reservation(data)
    rental = Rental()
    rental.collect_reservation(reservation)


def new_rental():
    rental = Rental()
    rental.add_to_database()
    return


def show_not_paid_rentals():
    search_unpaid_rental(datetime.date.today())
    input('\nWciśnij enter\n')
    return


def return_auto():
    rental = search_rental()
    if rental:
        rental.return_car()
    return


def rental_menu():
    clear_terminal()
    print('1. Odbiór rezerwacji\n2. Wypożyczenie aktualnie dostępnego pojazdu')
    print('3. Wypożyczenia z przekroczonym czasem opłacenia\n4. Zwrot samochodu\n9. Powrót')
    correct_value = False
    while not correct_value:
        answer = input('Wybór: ')
        if answer == '1':
            collection_reservation()
        elif answer == '2':
            new_rental()
            return
        elif answer == '3':
            show_not_paid_rentals()
            return
        elif answer == '4':
            return_auto()
            return
        elif answer == '9':
            return
        else:
            print('Niepoprawna wartość, spróbuj ponownie')


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
