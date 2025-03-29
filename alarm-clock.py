import pygame  # Importuje bibliotekę pygame do obsługi dźwięku
import time  # Importuje bibliotekę time do zarządzania czasem
import datetime  # Importuje bibliotekę datetime do pracy z datą i czasem
import threading  # Importuje bibliotekę threading do obsługi wątków

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

def display_menu():
    # Funkcja wyświetlająca menu główne
    print("Welcome to the Clock")  # Wyświetla powitanie
    print("\n== MAIN MENU ==\n")  # Wyświetla nagłówek menu
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
        elif choice == "2":  # Jeśli użytkownik wybierze opcję 2
            print("You selected: Stopwatch")  # Wyświetla komunikat o wyborze
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