
"""module imported"""
# run the command on termianl
# pip install pyttsx3 wikipedia pywhatkit requests pyjokes

# datetime for time in hours
import datetime
# speech_recognition to recognize the voice
import speech_recognition as sr
# pyttsx3 to speak the text
import pyttsx3
# wikipedia to search on wikipedia
import wikipedia
# webbrowser to open websites
import webbrowser
# pywhatkit to play youtube videos
import pywhatkit as kit
# requests to check the url is correct or not
import requests
# os to start application
import os
# smtplib to send emails
import smtplib
# pyjokes for random jokes 
import pyjokes

# intilize pyttsx3 and seting the voice 
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voices",voices[0].id)

class Shiva:

    def speak(self, text):
        """function to speak the text"""
        engine.say(text)
        print(text)
        engine.runAndWait()

    def greeting(self):
        """for greeting, for example: good morning, good afternoon"""
        greet = datetime.datetime.now().hour
        if greet >= 0 and greet <= 12:
            self.speak("Good Morning")
        elif greet > 12 and greet < 18:
            self.speak("Good Afternoon")
        else:
            self.speak("Good Evening.")
        self.speak("Have a good day.")

    def listening():
        """Taking micrrophoneinput and return string output"""

        voice = sr.Recognizer()
        with sr.Microphone() as mic:
            print("I can hear you....")
            voice.adjust_for_ambient_noise(mic)
            voice.pause_threshold = 1.5 # try all the parameters
            audio = voice.listen(mic)
        try:
            query = voice.recognize_google(audio, language="en-in")
        except Exception:
            pass
        return query

    
    def execution(self):
        """main function for execution on query"""
        query = self.listening().lower()
        print(query)
        
        # starting appliction
        if "application" in query:
            query = query.split(" ")
            try:
                if "open" in query:
                    self.speak(f"opening {query[1]}")
                    os.startfile(query[1])
                    self.speak(f"{query[1]} opened")
                else:
                    self.speak(f"opening {query[0]}")
                    os.startfile(query[0])
                    self.speak(f"{query[0]} opened")

            # checking the path on "file_path.txt" if not present asking to the user if he/she wants to add that appication so, next time you can run that application just saying application name
            except FileNotFoundError:
                file  = open("file_path.txt")
                file_data = [data.split(",") for data in file.readlines()]
                file.close()
                paths = [path[1][:-1] for path in file_data]
                names = [name[0] for name in file_data]
                for path, name in zip(paths, names):
                    if os.path.exists(path) == True and name == query[1]:
                        os.startfile(path)
                        self.speak(f"{query[1]} opened")
                        return ""

                self.speak("sorry can not find the application! If you want to open that application, say \"yes\" than type the path and application name or say \"no\" to return")
                while True:
                    try:
                        additional_features = self.listening(prompt="say yes or no").lower()
                        print(additional_features)
                        if additional_features == "yes":
                            self.speak("enter the path of application")
                            path = input("emter the name of application")
                            self.speak("")
                            app_name = input()
                            self.speak("wait a minute, I am checking the path")
                            
                            if os.path.exists(path) == True:
                                self.speak(f"path checking completed sucessfully")
                                self.speak("setting the path")
                                with open("file_path.txt", "a") as file:
                                    file.write(f"{app_name},{path}\n")
                                self.speak(f"path set sucessfully. Now you can open this application by calling \"open {app_name} application\"")
                            else:
                                self.speak("path not found")
                                continue
                            break
                        
                        elif additional_features == "no":
                            self.speak("ok!")
                            break
                    except Exception:
                        pass
            
        # opening websites
        elif "open" in query:
            try:
                query = query.split(" ")
                url = f"https://{query[-1]}.com"
                self.speak(f"Searching {query[-1]}.com on web, it may take minutes.")
                requests.get(url)
                self.speak(f"opening {query[-1]}")
                webbrowser.open(url)
            except Exception:
                self.speak(f"can not find {query[-1]}.com on web")
        
        # searching on youtube
        elif ("on youtube" in query or "in youtube" in query) and "play" not in query:
            query = query.split(" ")            
            
            if "search" in query:
                query = query[1]
            else:
                query = query[0]

            self.speak(f"searching {query} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

        # playing videos on youtube
        elif "play" in query:
            query = query.replace("play", "")
            query = query.replace("on youtube", "")
            self.speak(f"Playing {query} on YouTube")
            kit.playonyt(query)

        # seacrching on wikipedia
        elif "wikipedia" in query:
            query = query.replace("wikipedia", "")
            self.speak(f"According to wikipedia: {wikipedia.summary(query, 2)}")
        
        # for time
        elif "the time" in query or "current time" in query or "time right now" in query or "right now time" in query:
            self.speak(f"The Time is {datetime.datetime.now().strftime('%H:%M:%S')}")

        # sending email
        elif "send email" in query:
            self.speak("ok! type the mail address")
            reciver = input("Enter mail address: ")
            self.speak(f"What you want to send to {reciver}?")
            content = self.listening()
            self.speak(f"sending {content} to {reciver}")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('faltuhello1234@gmail.com', 'Faltu@hello123')
            server.sendmail('faltuhello1234@gmail.com', reciver, content)
            server.close()
            self.speak(f"email send to {reciver}")

        # for random joke
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            self.speak(joke)

        # exiting the programe
        elif "quit" in query:
            self.speak("Thanks for using, bye bye!")
            exit()

        # if all the above staement not match so, going to google and search for it
        else:
            self.speak(f"searching on google")
            webbrowser.open(f"https://google.com/search?q={query}")


shiva = Shiva()
shiva.greeting()
while True:
    try:
        shiva.execution()
    except Exception:
        pass
    