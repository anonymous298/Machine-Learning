import speech_recognition as sr
import pyttsx3
import requests
import pyautogui

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't get that.")
            return ""
        except sr.RequestError:
            speak("Sorry, the service is down.")
            return ""

def get_weather(city):
    api_key = "your_api_key_here"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == "404":
        speak("City not found.")
    else:
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(f"The weather in {city} is {weather} with a temperature of {temperature - 273.15:.2f}°C.")

def open_application(app_name):
    if app_name == "notepad":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('notepad')
        pyautogui.press('enter')
        speak(f"{app_name} is now open.")

def main():
    speak("Hello, I am your assistant. How can I help you today?")
    while True:
        command = listen()
        if "weather" in command:
            speak("Please say the city name.")
            city = listen()
            get_weather(city)
        elif "open" in command:
            app_name = command.split("open ")[-1]
            open_application(app_name)
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    main()
