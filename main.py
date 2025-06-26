
import os
import dotenv
import requests


dotenv.load_dotenv()

API_KEY = os.getenv("WEATHER_API")

def weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q' : city,
        'appid' : API_KEY,
        'units' : 'metric'
    }
    response = requests.get(base_url,params=params)

    if response.status_code == 200 :
        data = response.json()
        print("\n🌤️ Weather in", data['name'])
        print("Country:", data['sys']['country'])
        print("Temperature:", data['main']['temp'], "°C")
        print("Feels like:", data['main']['feels_like'], "°C")
        print("Humidity:", data['main']['humidity'], "%")
        print("Description:", data['weather'][0]['description'].title())
    else:
        print("❌ Error fetching weather data.")
        print("HTTP Status Code:", response.status_code)
        print("Response text:", response.text)

city = str(input("enter your city name : "))
weather(city)