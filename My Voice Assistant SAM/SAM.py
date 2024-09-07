import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import winshell
import threading
import time
import os
import subprocess
import Levenshtein
import sqlite3
import pywhatkit
from fuzzywuzzy import fuzz
import pyautogui



# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to speak the response in a separate thread
def speak_in_thread(text):
    thread = threading.Thread(target=engine.say, args=(text,))
    thread.start()
    engine.runAndWait()

# Function to listen to commands
def take_command():
    start_time = time.time()  # Record start time
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-In')
            print(f"User said: {query}\n")

            end_time = time.time()  # Record end time
            processing_time = end_time - start_time  # Calculate processing time
            print(f"Processing time: {processing_time:.2f} seconds")  # Display the time of processing.

        except Exception as e:
            print("hunnn ?")
            return ""
        return query

# Function to execute commands
def run_SAM():
    speak_in_thread("I'm ready commander.")

    command_handlers = {
        'wikipedia': handle_wikipedia,
        'open youtube and search': handle_youtube_search,  # Restored handle_youtube_search
        'open google and search': handle_google_search,
        'recycle bin': handle_recycle_bin,
        'what is the time': handle_time,
        'open google': handle_open_google,
        'open youtube': handle_open_youtube,
        'open app': handle_launch_app,
        'send message': handle_whatsapp_message,
        'search file': handle_search,
        'depart': handle_exit
    }

    while True:
        query = take_command().lower()
        wake_word = "sam"
        if wake_word in query:


            for command, handler in command_handlers.items():
                if command in query:
                # Handle YouTube search in a separate thread
                    if command == "open youtube and search":
                    # Start the search in a separate thread
                        ind = query.split().index("search")
                        search = query.split()[ind + 1:]
                        search_thread = threading.Thread(target=webbrowser.open, args=("https://youtube.com/results?search_query=" + "+".join(search),))
                        search_thread.start()
                        speak_in_thread("Searching on youtube...")  # Speak first
                        speak_in_thread("Here's what i found on youtube.")  # Speak second
                # Handle Google search in a separate thread
                    elif command == "open google and search":
                    # Start the search in a separate thread
                        ind = query.split().index("search")
                        results = query.split()[ind + 1:]
                        search_thread = threading.Thread(target=webbrowser.open, args=("https://www.google.com/search?q=" + "+".join(results),))
                        search_thread.start()
                        speak_in_thread('Searching on Google...')
                        speak_in_thread("Here's what i found on Google.")
                    elif command == "wikipedia":
                        speak_in_thread('Searching Wikipedia...')
                        query = query.replace("wikipedia", "")
                        try:
                            results = wikipedia.summary(query, sentences=5)
                            speak_in_thread("According to Wikipedia")
                            print(results)
                            speak_in_thread(results)
                        except wikipedia.exceptions.PageError:
                            speak_in_thread(f"No results found for {query} on Wikipedia.")
                    elif command == "recycle bin":
                        try:
                            winshell.recycle_bin().empty(confirm=True, show_progress=False, sound=True)
                            speak_in_thread("Recycle Bin is emptied.")
                        except Exception as e:
                            speak_in_thread("There was an error emptying the Recycle Bin.")
                    elif command == "what is the time":
                        strTime = datetime.datetime.now().strftime("%H:%M:%S")
                        speak_in_thread(f"The time is {strTime}")
                    elif command == "open google":
                        speak_in_thread("Sure SIR! Opening Google.")
                        webbrowser.open("https://google.com/")
                    elif command == "open youtube":
                        speak_in_thread("Sure SIR! Opening YouTube.")
                        webbrowser.open("https://youtube.com/")
                    elif command == "open app":
                        speak_in_thread("Sure Sir!")
                        handle_launch_app()
                    elif command == "send message":
                        speak_in_thread("Sure SIR!")
                        handle_whatsapp_message()
                    elif command == "search file":
                        speak_in_thread("Sure SIR!")
                        handle_search()
                    elif command == "depart":
                        handle_exit()
                        break
                    else:
                        thread = threading.Thread(target=handler, args=(query,))
                        thread.start()  # Start the handler in a separate thread
                    break  # Exit the loop if a handler is found
            else:
                speak_in_thread("I am sorry, I don't understand that command.")
                speak_in_thread("Didn't catch that.")

