# This line is optional(I've added it for security, hiding my app_id)
from config import app_id

import speech_recognition as sr
import pyttsx3
import wolframalpha
import wikipedia
from datetime import datetime
import webbrowser
import subprocess
import pywhatkit

# Initializations...
running = True
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Voice Selection
select_voice = input("Select voice(Male/Female): ")
if select_voice.lower() == "male":
    name = "David"
    engine.setProperty('voice', voices[0].id)
else:
    name = "Zira"
    engine.setProperty('voice', voices[1].id)


# Initializations(WolframAlpha).
client = wolframalpha.Client(app_id)

# Speak Function...


def speak(text):
    print(f"{name}: {text}")
    engine.say(text)
    engine.runAndWait()


# Listen Function...
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"User: {command}")
        except:
            speak("I can't get that!")
            speak("Please try again.")
    return command


def intro():
    speak(f"Hi, I am {name}.")
    speak("I am your personal assistant!")


intro()
while running:
    command = listen().lower()
    if ("exit" or "bye") in command:
        speak("Exiting Program.")
        speak("Thank you for using me!")
        running = False

    elif "play on youtube" in command:
        speak("What is the title?")
        title = listen()
        pywhatkit.playonyt(title)
        speak(f"Searching for {title} on YouTube!")

    elif "take screenshot" in command:
        speak("Capturing Screenshot!")
        pywhatkit.take_screenshot()

    elif "notepad" in command:
        speak("Opening Notepad!")
        subprocess.run('notepad')

    elif "open camera" in command:
        speak("Okay!")
        subprocess.run('start microsoft.windows.camera:', shell=True)
        speak("I can see you through this!")

    elif ("shutdown" or "good bye") in command:
        speak("You will be logged out in a minute!")
        subprocess.run('shutdown /s')  # To shutdown
        subprocess.run('shutdown /r')  # To restart
        subprocess.run('shutdown /l')  # To logout
        speak("Shutting Down!")

    elif "your name" in command:
        speak("Hello, I am Zira!")

    elif "create file" in command:
        speak("Name of the file(without extension).")
        file_name = listen()
        with open(f"{file_name}.txt", 'w') as file:
            speak("Content of the file.")
            file_content = listen()
            file.write(file_content)
            speak("File created successfully!")

    elif "date" in command:
        date = datetime.now().date()
        speak(f"Today: {date}")

    elif "time" in command:
        time = datetime.now().time()
        speak(f"Current : {time}")

    else:
        try:
            if "wikipedia" in command:
                summary = wikipedia.summary(command, sentences=2)
                speak(summary)

            else:
                res = client.query(command)
                result = res.results
                speak(next(result).text)
        except:
            speak("I can't understand that!")
            speak("You can try searching on google instead")
            webbrowser.open('www.google.com')
