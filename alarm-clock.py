import pygame  # Importuje bibliotekę pygame do obsługi dźwięku
import time  # Importuje bibliotekę time do zarządzania czasem
import datetime  # Importuje bibliotekę datetime do pracy z datą i czasem
import threading  # Importuje bibliotekę threading do obsługi wątków
from datetime import datetime  # Importuje klasę datetime z biblioteki datetime
import pytz  # Importuje bibliotekę pytz do obsługi stref czasowych

stop_alarm = False  # Flaga globalna, która kontroluje zatrzymanie alarmu

def play_sound(file_path):
    # Funkcja odtwarzająca dźwięk alarmu
    global stop_alarm  # Używa globalnej flagi stop_alarm
    pygame.mixer.init()  # Inicjalizuje mikser dźwięku pygame
    pygame.mixer.music.load(file_path)  # Ładuje plik dźwiękowy
    pygame.mixer.music.play()  # Odtwarza plik dźwiękowy
    while pygame.mixer.music.get_busy():  # Sprawdza, czy dźwięk jest odtwarzany
        if stop_alarm:  # Jeśli flaga stop_alarm jest ustawiona na True
            pygame.mixer.music.stop()  # Zatrzymuje odtwarzanie dźwięku
            break  # Przerywa pętlę
        time.sleep(1)  # Czeka 1 sekundę przed kolejnym sprawdzeniem

def stop_alarm_input():
    # Funkcja pozwalająca użytkownikowi zatrzymać alarm
    global stop_alarm  # Używa globalnej flagi stop_alarm
    input("Press Enter to stop the alarm...")  # Czeka na naciśnięcie Enter przez użytkownika
    stop_alarm = True  # Ustawia flagę stop_alarm na True

def set_alarm(alarm_time):
    # Funkcja ustawiająca alarm na określony czas
    global stop_alarm  # Używa globalnej flagi stop_alarm
    alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M:%S").strftime("%H:%M:%S")  # Konwertuje czas alarmu na format HH:MM:SS
    print(f"Alarm set for {alarm_time}.")  # Wyświetla komunikat o ustawieniu alarmu
    is_running = True  # Flaga kontrolująca działanie pętli alarmu
    while is_running:  # Pętla sprawdzająca czas
        current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Pobiera aktualny czas w formacie HH:MM:SS
        print(f"Current time: {current_time}", end="\r")  # Wyświetla aktualny czas w tej samej linii
        if current_time == alarm_time:  # Sprawdza, czy aktualny czas to czas alarmu
            stop_alarm = False  # Resetuje flagę stop_alarm
            print("\nAlarm ringing!")  # Wyświetla komunikat o dzwoniącym alarmie
            
            # Tworzy nowy wątek do odtwarzania dźwięku
            sound_thread = threading.Thread(target=play_sound, args=('iphone_alarm.mp3',))
            sound_thread.start()  # Uruchamia wątek odtwarzania dźwięku
            
            stop_alarm_input()  # Wywołuje funkcję zatrzymania alarmu
            sound_thread.join()  # Czeka na zakończenie wątku odtwarzania dźwięku
            is_running = False  # Ustawia flagę is_running na False, aby zakończyć pętlę
        time.sleep(1)  # Czeka 1 sekundę przed kolejnym sprawdzeniem czasu

def format_time(seconds):
    # Funkcja formatująca czas w sekundach na HH:MM:SS
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def stopwatch():
    # Funkcja obsługująca stoper
    print("\n== STOPWATCH ==")
    print("Commands: [S]tart, [P]ause, [R]eset, [L]ap, [Q]uit")
    
    running = False  # Flaga wskazująca, czy stoper działa
    start_time = 0  # Czas rozpoczęcia
    elapsed_time = 0  # Łączny czas działania stopera
    laps = []  # Lista przechowująca czasy okrążeń

    while True:
        command = input("Enter command: ").strip().lower()  # Pobiera polecenie od użytkownika

        if command == "s":  # Start
            if not running:
                running = True
                start_time = time.time() - elapsed_time  # Ustawia czas rozpoczęcia, uwzględniając poprzedni czas
                print("Stopwatch started.")
            else:
                print("Stopwatch is already running.")

        elif command == "p":  # Pause
            if running:
                running = False
                elapsed_time = time.time() - start_time  # Oblicza czas działania stopera
                print(f"Stopwatch paused at {format_time(elapsed_time)}.")
            else:
                print("Stopwatch is not running.")

        elif command == "r":  # Reset
            running = False
            start_time = 0
            elapsed_time = 0
            laps = []  # Czyści listę okrążeń
            print("Stopwatch reset.")

        elif command == "l":  # Lap
            if running:
                lap_time = time.time() - start_time  # Oblicza czas od rozpoczęcia
                laps.append(lap_time)  # Dodaje czas okrążenia do listy
                print(f"Lap {len(laps)}: {format_time(lap_time)}")
            else:
                print("Stopwatch is not running. Start it first.")

        elif command == "q":  # Quit
            print("Exiting stopwatch.")
            break

        else:
            print("Invalid command. Use [S], [P], [R], [L], or [Q].")

        if running:
            # Wyświetla aktualny czas działania stopera
            elapsed_time = time.time() - start_time
            print(f"Elapsed time: {format_time(elapsed_time)}", end="\r")

