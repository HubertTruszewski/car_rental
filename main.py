import os


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
    pass


def manipulate_car():
    pass


def auto_menu():
    print("MENU - AUTA")
    print("Proszę wybrać jedną z dostępnych opcji:")
    print("1. Dodanie nowego samochodu")
    print("2. Wyszukiwanie pojazdu, edycja danych, usuwanie")
    print("9. Powrót do głównego menu")

    answer = 0

    while not answer:
        answer = int(input("Wybór: "))
    if answer == 1:
        clear_terminal()
        add_car()
    elif answer == 2:
        clear_terminal()
        manipulate_car()
    elif answer == 9:
        clear_terminal()
        main()
    else:
        print("Niepoprawny wybór, spróbuj jeszcze raz:")
        answer = 0


def reservation_menu():
    pass


def rental_menu():
    pass


def main():
    print_logo()
    print_line(40)
    print_main_menu()

    answer = 0

    while not answer:
        answer = int(input("Wybór: "))
        if answer == 1:
            clear_terminal()
            auto_menu()
        elif answer == 2:
            clear_terminal()
            reservation_menu()
        elif answer == 3:
            clear_terminal()
            rental_menu()
        elif answer == 0:
            break
        else:
            print("Niepoprawny wybór, spróbuj jeszcze raz:")
            answer = 0


if __name__ == "__main__":
    main()
