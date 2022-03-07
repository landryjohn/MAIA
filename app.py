import requests, pyttsx3, speech_recognition as sr

import utils, os
from random import choice
from decouple import config
from functions import api
from datetime import datetime
import brain
import termcolor, pyfiglet
import platform
from functions import zabbix_api

USERNAME = config('USER_NAME')
BOTNAME = config('BOTNAME')
TTS_DRIVER = 'sapi5' if 'windows' in platform.system().lower() else 'espeak'

# set the TTS engine
engine = pyttsx3.init(TTS_DRIVER)

# Set the rate of the assistant
engine.setProperty('rate', 170)

# Set the volume of the assistant
engine.setProperty('volume', 1.0)

# Set the voice of the assistant (Male) 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

api.USER_API_USERNAME = config('API_USERNAME')
api.USER_API_PASSWORD = config('API_PASSWORD')
api.BASE_URL = config('BASE_URL')

def speak(text:str) -> None :
    """Write the text passed in parameter"""
    print(f"🤖 {BOTNAME} parle...")
    # TODO : Addapt this to tts process 
    print(f"{BOTNAME} : {text}")
    # engine.say(text)
    # engine.runAndWait()

def greet_user() -> None:
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if 12 <= hour < 16 :
        speak(f"Bon après-midi {USERNAME}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USERNAME}") 
    else :
        speak(f"Bonjour {USERNAME}")
    speak(f"Je suis {BOTNAME}. Comment puis-je vous aider")

def listen_to_user_input() -> str : 
    """Listen to user, make STT conversion using SAPI5"""
    r = sr.Recognizer()
    # TODO : Addapt this to STT process 
    # with sr.Microphone(device_index=2) as source:
    #     print('\n\n\n\n\n👂 En écoute...')
    #     r.adjust_for_ambient_noise(source)
    #     r.pause_threshold = 2
    #     audio = r.listen(source)

    try:
        print('🤖 Traitement...')
        # TODO : change how user input query from manuel to STT
        # query = r.recognize_google(audio, language='fr-FR')
        query = input(">>> Saisir votre requête : ")
        if any([el in query for el in ['arrêter', 'sortir', 'arrêt', 'fin', 'terminer']]):
            speak('Au revoir')
            exit()
        else : 
            speak(choice(utils.opening_text))
            
    except Exception:
        speak('Désolé, Je ne comprends pas. Pouvez vous repeter ?')
        query = 'None'
    
    return query

def say_random_answer(intent): 
    speak(choice(intent["responses"]))

if __name__ == '__main__' :
    output = os.system("clear")
    count = 0 
    Authenticated = False 
    while not Authenticated : 
        access_key = input("Saisir la clé d'accès : ")
        Authenticated = access_key == config("ACCESS_KEY")
        if not Authenticated : 
            print("Clé d'authentifcation incorrecte")
            count += 1 
        if count > 3 : 
            print("Echec de l'authentification")
            exit()
    f = pyfiglet.Figlet(font='standard')
    print(termcolor.colored(f.renderText('... MAIA ...'), 'yellow'))
    print(f"Bienvenue dans votre session {config('USER_NAME')}")
    # try :
    #      TODO : Add API authentication 
    #     api.auth_user()
    # except Exception as error:
    #     print(error)

    greet_user()
    
    while True :
        query = listen_to_user_input()
        print("Utilisateur :", query)
        if query == "" : continue 
        intents = brain.class_prediction(query.lower(), brain.words, brain.classes)
        intent = brain.get_intent(intents, brain.data)
        print(intent["tag"])
        if intent["tag"] == 'grettings' : 
            say_random_answer(intent)
            speak("Comment puis-je vous aider ?")
        elif intent["tag"] == 'network_status' :
            say_random_answer(intent)
            resp = zabbix_api.network_status()
            print(resp)
        elif intent["tag"] == 'activity_status' :
            say_random_answer(intent)
            resp = zabbix_api.activity_status()
            print(resp)
        elif intent["tag"] == 'red_code' :
            say_random_answer(intent)
            print(termcolor.colored("[!] ACTIVATION DU CODE ROUGE [!]", color='red'))
        elif intent["tag"] == 'stop_maia' : 
            speak('Au revoir')
            exit()
        else :
            print(f"Commande : {intent['tag']}")
            speak('La fonctionnalité est en cours de développement')
