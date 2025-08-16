import requests

API_KEY = "4bff826965693ff8aa51d19dc41160b8"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    parameters={'q':city, 'appid':API_KEY, 'units':"metric"}
    response= requests.get(BASE_URL, params=parameters)
    if response.status_code==200:
        data = response.json()
        print(f"City: {data['name']}")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Weather: {data['weather'][0]['description']}")
    else:
        print("Error- You hurt Hitler")

def get_forecast(city):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        forecast_item = data["list"][0]
        forecast_temp = forecast_item["main"]["temp"]
        pop = forecast_item.get("pop", 0)
        print(f"Future temperature: {forecast_temp}\\u00B0C")
        print(f"Chance of rain: {pop * 100}\\%")
    else:
        print("Error fetching forecast")

city_name=input("Enter City name")
get_weather(city_name)
get_forecast(city_name)