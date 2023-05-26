from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import os
import requests
import json


geolocator = Nominatim(user_agent="WeatherCastBot")

load_dotenv()
API_KEY = os.getenv("YANDEX_API_KEY")


def get_weather(city):
    location = retrieve_coordinates(city)
    weather_data = retrieve_weather_data(location)

    weather_data_json = json.loads(weather_data)
    parsed_weather_data = parse_weather_data_json(weather_data_json)

    return parsed_weather_data


def retrieve_coordinates(city):
    location = geolocator.geocode(city)
    return location


def retrieve_weather_data(location):
    try:
        lat, lon = location.latitude, location.longitude
        url = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&limit=1'
        headers = {'X-Yandex-API-Key': API_KEY}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f'Error retrieving weather data - {response.status_code}')
            return None
    
        return response.text
    except Exception as e:
        print(f'ERROR: {e}')

    


def parse_weather_data_json(weather_data_json):
    weather_data = {}

    weather_data["country"] = weather_data_json['geo_object']['country']['name']
    weather_data["city"] = weather_data_json['geo_object']['locality']['name']
    weather_data["morning_temp"] = weather_data_json['forecasts'][0]['parts']['morning']['temp_avg']
    weather_data["day_temp"] = weather_data_json['forecasts'][0]['parts']['day']['temp_avg']
    weather_data["evening_temp"] = weather_data_json['forecasts'][0]['parts']['evening']['temp_avg']
    weather_data["sunrise"] = weather_data_json['forecasts'][0]['sunrise']
    weather_data["sunset"] = weather_data_json['forecasts'][0]['sunset']

    return weather_data