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


def auto_menu():
    pass


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
            auto_menu()
        elif answer == 2:
            reservation_menu()
        elif answer == 3:
            rental_menu()
        else:
            print("Niepoprawny wybór, spróbuj jeszcze raz:")
            answer = 0


if __name__ == "__main__":
    main()
