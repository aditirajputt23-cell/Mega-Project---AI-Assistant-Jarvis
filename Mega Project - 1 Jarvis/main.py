import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import google.generativeai as genai



# Replace with your NEW Gemini API key
genai.configure(api_key="<Your API key>")

model = genai.GenerativeModel("gemini-2.5-flash")

newsapi = "bce38f337213fc2027c6a8b4b554248c"

recognizer = sr.Recognizer()
engine = pyttsx3.init()




def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")




def aiProcess(command):
    prompt = f"""
You are a virtual assistant named Jarvis.
Give short and helpful responses.

User: {command}
"""

    response = model.generate_content(prompt)
    return response.text



# COMMANDS


def processCommand(c):

    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):

        song = c.replace("play", "").strip()

        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
        else:
            speak("Sorry, I couldn't find that song.")

    elif "news" in c:

        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if r.status_code == 200:

            data = r.json()

            articles = data.get("articles", [])

            for article in articles[:5]:
                speak(article["title"])

    else:
        output = aiProcess(c)
        speak(output)




if __name__ == "__main__":

    speak("Initializing Jarvis")

    while True:

        print("Recognizing...")

        try:

            with sr.Microphone() as source:

                recognizer.adjust_for_ambient_noise(source, duration=1)

                print("Listening...")

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            word = recognizer.recognize_google(audio)

            print("You said:", word)

            if "jarvis" in word.lower():

                speak("Yes?")

                with sr.Microphone() as source:

                    print("Jarvis Active...")

                    recognizer.adjust_for_ambient_noise(source, duration=0.5)

                    audio = recognizer.listen(source)

                    command = recognizer.recognize_google(audio)

                    print("Command:", command)

                    processCommand(command)

        except Exception as e:
            print("Error:", e)    