# Helper functions for each command
def handle_wikipedia(query):
    speak_in_thread('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=5)
        speak_in_thread("According to Wikipedia")
        print(results)
        speak_in_thread(results)
    except wikipedia.exceptions.PageError:
        speak_in_thread(f"No results found for {query} on Wikipedia.")

def handle_youtube_search(query):
    speak_in_thread("Searching on youtube...")
    ind = query.split().index("youtube")
    search = query.split()[ind + 1:]
    speak_in_thread("Here are some results.")
    # Start the search in a separate thread
    search_thread = threading.Thread(target=webbrowser.open, args=("https://youtube.com/results?search_query=" + "+".join(search),))
    search_thread.start()

def handle_google_search(query):
    speak_in_thread('Searching on Google...')
    ind = query.split().index("search")
    results = query.split()[ind + 1:]
    speak_in_thread("Here are some results.")
    webbrowser.open("https://www.google.com/search?q=" + "+".join(results))
    speak_in_thread(results)

def handle_recycle_bin(query):
    try:
        winshell.recycle_bin().empty(confirm=True, show_progress=False, sound=True)
        speak_in_thread("Recycle Bin is emptied.")
    except Exception as e:
        speak_in_thread("There was an error emptying the Recycle Bin.")

def handle_time(query):
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak_in_thread(f"The time is {strTime}")

def handle_open_google(query):
    speak_in_thread("Sure SIR! Opening Google.")
    webbrowser.open("https://google.com/")

def handle_open_youtube(query):
    speak_in_thread("Sure SIR! Opening YouTube.")
    webbrowser.open("https://youtube.com/")

def handle_launch_app():
    def load_app_dict(filename):
        app_dict = {}
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        app_name, app_id = line.split(',', 1)
                        app_dict[app_name.strip().lower()] = app_id.strip()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error loading app dictionary: {e}")
        return app_dict

    # Function to open an application using its app ID
    def open_app(app_dict, app_name):
        # Normalize user input to lowercase
        normalized_app_name = app_name.lower()

        # Find the best match using fuzzy search
        best_match = None
        lowest_distance = float('inf')  # Start with infinity for comparison
        for possible_name in app_dict.keys():
            distance = Levenshtein.distance(normalized_app_name, possible_name)
            if distance < lowest_distance:
                lowest_distance = distance
                best_match = possible_name

        if best_match:
            app_id = app_dict[best_match]
            command = f'powershell -command "Start-Process shell:AppsFolder\\{app_id}"'
            subprocess.Popen(command, shell=True)
            speak_in_thread(f'Opening {app_name} (matched with: {best_match})...')
        else:
            print(f'App "{app_name}" not found in the dictionary.')

    # Function to handle applications with hardcoded paths
    def open_application(file_path):
        try:
            os.startfile(file_path)
        except FileNotFoundError:
            print("File not found!")
        except Exception as e:
            print(f"Error occurred while opening '{file_path}': {e}")

    # Function to ask for application name and return the appropriate path or ID
    def ask_for_application():
        appname = take_command().strip()

        # Define hardcoded_apps dictionary here
        hardcoded_apps = {
            "pycharm": r'C:\Program Files\JetBrains\PyCharm Community Edition 2024.1\bin\pycharm64.exe',
            "vs code": r'C:\Users\himan\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            "bluestacks": r'C:\Program Files\BlueStacks_nxt\HD-Player.exe',
            "epicgames": r'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe',
            "filmora": r'C:\Users\himan\AppData\Local\Wondershare\Wondershare Filmora (CPC)\Wondershare Filmora Launcher.exe'
        }

        # Combine hardcoded_apps and apps.txt into a single dictionary
        all_apps = {
            **hardcoded_apps,  # Corrected: Include hardcoded_apps
            **load_app_dict('apps.txt')
        }

        # Find the best match using fuzzy search
        best_match = None
        lowest_distance = float('inf')  # Start with infinity for comparison
        for possible_name in all_apps.keys():
            distance = Levenshtein.distance(appname.lower(), possible_name)
            if distance < lowest_distance:
                lowest_distance = distance
                best_match = possible_name

        if best_match:
            if best_match in hardcoded_apps:
                return hardcoded_apps[best_match]
            else:  # App ID from apps.txt
                app_dict = all_apps
                app_name = best_match
                return open_app(app_dict, app_name)
        else:
            print(f'App "{appname}" not found.')
            return None

    # Main function to run the application
    def main():
        speak_in_thread("Which app do you like me to open.")

        file_path = ask_for_application()
        if file_path:  # Check if file_path is not None
            open_application(file_path)
        else:
            print(f'Application not found.')

    main()

def handle_whatsapp_message():

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()

    # Create a table for contacts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    ''')

    conn.commit()

    # Function to add a contact
    def add_contact(name, phone):
        cursor.execute('''
        INSERT INTO contacts (name, phone)
        VALUES (?, ?)
        ''', (name, phone))
        conn.commit()

    # Function to get a contact's phone number by name
    def get_contact_number(name):
        cursor.execute('SELECT phone FROM contacts WHERE name = ?', (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    # Function to send a WhatsApp message
    def send_whatsapp_message(contact_name, message):
        phone_number = get_contact_number(contact_name)
        if phone_number:
            pywhatkit.sendwhatmsg_instantly(f'+{phone_number}', message)
            speak_in_thread(f'Message sent to {contact_name}')
        else:
            speak_in_thread(f'Contact {contact_name} not found')

    # Function to load contacts from a text file
    def load_contacts_from_file(file_path):
        with open(r'C:\Users\himan\PycharmProjects\My Voice Assistant SAM\Whatsapp_contacts.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    name, phone = parts
                    add_contact(name, phone)

    # Function to save contacts to a text file
    def save_contacts_to_file(file_path):
        cursor.execute('SELECT name, phone FROM contacts')
        contacts = cursor.fetchall()
        with open(file_path, 'w') as file:
            for contact in contacts:
                file.write(f'{contact[0]},{contact[1]}\n')
                speak_in_thread("Message sent successfully.")
    def clear_file(path_to_file):
        # Check if the file exists
        if os.path.isfile(path_to_file):
            # Open the file in write mode to clear its contents
            with open(path_to_file, 'w'):
                pass
            print(f"The contents of file have been cleared.")
        else:
            print(f"Error: Path does not exist.")


    # Main function to interact with the user
    def main_2():
        speak_in_thread("Loading Contacts..")
        load_contacts_from_file('contacts.txt')
        while True:
            choice = "send"

            if choice == 'add':
                speak_in_thread("Tell me the name that you want to save.")
                name = input("Enter: ")
                speak_in_thread(f"Now Please enter the number of {name}")
                phone = input("Enter: ")
                add_contact(name, phone)
                speak_in_thread(f'Contact {name} created successfully.')
                save_contacts_to_file('contacts.txt')
                speak_in_thread("Do you like me to do more with whatsapp. If want say yes. Else say no.")
                user_say = take_command().lower()
                if user_say == "yes":
                    continue
                elif user_say == "no":
                    break
            elif choice == 'send':
                speak_in_thread("Please tell me the name to whom you want to send message.")
                name = take_command()
                speak_in_thread(f"Now tell me the message you want to send to {name}")
                message = take_command()
                speak_in_thread(f"Sending message to {name}.")
                send_whatsapp_message(name, message)
                speak_in_thread("Do you like me to do more with whatsapp. If want say yes. Else say no.")
                user_say = take_command().lower()
                if user_say == "yes":
                    continue
                elif user_say == "no":
                    break
            elif choice == 'exit':
                break
            else:
                speak_in_thread("Invalid choice. Please try again.")

    main_2()

    path_to_file = r'C:\Users\himan\PycharmProjects\My Voice Assistant SAM\PyWhatKit_DB.txt'
    clear_file(path_to_file)


def handle_search():
    def build_index(root_dir, file_types):
        index = {}
        for root, _, files in os.walk(root_dir):
            for name in files:
                if name.endswith(tuple(ft for ft in file_types)) or file_types[0] == "":
                    index[name.lower()] = os.path.join(root, name)
        return index

    def ask_user_to_open_or_print_or_share_file(file_path):
        while True:
            speak_in_thread(f"Do you want to open or print or share '{filename}'?")
            choice = take_command().lower()
            if choice == 'open':
                open_file(file_path)
                break
            elif choice == 'print':
                print_selected_file(file_path)
                break
            elif choice == 'share':
                speak_in_thread("Sharing the file to your phone.")
                share_file(file_path)
                break
            else:
                print("Invalid choice. Please enter 'open', 'print', or 'share'.")

    def share_file(file_path):

        # Define the coordinates for the 'Add File' button
        ADD_FILE_X = 666  # Replace with the actual x-coordinate
        ADD_FILE_Y = 444  # Replace with the actual y-coordinate

        def open_intel_unison():
            # Open the Start menu
            pyautogui.press('win')
            time.sleep(1)

            # Type "Intel Unison" to search for the app
            pyautogui.write('Intel Unison')
            time.sleep(2)  # Wait for search results to appear

            # Select the first result (assuming it's the right one) and press Enter
            pyautogui.press('enter')
            time.sleep(10)  # Wait for the app to launch

        def click_at_coordinates(x, y):
            # Click at the specified coordinates
            pyautogui.click(x, y)
            time.sleep(1)  # Wait for the click action to be processed

        def paste_file_path(file_path):
            # Simulate pasting the file path into the file dialog
            pyautogui.write(file_path)  # Type the file path
            pyautogui.press('enter')  # Confirm the file path entry
            time.sleep(1)

            # Open Intel Unison

        open_intel_unison()
        pyautogui.hotkey('win', 'up')
        click_at_coordinates(ADD_FILE_X, ADD_FILE_Y)
        paste_file_path(file_path)

    def open_file(file_path):
        try:
            os.startfile(file_path)
            speak_in_thread(f"Opening file: {filename}")
        except Exception as e:
            print(f"Failed to open file: {e}")

    def print_selected_file(file_path):
        try:
            os.startfile(file_path, "print")
            speak_in_thread(f"Printing file: {filename}")
        except Exception as e:
            print(f"Failed to print file: {e}")



    while True:
        root_dir = r'C:\Users\himan'
        speak_in_thread("Please provide me the file format of the file.")
        file_types = take_command().lower()
        speak_in_thread("Searching and Seperating files by their formats. Please wait..")
        start = time.process_time()

        file_types = file_types.split(" ")
        file_index = build_index(root_dir, file_types)
        stop = time.process_time()
        time_taken = (stop - start)
        print(time_taken)

        speak_in_thread("Please provide me the file name.")
        search_query = take_command().lower()
        if search_query == "":
            speak_in_thread("Please enter a search query.")
            continue

        search_query_lower = search_query.lower()
        matches = []
        for filename, filepath in file_index.items():
            if fuzz.token_sort_ratio(search_query_lower, filename) > 50:
                matches.append(filepath)

        if matches:
            print("Matches:")
            for i, match in enumerate(matches, start=1):
                print(f"{i}. {match}")

            speak_in_thread("Please provide me the index number of the file you want to open, print or share.")
            time.sleep(2)
            selected_number = input("Enter: ")
            try:
                selected_index = int(selected_number) - 1
                if 0 <= selected_index < len(matches):
                    ask_user_to_open_or_print_or_share_file(matches[selected_index])
                    speak_in_thread("Do you want me to open more files. Say yes or no.")
                    ask = take_command().lower()
                    if ask == "yes":
                        continue
                    elif ask == "no":
                        break
                else:
                    print("Invalid selection. Please choose a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            speak_in_thread("No matches found.")
            break


def handle_exit():
    speak_in_thread("Goodbye Sir!")
    exit()

if __name__ == "__main__":
    run_SAM()