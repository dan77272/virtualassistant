import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import winapps
import subprocess
import webbrowser
from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}


def weather(city):
    city = city.replace("", "+")
    res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7'
                       f'&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    talk(location)
    talk(time)
    talk(info)
    talk(weather)


listener = sr.Recognizer()
eng = pyttsx3.init()
voices = eng.getProperty('voices')
eng.setProperty('voice', voices[1].id)
eng.setProperty('rate', 150)
eng.say("Hey, what can I do for you?")
eng.runAndWait()


def talk(command):
    eng.say(command)
    eng.runAndWait()


def receive_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            return command
    except:
        pass


def execute_command():
    command = receive_command()

    try:
        if 'play' in str(command).lower():
            talk(f"Now playing {str(command).split('play')[1]}")
            pywhatkit.playonyt(str(command).split("play")[1])

        myList = ['time is it', 'what is the time', 'the time']
        element = any(ele in command.lower() for ele in myList)
        if bool(element):
            now = datetime.datetime.now()
            current_time = now.strftime('%I:%M %p')
            talk(f"The current time is: {current_time}")

        myList = ['is the date', 'me the date']
        element = any(ele in command.lower() for ele in myList)
        if bool(element):
            now = datetime.datetime.today()
            current_time = now.strftime("%B %d, %Y")
            talk(f"The date today is: {current_time}")

        if 'search for' in str(command).lower():
            word = str(command).lower().replace("search for", '')[1:]
            url = f"https://en.wikipedia.org/wiki/{word.replace(' ', '_')}"
            webbrowser.open_new_tab(url)

        if 'open' in str(command).lower():
            app = command.replace('open', '')
            for item in winapps.search_installed(app[1:]):
                print(item.install_location)
                try:
                    subprocess.call(f"{item.install_location}" + f"\{app[1:]}")
                except FileNotFoundError:
                    talk("I'm sorry. I couldn't find the app.")
        elif 'joke' in str(command).lower():
            talk(pyjokes.get_joke())
        elif 'google' in str(command).lower():
            app = command.replace('Google', '')
            url = f"https://www.google.com.tr/search?q={app[1:]}"
            webbrowser.open_new_tab(url)

        elif 'weather' in str(command).lower():
            weather(command)
        elif 'goodbye' in str(command).lower():
            talk('Goodbye')
            exit()

    except AttributeError:
        talk("I couldn't catch that")
        execute_command()


execute_command()
