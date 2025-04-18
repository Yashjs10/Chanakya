import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
import time
import os
import re

recognizer = sr.Recognizer()
newsapi = "df6f66ddcf834a53a4ef104fb32e111c"

engine = pyttsx3.init()
# Set male voice
voices = engine.getProperty('voices')
for voice in voices:
    if 'male' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 160)  # Optional: slow down speech a bit

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

def speak(text):
    print("Speaking:", text)
    try:
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        engine.say(cleaned_text)
        engine.runAndWait()
    except Exception as e:
        print("Speak error:", e)

def aiprocess(text):
    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Edith skilled in general tasks like Alexa and Google Assistant. Give short responses please."},
                {"role": "user", "content": text}
            ],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=False
        )
        response = completion.choices[0].message.content
        print("AI Response:", response)
        return response
    except Exception as e:
        print("AI processing error:", e)
        return "Sorry, there was an error processing your request."

def processcommand(c):
    c = c.lower()
    if c in ["stop", "exit", "shutdown", "bye"]:
        speak("Shutting down sir. Goodbye!")
        exit()

    if "open google" in c:
        webbrowser.open("https://www.google.com")
        speak("okie sir opening Google")
    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com")
        speak("okie sir opening YouTube")
    elif "open facebook" in c:
        webbrowser.open("https://www.facebook.com")
        speak("okie sir opening Facebook")
    elif "open whatsapp" in c:
        webbrowser.open("https://web.whatsapp.com")
        speak("okie sir opening WhatsApp")
    elif "open linkedin" in c:
        webbrowser.open("https://www.linkedin.com")
        speak("okie sir opening LinkedIn")
    elif "open instagram" in c:
        speak("okie sir opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif c.startswith("play"):
        try:
            song = c.split(" ", 1)[1]
            link = musiclibrary.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                speak("Sorry, song not found.")
        except:
            speak("Please mention a song name.")
    elif "open news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles[:5]:
                    speak(article['title'])
                    time.sleep(0.5)
            else:
                speak("Sorry, I couldn't fetch the news.")
        except Exception as e:
            print("News error:", e)
            speak("There was an error fetching the news.")
    else:
        response = aiprocess(c)
        speak(response)

if __name__ == "__main__":
    speak("Initializing chanakya .........")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening .....")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)

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
