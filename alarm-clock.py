import playsound


def display_menu():

    print("Welcome to the Clock")
    print("\n== MAIN MENU ==\n")
    my_menu_list = ["World Clock","Stopwatch", "Alarm", "Exit"]
    for option in my_menu_list:
        if option == "Exit":
            print("[0]", option)
        else:
            print([my_menu_list.index(option) + 1], option)


def main():
    while True:
        display_menu()
        choice = input("Select an option (0-2): ")

        if choice == "1":
            print("You selected: World Clock")
        elif choice == "2":
            print("You selected: Stopwatch")
        elif choice == "3":
            print("You selected: Alarm")
        elif choice == "0":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()  