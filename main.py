import os
import win32com.client
import speech_recognition as sr
import webbrowser
import openai
from config import apikey
from AppOpener import open as op
from weather import w_api_key
import datetime
import requests
import locationtagger as lt


speaker = win32com.client.Dispatch("SAPI.SpVoice")
loop = 0

chatStr = ""


def talk(query):
    global chatStr
    # query = input("Enter your query: ")
    openai.api_key = apikey
    chatStr += f"Hari: {query}\n Nexus: "
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    speaker.Speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    print(chatStr)
    if "who created you" in query:
        speaker.Speak("I was created by Hari")
        print("I was created by Hari")
    if "when is your birthday" in query:
        speaker.Speak("I was born on 20th May 2023")
        print("I was born on 20th May 2023")
    return chatStr


def ai(prompt):
    openai.api_key = apikey
    text = prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    #print(response["choices"][0][text])
    text += response["choices"][0].get("text", "")
    file_path = f"Responses/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"

    if not os.path.exists("Responses"):
        os.makedirs("Responses")

    try:
        with open(file_path, "w") as f:
            f.write(text)
    except Exception as e:
        print(f"Error occurred while opening/writing to the file: {e}")


def tellTime():
    time = str(datetime.datetime.now())
    print(time)
    hour = time[11:13]
    min = time[14:16]
    speaker.Speak("The time is sir" + hour + "Hours and" + min + "Minutes")


def take_command():
    r = sr.Recognizer()

    # from the speech_Recognition module I use the Microphone module to
    # listen to the command
    with sr.Microphone() as source:
        print('Listening')

        # seconds of non-speaking audio before a phrase is considered complete
        #r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing")

            # for Listening the command in indian english we can also use 'hi-In'
            # for hindi recognizing
            Query = r.recognize_google(audio, language='en-in')
            #speaker.Speak(Query)
            print("the command printed = ", Query)
            return Query

        except Exception as e:
            print(e)
            speaker.Speak("Say that again sir")
            print("Say that again sir")
            return "None"


def Hello():
    hello = "Hi Hari, what can I assist you with today"
    speaker.Speak(hello)


def do_command():
    global chatStr
    Hello()
    while True:
        task = take_command().lower()
        if "open youtube" in task:
            speaker.Speak("Opening Youtube")
            webbrowser.open("www.youtube.com")
            continue
        elif "open google" in task:
            speaker.Speak("Opening Google")
            webbrowser.open("www.google.com")
            continue
        elif "the time" in task:
            tellTime()
        elif "open spotify" in task:
            speaker.Speak("Opening Spotify")
            op("spotify")
        elif "open notepad" in task:
            speaker.Speak("Opening Notepad")
            op("notepad")
        elif "using artificial intelligence" in task:
            ai(prompt=task)
        elif "lets talk":
            talk(task)
        if "terminate" in task or "exit" in task:
            global loop
            loop = 1
            speaker.Speak("Terminating")
            break
        if "erase chat history" in task:
            chatStr = ""
            speaker.Speak("Chat history erased")
        if "weather report" in task:
            def create_weather_report():
                api_key = w_api_key

                base_url = "http://api.openweathermap.org/data/2.5/weather?"

                place_entity = lt.find_locations(text=task)
                city_name = str(place_entity.cities)
                print(city_name)

                complete_url = base_url + "appid=" + api_key + "&q=" + city_name

                response = requests.get(complete_url)

                x = response.json()

                # Now x contains list of nested dictionaries
                # Check the value of "cod" key is equal to
                # "404", means city is found otherwise,
                # city is not found
                if x["cod"] != "404":

                    # store the value of "main"
                    # key in variable y
                    y = x["main"]

                    # store the value corresponding
                    # to the "temp" key of y
                    current_temperature = y["temp"]

                    # store the value corresponding
                    # to the "pressure" key of y
                    current_pressure = y["pressure"]

                    # store the value corresponding
                    # to the "humidity" key of y
                    current_humidity = y["humidity"]

                    # store the value of "weather"
                    # key in variable z
                    z = x["weather"]

                    # store the value corresponding
                    # to the "description" key at
                    # the 0th index of z
                    weather_description = z[0]["description"]

                    # print following values
                    print(" Temperature (in kelvin unit) = " +
                          str(current_temperature) +
                          "\n atmospheric pressure (in hPa unit) = " +
                          str(current_pressure) +
                          "\n humidity (in percentage) = " +
                          str(current_humidity) +
                          "\n description = " +
                          str(weather_description))
                    speaker.Speak(f"Temperature (in kelvin unit) = {current_temperature} \n atmospheric pressure (in hPa unit) = {current_pressure} \n humidity (in percentage) = {current_humidity} \n description = {weather_description}")

                else:
                    print(" City Not Found ")
            create_weather_report()


while loop == 0:
    do_command()
