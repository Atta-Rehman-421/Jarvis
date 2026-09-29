import speech_recognition as sr
import webbrowser
import musicLibrary
import pyttsx3
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv



recognize = sr.Recognizer()
newsapi = os.getenv("NEWS_API")
load_dotenv()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)   
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1")

    completion = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "system",
            "content": "You are a virtual assistant named Jarvis."
        },
        {
            "role": "user",
            "content": command
        }
    ]
)

    return completion.choices[0].message.content
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
        song = c.split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        # Check if the request was successful
        if r.status_code == 200:
            # Convert JSON response into Python dictionary
            data = r.json()
            articles = data.get("articles",[]) 
            # Loop through all news articles
            for article in articles:
                speak(article["title"])
    elif command in c:
            # Remove "search google for" from the user's
            search = command.replace("search youtube for", "").strip()

            webbrowser.open(
                "https://www.youtube.com/search?q=" + search.replace(" ", "+")
            )
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    # it is for to wakeup "Jarvis"
    while True:
        r = sr.Recognizer()

        # It is used for recognizing speech 
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1.5)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listening for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except sr.RequestError as e:
            print("Google Speech Recognition error:", e)
        except Exception as e:
            print("Error:{0}".format(e))