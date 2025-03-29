import pygame
import time
import datetime
import threading

class AlarmClock:
    def __init__(self):
        self.stop_alarm = False

    def play_sound(self, file_path):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if self.stop_alarm:
                    pygame.mixer.music.stop()
                    break
                time.sleep(1)
        except pygame.error as e:
            print(f"Error playing sound: {e}")

    def stop_alarm_input(self):
        input("Press Enter to stop the alarm...")
        self.stop_alarm = True

    def set_alarm(self, alarm_time):
        alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M:%S").strftime("%H:%M:%S")
        print(f"Alarm set for {alarm_time}.")
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Current time: {current_time}", end="\r")
            if current_time == alarm_time:
                self.stop_alarm = False
                print("\nAlarm ringing!")
                sound_thread = threading.Thread(target=self.play_sound, args=('iphone_alarm.mp3',))
                sound_thread.start()
                self.stop_alarm_input()
                sound_thread.join()
                break
            time.sleep(1)

def display_menu():
    print("Welcome to the Clock")
    print("\n== MAIN MENU ==\n")
    print("[1] World Clock")
    print("[2] Stopwatch")
    print("[3] Alarm")
    print("[0] Exit")

def main():
    alarm_clock = AlarmClock()
    menu_options = {
        "1": lambda: print("You selected: World Clock"),
        "2": lambda: print("You selected: Stopwatch"),
        "3": lambda: alarm_clock.set_alarm(input("Enter alarm time in HH:MM:SS format: ")),
        "0": lambda: exit("Exiting the program. Goodbye!")
    }

    while True:
        display_menu()
        choice = input("Select an option (0-3): ")
        action = menu_options.get(choice, lambda: print("Invalid option. Please try again."))
        action()

if __name__ == "__main__":
    main()