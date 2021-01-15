import datetime
import os
from classes import Car, PassengerCar, Rental, Reservation, Van, input_date, input_start_and_end_date, search_rental
from classes import search_unpaid_rental, search_reservation
from classes import search_car
from modelio import query_to_database


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


def cancel_uncollected_reservation():
    query = 'UPDATE reservations SET status="anulowana" WHERE "{}">startdate AND status="aktywna"'
    query = query.format(datetime.date.today())
    query_to_database(query)


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
    if auto is None:
        return
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
                return
            elif answer == 2:
                reservation.cancel_reservation()
                return
            elif answer == 9:
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
            return
        elif answer == 3:
            clear_terminal()
            startdate, enddate = input_start_and_end_date('Data początkowa: ', 'Data końcowa: ')
            dates_parameteres = {'startdate': startdate, 'enddate': enddate}
            search_car(dates_parameteres)
            return
        elif answer == 9:
            return
        else:
            print("Niepoprawny wybór, spróbuj jeszcze raz:")
            answer = 0


def reservation_menu():
    clear_terminal()
    print('MENU - REZERWACJE')
    print('1. Nowa rezerwacja\n2. Wyświetlenie, edycja, anulowanie rezerwacji\n9. Powrót')
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
    data = input_date('Na jaki dzień wyświetlić rezerwacje? [{}]: '.format(data), True, data)
    correct_value = False
    reservation = None
    while not correct_value:
        reservation = search_reservation(data)
        if reservation is None:
            return
        elif reservation.status() != 'aktywna':
            print('Nie można wypożyczyć odebranej lub anulowanej rezerwacji')
            print('Spróbuj ponownie\nWciśnij enter')
            input()
            return
        else:
            correct_value = True
    rental = Rental()
    rental.collect_reservation(reservation)


def new_rental():
    rental = Rental()
    rental.add_to_database()
    return


def show_not_paid_rentals():
    search_unpaid_rental(datetime.date.today())
    return


def return_auto():
    rental = search_rental()
    if rental:
        rental.return_car()
    return


def rental_menu():
    clear_terminal()
    print('MENU - REZERWACJE\n1. Odbiór rezerwacji\n2. Wypożyczenie aktualnie dostępnego pojazdu')
    print('3. Wypożyczenia z przekroczonym czasem opłacenia\n4. Zwrot samochodu\n9. Powrót')
    correct_value = False
    while not correct_value:
        answer = input('Wybór: ')
        if answer == '1':
            collection_reservation()
            return
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
    while True:
        answer = 0
        clear_terminal()
        print_logo()
        print_line(40)
        print_main_menu()

        while not answer:
            try:
                answer = int(input("Wybór: "))
            except Exception:
                print('Niepoprawna wartość, spróbuj jeszcze raz')
                continue
            if answer == 1:
                auto_menu()
                break
            elif answer == 2:
                reservation_menu()
                break
            elif answer == 3:
                rental_menu()
                break
            elif answer == 0:
                return
            else:
                print("Niepoprawny wybór, spróbuj jeszcze raz:")
                answer = 0


if __name__ == "__main__":
    cancel_uncollected_reservation()
    main_menu()