def load_cities(file_path):
    """
    Funkcja wczytująca miasta i ich strefy czasowe z pliku txt.
    :param file_path: Ścieżka do pliku cities.txt
    :return: Słownik {miasto: strefa_czasowa}
    """
    cities = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()  # Usuwa białe znaki z początku i końca linii
                if line:  # Ignoruje puste linie
                    city, timezone = line.split(",")  # Rozdziela miasto i strefę czasową
                    cities[city.strip()] = timezone.strip()  # Dodaje do słownika
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")
    return cities

def world_clock():
    """
    Funkcja wyświetlająca aktualny czas w wybranych miastach.
    """
    file_path = "cities.txt"  # Ścieżka do pliku z miastami
    cities = load_cities(file_path)  # Wczytuje miasta i strefy czasowe

    if not cities:
        print("No cities available to display.")
        return

    print("\n== WORLD CLOCK ==")
    for city, timezone in cities.items():
        try:
            tz = pytz.timezone(timezone)  # Pobiera strefę czasową
            city_time = datetime.now(tz)  # Pobiera aktualny czas w danej strefie
            print(f"{city}: {city_time.strftime('%Y-%m-%d %H:%M:%S')}")  # Wyświetla czas
        except pytz.UnknownTimeZoneError:
            print(f"Error: Unknown timezone for city '{city}'.")

def display_menu():
    # Funkcja wyświetlająca menu główne
    print("\n\n\n== CLOCK MAIN MENU ==\n\n\n")  # Wyświetla nagłówek menu
    my_menu_list = ["World Clock", "Stopwatch", "Alarm", "Exit"]  # Lista opcji menu
    for option in my_menu_list:  # Iteruje przez opcje menu
        if option == "Exit":  # Jeśli opcja to "Exit"
            print("[0]", option)  # Wyświetla opcję wyjścia z numerem 0
        else:
            print([my_menu_list.index(option) + 1], option)  # Wyświetla inne opcje z numerami od 1

def main():
    # Funkcja główna programu
    while True:  # Pętla główna programu
        display_menu()  # Wywołuje funkcję wyświetlającą menu
        choice = input("Select an option (0-3): ")  # Pobiera wybór użytkownika

        if choice == "1":  # Jeśli użytkownik wybierze opcję 1
            print("You selected: World Clock")  # Wyświetla komunikat o wyborze
            world_clock()  # Uruchamia funkcję World Clock
        elif choice == "2":  # Jeśli użytkownik wybierze opcję 2
            print("You selected: Stopwatch")  # Wyświetla komunikat o wyborze
            stopwatch()  # Uruchamia funkcję stopera
        elif choice == "3":  # Jeśli użytkownik wybierze opcję 3
            print("You selected: Alarm")  # Wyświetla komunikat o wyborze
            alarm_time = input("Enter alarm time in HH:MM:SS format: ")  # Pobiera czas alarmu od użytkownika
            try:
                datetime.datetime.strptime(alarm_time, "%H:%M:%S")  # Sprawdza poprawność formatu czasu
                set_alarm(alarm_time)  # Ustawia alarm
            except ValueError:  # Jeśli format czasu jest niepoprawny
                print("Invalid time format. Please use HH:MM:SS.")  # Wyświetla komunikat o błędzie
        elif choice == "0":  # Jeśli użytkownik wybierze opcję 0
            print("Exiting the program. Goodbye!")  # Wyświetla komunikat o zakończeniu programu
            break  # Kończy pętlę główną
        else:  # Jeśli użytkownik wybierze nieprawidłową opcję
            print("Invalid option. Please try again.")  # Wyświetla komunikat o błędzie

if __name__ == "__main__":
    main()  # Uruchamia funkcję główną programu