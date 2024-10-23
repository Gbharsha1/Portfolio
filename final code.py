import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
import subprocess
import random
import wolframalpha

                
class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.recognizer = sr.Recognizer()

        self.NEWS_API_KEY = '2456493e27044197b0f5885149f5d588'
        self.OPENWEATHERMAP_API_KEY = '227e5e941bb97b9e30f574782acccac0'

        self.text_output = None

    def wish_me(self):
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")

        self.speak("Hi. I am your personal voice assistant. Please tell me how can I help you")


    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again, please...")
            return "None"
        return query.lower()

    def start_voice_assistant(self):
        # Update the text_output attribute of the VoiceAssistant class
        self.text_output = self.text_output
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, "Voice Assistant is now running...\n")
        self.wish_me()

        while True:
            query = self.take_command().lower()

            if 'wikipedia' in query:
                self.speak('Sure, what would you like to search on Wikipedia?')
                search_query = self.take_command().lower()
                if search_query != 'none':
                    self.speak(f'Searching Wikipedia for {search_query}...')
                    results = wikipedia.summary(search_query, sentences=2)
                    self.speak(f"According to Wikipedia, {results}")
                    print(results)
                else:
                    self.speak("Sorry, I didn't catch that. Please try again.")

            elif 'recommend movies' in query or 'movie recommendations'in query or 'recommend' in query:
                self.recommend_movies()
            elif 'open google' in query:
                webbrowser.open("https://www.google.com/")
            
            elif 'youtube' in query or 'open youtube' in query:
                webbrowser.open("https://www.youtube.com/")
            elif 'plan a holiday' in query or 'holiday trip' in query or 'planning a holiday' in query:
                self.plan_holiday_trip()
        
            elif 'tell a joke' in query or 'joke' in query:
                self.tell_joke()
            
            elif 'set a reminder' in query or 'reminder' in query:
                self.set_remainder()
            
            elif 'motivation' in query or 'quote' in query:
                quote = self.get_daily_quote()
                self.speak(quote)

            elif 'calculate' in query or 'math' in query:
                self.speak("Sure, what mathematical operation would you like me to perform? You can choose addition, subtraction, multiplication, division, or percentage.")
                math_operation = self.take_command().lower()

                if math_operation in ['addition', 'subtraction', 'multiplication', 'division', 'percentage']:
                    self.speak(f"Please provide the values for the {math_operation}.")
                    self.speak("Value for A:")
                    value_a = float(self.take_command())
                    self.speak("Value for B:")
                    value_b = float(self.take_command())

                    if math_operation == 'addition':
                        result = value_a + value_b
                        self.speak(f"The sum of {value_a} and {value_b} is {result}")
                    elif math_operation == 'subtraction':
                        result = value_a - value_b
                        self.speak(f"The result of {value_a} minus {value_b} is {result}")
                    elif math_operation == 'multiplication':
                        result = value_a * value_b
                        self.speak(f"The product of {value_a} and {value_b} is {result}")
                    elif math_operation == 'division':
                        if value_b != 0:
                            result = value_a / value_b
                            self.speak(f"The result of {value_a} divided by {value_b} is {result}")
                        else:
                            self.speak("Error: Division by zero. Please provide a non-zero value for B.")
                    elif math_operation == 'percentage':
                        result = (value_a / value_b) * 100
                        self.speak(f"{value_a} is {result}% of {value_b}")
                else:
                    self.speak("Sorry, I didn't recognize that mathematical operation. Please try again.")

            elif 'what is the climate report' in query or 'weather report' in query:
                self.speak("Sure, which city would you like to get the weather report for?")
                city = self.take_command().lower()
                if city != 'none':
                    weather_reports = self.get_weather_report(self.OPENWEATHERMAP_API_KEY, city)
                    if weather_reports:
                        self.speak("Here is the weather report:")
                        for report in weather_reports:
                            self.speak(report)
                            print(report)
                    else:
                        self.speak("Sorry, I couldn't fetch the weather report. Please try again.")
                else:
                    self.speak("Sorry, I didn't catch that. Please try again.")

            elif 'play music' in query or 'music' in query or 'song' in query:
                self.speak("Do you want to play an internet song, a YouTube song, or a downloaded song?")
                response = self.take_command().lower()

                if 'internet' in response:
                    try:
                        self.speak("Sure, which internet song would you like to play?")
                        song_name = self.take_command()
                        self.search_google(song_name)
                        self.speak("I couldn't play the song, but I found the search results on Google.")
                    except Exception as e:
                        print(e)
                        self.speak("Sorry, I couldn't play the song .")

                elif 'youtube' in response:
                    self.speak("Select your song to play.")
                    song_name = self.take_command()
                    self.speak(f"Playing {song_name} on YouTube.")
                    self.play_youtube(song_name)

                elif 'downloaded' in response:
                    music_dir = 'C:\\Users\\gbhar\\Downloads\\Songs'
                    songs = os.listdir(music_dir)

                    if songs:
                        self.speak("Sure, here is the list of downloaded songs:")
                        for index, song in enumerate(songs, start=1):
                            print(f"{index}. {song}")

                        self.speak("Which downloaded song would you like to play?")
                        song_number = self.take_command()

                        try:
                            song_index = int(song_number)
                            if 1 <= song_index <= len(songs):
                                song_to_play = songs[song_index - 1]
                                self.speak(f"Playing {song_to_play}.")
                                os.startfile(os.path.join(music_dir, song_to_play))
                            else:
                                self.speak("Invalid selection. Please choose a valid song number.")
                        except ValueError:
                            self.speak("Sorry, I couldn't understand the song number.")
                    else:
                        self.speak("Sorry, no downloaded songs found.")


            elif 'the time' in query:
                current_time = datetime.datetime.now()
                strTime = current_time.strftime("%I:%M:%S %p")  
                current_date = current_time.strftime("%A, %B %d, %Y")  
                self.speak(f"Sir, the time is {strTime} and the date is {current_date}")

            elif 'play movies' in query:
                movie_dir = #give your movies location here  
                movies = os.listdir(movie_dir)

                if movies:
                    self.speak("Sure, here is the list of downloaded movies:")
                    for index, movie in enumerate(movies, start=1):
                        print(f"{index}. {movie}")

                    self.speak("Please tell me the name of the movie you want to play.")
                    movie_name = self.take_command()

                    # Check if the specified movie is in the list of downloaded movies
                    if any(movie_name.lower() in movie.lower() for movie in movies):
                        movie_to_play = next((movie for movie in movies if movie_name.lower() in movie.lower()), None)
                        self.speak(f"Playing {movie_to_play}.")
                        codePath = os.path.join(movie_dir, movie_to_play)
                        subprocess.Popen(['start', '""', codePath], shell=True)
                    else:
                        self.speak(f"Sorry, I couldn't find a movie with the name {movie_name}.")
                else:
                    self.speak("Sorry, no downloaded movies found.")

            elif 'tell news' in query or 'news' in query:
                headlines = self.get_news_headlines(self.NEWS_API_KEY)
                if headlines:
                    self.speak("Here are the latest news headlines:")
                    for i, headline in enumerate(headlines, 1):
                        self.speak(f"{i}. {headline}")
                        print(f"{i}. {headline}")
                else:
                    self.speak("Sorry, I couldn't fetch the latest news headlines. Please try again.")
            elif 'thank you' in query and 'happy' in query and 'bye' in query:
                self.speak("My pleasure to help you! Goodbye.")
                break

        
    def search_google(self, song_name):
        google_search_url = "https://www.google.com/search?q="
        search_query = song_name.replace(" ", "+")
        url = f"{google_search_url}{search_query}"
        webbrowser.open(url)
        self.speak(f"Here are the search results for {song_name} on Google.")

    def play_internet_song(self):
        try:
            self.speak("Sure, which internet song would you like to search for?")
            song_name = self.take_command()
            self.search_google(song_name)
            self.speak("I couldn't play the song, but I found the search results on Google.")
        except Exception as e:
            print(e)
            self.speak("Sorry, I encountered an error while trying to perform the Google search.")

    def get_destination_info(self, destination):
        try:
            self.speak(f"Gathering information about {destination}...")
            destination_info = wikipedia.summary(destination, sentences=2)
            self.speak(f"Here is some information about {destination}: {destination_info}")
            print(destination_info)
        except Exception as e:
            print(e)
            self.speak("Sorry, I couldn't fetch information about the destination. Please try again.")

    def get_famous_place_suggestion(self, destination, day):
        try:
            locations_by_day = {
                1: ["Location1_Day1", "Location2_Day1", "Location3_Day1"],
                2: ["Location1_Day2", "Location2_Day2", "Location3_Day2"],
            }
            self.speak(f"Finding a famous place to visit on Day {day} at {destination}...")
            locations = locations_by_day.get(day, [])
            if locations:
                location_names = ', '.join(locations)
                suggestion = f"For Day {day}, you can visit {location_names} in {destination}."
                self.speak(suggestion)
                print(suggestion)
            else:
                self.speak(f"Sorry, I couldn't fetch suggestions for Day {day}. Please try again.")
        except Exception as e:
            print(e)
            self.speak(f"Sorry, I couldn't fetch suggestions for Day {day}. Please try again.")

    def convert_to_days(self, time_value, time_unit):
        if time_unit == 'days':
            return time_value
        elif time_unit == 'weeks':
            return time_value * 7
        elif time_unit == 'months':
            return time_value * 30  
        elif time_unit == 'years':
            return time_value * 365  
        else:
            return None

    def parse_duration(self, duration_response):
        try:
            if any(unit in duration_response for unit in ['day', 'week', 'month', 'year']):
                duration_numeric = next((int(s) for s in duration_response.split() if s.isdigit()), None)
                duration_unit = next((s for s in duration_response.split() if any(unit in s for unit in ['day', 'week', 'month', 'year'])), None)

                if duration_numeric and duration_unit:
                    total_days = self.convert_to_days(duration_numeric, duration_unit)

                    if total_days:
                        return total_days
        except Exception as e:
            print(e)
        return None

    def plan_holiday_trip(self):
        self.speak("Great! Where do you want to go?")
        destination = self.take_command().lower()

        self.speak("How long are you planning to stay? You can specify the duration in days, weeks, months, or years.")
        duration_response = self.take_command().lower()

        total_days = self.parse_duration(duration_response)

        if total_days:
            self.speak(f"Awesome! Planning a trip to {destination} for {duration_response}. "
                f"Converted to approximately {total_days} days. Let me gather more information.")        
            self.get_destination_info(destination)
            for day in range(1, total_days + 1):
                self.speak(f"For Day {day}, here's a suggestion for a famous place to visit:")
                self.get_famous_place_suggestion(destination, day)

            print(f"Destination: {destination}")
            print(f"Duration: {duration_response} (Converted to {total_days} days)")
        else:
            self.speak("Sorry, I didn't catch the duration. Please try again.")

    def get_news_headlines(self, api_key):
        try:
            news_api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
            response = requests.get(news_api_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            news_data = response.json()
            headlines = [article['title'] for article in news_data.get('articles', [])]
            return headlines
        except Exception as e:
            print(e)
            return []

    def get_weather_report(self, api_key, city, days=2):
        try:
            print("Getting weather report...")
            weather_api_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'
            response = requests.get(weather_api_url)
            response.raise_for_status()
            weather_data = response.json()
            reports = []
            for day in range(days):
                date = datetime.datetime.fromtimestamp(weather_data['list'][day]['dt']).strftime('%Y-%m-%d')
                description = weather_data['list'][day]['weather'][0]['description']
                temperature_kelvin = weather_data['list'][day]['main']['temp']
                temperature_celsius = temperature_kelvin - 273.15 
                report = f"For {date}, the weather is {description} with a temperature of {temperature_celsius:.2f} degrees Celsius."
                reports.append(report)
                # print(report)
            return reports
        except Exception as e:
            print(e)
            return []

    def play_youtube(self, song_name):
        youtube_search_url = "https://www.youtube.com/results?search_query="
        search_query = song_name.replace(" ", "+")
        url = f"{youtube_search_url}{search_query}"
        webbrowser.open(url)

    def get_daily_quote(self):
        motivation = [
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "Do not wait to strike till the iron is hot, but make it hot by striking. - William Butler Yeats",
            "Life is what happens when you're busy making other plans. - Allen Saunders",
        ]
        return random.choice(motivation)

    def set_remainder(self):
        self.speak("Sure, what would you like to set a reminder for?")
        reminder_text = self.take_command().capitalize()

        self.speak("When would you like to be reminded? Please specify the time.")
        reminder_time = self.take_command().lower()

        print(f"Reminder set for: {reminder_text} at {reminder_time}")
        self.speak(f"Reminder set for: {reminder_text} at {reminder_time}")

    def perform_math_calculation(self, query):
        app_id = 'X5HPRJ-VTQV3UE7AV'  
        client = wolframalpha.Client(app_id)

        try:
            res = client.query(query)
            answer = next(res.results).text
            self.speak(f"The answer is {answer}")
        except Exception as e:
            print(e)
            self.speak("Sorry, I couldn't perform the calculation. Please try again.")

    def get_movie_recommendations(self, genre):
        try:
            api_key = '2570c868aeeae572f0432f1e1bdbfb49'
            base_url = 'https://api.themoviedb.org/3'
            genre_url = f'{base_url}/genre/movie/list?api_key={api_key}&language=en-US'
            response = requests.get(genre_url)
            genres = response.json()['genres']

            genre_id = next((g['id'] for g in genres if g['name'].lower() == genre.lower()), None)

            if genre_id:
                discover_url = f'{base_url}/discover/movie?api_key={api_key}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={genre_id}'
                response = requests.get(discover_url)
                movies = response.json()['results']

                if movies:
                    top_movies = movies[:3]
                    self.speak(f"Here are the top 3 movies in the {genre} genre:")
                    for i, movie in enumerate(top_movies, 1):
                        title = movie['title']
                        self.speak(f"{i}. {title}")
                        print(f"{i}. {title}")
                else:
                    self.speak(f"Sorry, I couldn't find any movies in the {genre} genre.")
            else:
                self.speak("Sorry, I couldn't recognize that genre. Please try again.")
        except Exception as e:
            print(e)
            self.speak("Sorry, I encountered an error while fetching movie recommendations. Please try again.")

    def print_all_genres(self):
        try:
            api_key = '2570c868aeeae572f0432f1e1bdbfb49'
            base_url = 'https://api.themoviedb.org/3'
            genre_url = f'{base_url}/genre/movie/list?api_key={api_key}&language=en-US'
            response = requests.get(genre_url)
            genres = response.json()['genres']

            print("Available Movie Genres:")
            for genre in genres:
                print(f"{genre['id']}. {genre['name']}")
        except Exception as e:
            print("Failed to fetch movie genres. Please try again.")

    def recommend_movies(self):
        self.print_all_genres()

        self.speak("Sure, what genre are you in the mood for?")
        user_genre = self.take_command().lower()

        if user_genre != 'none':
            self.get_movie_recommendations(user_genre)
        else:
            self.speak("Sorry, I didn't catch that. Please try again.")

class VoiceAssistantGUI:
    def __init__(self, master, voice_assistant):
        self.master = master
        master.title("Voice Assistant")

        self.voice_assistant = voice_assistant

        self.text_output = scrolledtext.ScrolledText(master, width=60, height=20)
        self.text_output.pack(padx=10, pady=10)

        self.button_start = tk.Button(master, text="Start Voice Assistant", command=self.start_voice_assistant)
        self.button_start.pack(pady=10)

        self.button_stop = tk.Button(master, text="Stop Voice Assistant", command=self.stop_voice_assistant)
        self.button_stop.pack(pady=5)

    def start_voice_assistant(self):
        # Pass the text_output attribute to the VoiceAssistant class
        self.voice_assistant.text_output = self.text_output
        self.voice_assistant.start_voice_assistant()

    def stop_voice_assistant(self):
        self.text_output.insert(tk.END, "Voice Assistant stopped.\n")
if __name__ == "__main__":
    class VoiceAssistantGUI:
        def __init__(self, master, voice_assistant):
            self.master = master
            master.title("Voice Assistant")

            self.voice_assistant = voice_assistant

            self.text_output = scrolledtext.ScrolledText(master, width=60, height=20)
            self.text_output.pack(padx=10, pady=10)

            self.button_start = tk.Button(master, text="Start Voice Assistant", command=self.start_voice_assistant)
            self.button_start.pack(pady=10)

            self.button_stop = tk.Button(master, text="Stop Voice Assistant", command=self.stop_voice_assistant)
            self.button_stop.pack(pady=5)

        def start_voice_assistant(self):
            self.voice_assistant.text_output = self.text_output
            self.voice_assistant.start_voice_assistant()

        def stop_voice_assistant(self):
            self.text_output.insert(tk.END, "Voice Assistant stopped.\n")


    root = tk.Tk()
    voice_assistant = VoiceAssistant()
    gui = VoiceAssistantGUI(root, voice_assistant)
    root.mainloop()
