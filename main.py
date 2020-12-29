import os
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
                if answer == 2:
                    auto = Van()
                if answer == 3:
                    auto = Car()
                    auto.add_to_database()
            else:
                print('Niepoprawna wartość, spróbuj jeszcze raz')
        else:
            print('Niepoprawna wartość, spróbuj jeszcze raz')


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
