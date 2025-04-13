import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import time
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()  # Initialize the text to speech engine
newsapi = "df6f66ddcf834a53a4ef104fb32e111c"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save('hello.mp3')

    # Initialize the mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("hello.mp3")  # updated to correct filename

    # Play the music
    pygame.mixer.music.play()

    # Optional: Wait for music to finish
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    
    pygame.mixer.music.unload()
    os.remove("hello.mp3")  # Remove the file after playing


def aiprocess(text):
    client = OpenAI(
        api_key=""  # 🔒 Keep this safe
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Edith skilled in general tasks like Alexa and Google Assistant. Give short responses please."},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content


def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
        speak("okie sir opening Google")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
        speak("okie sir opening YouTube")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
        speak("okie sir opening Facebook")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
        speak("okie sir opening WhatsApp")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
        speak("okie sir opening LinkedIn")
    elif "open instagram" in c.lower():
        speak("okie sir opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, song not found.")
    elif "open news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
              speak(article['title'])
              time.sleep(0.5)  # Give a short break between audios

        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = aiprocess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing chanakya .........")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening .....")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                

            word = recognizer.recognize_google(audio)
            print("You said:", word)
            if word.lower() == "chanakya":
                speak("Yes sir")

                with sr.Microphone() as source:
                    print("chanakya active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    processcommand(command)

        except Exception as e:
            print("Error:", e)
