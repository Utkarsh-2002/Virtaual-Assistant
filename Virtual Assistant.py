#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install pyttsx3
pip install speechRecognition
pip install pyaudio
pip install wikipedia


# In[ ]:


import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import requests

engine = pyttsx3.init('sapi5')    # speech API
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()



# Movie recommendations
movie_recommendations = {
    'action': ['The Avengers', 'Mission: Impossible', 'Die Hard'],
    'adventure': ['Indiana Jones', 'Jurassic Park', 'Avatar'],
    'sci-fi': ['The Matrix', 'Blade Runner', 'Inception'],
    'comedy': ['Anchorman', 'Superbad', 'Bridesmaids'],
    'romance': ['The Notebook', 'La La Land', 'Casablanca'],
    'drama': ['The Shawshank Redemption', 'The Godfather', 'Schindler\'s List'],
    'mystery': ['Gone Girl', 'Sherlock Holmes', 'Memento'],
    'thriller': ['The Silence of the Lambs', 'Se7en', 'Prisoners'],
    # Add more movie recommendations here
}

def generate_movie_recommendations(genre):
    recommendations = movie_recommendations.get(genre.lower(), [])
   
    
            
    
    # Randomly select a subset of recommendations
    random.shuffle(recommendations)
    recommendations = recommendations[:5]  # Select top 5 recommendations
    
    return recommendations

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hi, I am Zara. How may I help you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')
    server.sendmail('your-email@gmail.com', to, content)
    server.close()


def get_weather():
    api_key = 'YOUR_API'  # Replace with your actual OpenWeatherMap API key
    base_url = 'https://api.openweathermap.org/data/2.5/weather?q='
    city = 'CITY'  # Replace with the desired city
    complete_url = base_url + city + '&appid=' + api_key

    response = requests.get(complete_url)
    data = response.json()

    if data['cod'] != '404':
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']

        weather_info = f"The weather in {city} is {weather_description}. "                        f"The temperature is {temperature} Kelvin, and the humidity is {humidity}%."
        speak(weather_info)
        print(weather_info)
    else:
        speak("Sorry, I couldn't fetch the weather information.")


def get_news():
    api_key = 'API_KEY'  # Replace with your actual NewsAPI key
    news_url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    response = requests.get(news_url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles']
        for article in articles:
            title = article['title']
            speak(title)
            print(title)
    else:
        speak("Sorry, I couldn't fetch the news updates.")


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'recommend movie' in query:
            speak('Sure! please tell me the genre')
            genre = takeCommand().lower()
            recommendations = generate_movie_recommendations(genre)
            if recommendations:
                speak(f"Here are some movie recommendations for {genre}:")
                for movie in recommendations:
                    speak(movie)
            else:
                speak("Sorry, I couldn't find any recommendations for you.")
                
                
        elif 'stop' in query:
            speak('Stopping...')
            break   
    
    
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open ai' in query:
            webbrowser.open("openai.com")

        elif 'play music' in query:
            music_dir = 'D:\\Songs'
            songs = os.listdir(music_dir)
            random_song = random.choice(songs)
            song_path = os.path.join(music_dir, random_song)
            os.startfile(song_path)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open code' in query:
            codepath = "E:\Microsoft VS Code\Code.exe"
            os.startfile(codepath)

        elif 'email to utkarsh' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "youremail@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email.")

        elif 'weather' in query:
            get_weather()

        elif 'news' in query:
            get_news()

