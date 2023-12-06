import pyttsx3 ; import datetime ; import speech_recognition as sr ; from scapy.all import sniff

import wikipedia as wiki ; import smtplib

import webbrowser as wb ; import os ; import pyautogui ; import psutil ; import pyjokes ; import requests

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say(" Hello Med Amine !!")
engine.runAndWait()


def speak(audio):
    engine.say (audio)
    engine.runAndWait()

def time() :
    #time = datetime.datetime.now().strftime("%Y-%m-%d")
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    speak(hour)
    speak(minute)
#time()

def wishme() :
    current_hour = int (datetime.datetime.now().hour)
    if current_hour >= 6 and current_hour < 12:
        speak("i hope you doing well , Good Morning , how can i assist you")
    elif current_hour >= 12 and current_hour <18 :
        speak("i hope you doing well , Good Afternoon , how can i assist you")
    elif current_hour >= 18 and current_hour < 24:
        speak("i hope you doing well , Good Evening , how can i assist you")
    else:
        speak("Good Night")
#wishme()


def date() :
    year = int  (datetime.datetime.now().year)
    month = int (datetime.datetime.now().month)
    day = int (datetime.datetime.now().day)
    speak(day)
    speak(month)
    speak(year)
#date()


def command_orders():
    micro = sr.Microphone()
    recognizer = sr.Recognizer()
    with micro as source:
        print("im listening ...")
        #speak("im listening ...")
        recognizer.pause_threshold = 0.5
        audio = recognizer.listen(source)
    try:
        print("recognizing ...")
        query = recognizer.recognize_google(audio, language="en-uk")
        print(query)

    except Exception as e:
        print(e)
        print("Im Sorry i can't hear youu Properly , say it again")
        return "None"
    return query

#command_orders()


def send_mail(to,content) :
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login("" , "****")
    server.sendmail("",to,content)

def screenshot() :
    img = pyautogui.screenshot()
    img.save("screenshot.png")


def cpu() :
    cpu_usage = str(psutil.cpu_percent())
    speak((cpu_usage))


def battery () :
    battery = psutil.sensors_battery()
    speak(battery.percent)


def capture_network_traffic(interface, num_packets):
    packets = sniff(iface=interface, count=num_packets)
    print(f"{len(packets)} packets captured successfully !")
    return packets


def analyse_packets(packets):
    for packet in packets:
        print(packet.summary())


def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        speak(f"Weather in {city}:")
        speak(f"Temperature: {data['main']['temp']}°C")
        speak(f"Description: {data['weather'][0]['description']}")
        speak(f"Humidity: {data['main']['humidity']}%")
    else:
        speak(f"Error: Unable to retrieve weather data. Status code: {response.status_code}")


if __name__ == '__main__':
    wishme()
    while True:
        query =command_orders().lower()

        if "time" in query :
            speak("the current time is")
            time()

        elif "date" in query :
            speak("the current date is")
            date()

        elif "your name" in query :
            speak("My name is Mohamed Amine")

        elif "wikipedia" in query :
            speak("Searching ...")
            query = query.replace("wikipedia", "")
            result = wiki.summary(query,sentences=2)
            print(result)
            speak(result)

        elif "search in google" in query:
            speak("what should i search !")
            search = command_orders().lower()
            print(search)
            #wb.open_new_tab(search+".com")
            wb.open_new_tab(search)

        elif "send email" in query :
            try :
                speak("what should i say !")
                content = command_orders()
                to=""
                send_mail(to, content)
                speak("email has been sent successfully")
            except Exception as e :
                print(e)
                speak("there is something wrong , please try again")
        elif "save this" in query :
            speak("what should i save !")
            data = command_orders()
            speak("as i remember you said !"+ data)
            remember = open("data.txt","w")
            remember.write(data)
            remember.close()
        elif "log out" in query :
            os.system("shutdown /l")
        elif "shutdown" in query :
            os.system(" shutdown /s")
        elif "restart" in query :
            os.system(" shutdown /r")
        elif "offline" in query :
            quit()
        elif "screenshot" in query :
            screenshot()
            speak("Done ")

        elif "cpu" in query :
            cpu()
        elif "battery " in query :
            battery()

        elif "joke" in query:
            try:
                jokes=pyjokes.get_joke()
                print(jokes)
                speak(jokes)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        elif "sniffing network" in query :
            interface="Wi-Fi"
            speak("how many packets!")
            num_packets = command_orders()
            captured_packets = capture_network_traffic(interface,int(num_packets))
            analyse_packets(captured_packets)

        elif "weather" in query :
            api_key = 'ur api key'
            speak("for which country ! ")
            city_name = command_orders()
            get_weather(api_key, city_name)
