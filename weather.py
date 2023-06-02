import requests
import json
import os

import requests


def get_weather_data(w_api_key, city_id):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "id": city_id,
        "units": "metric",
        "appid": w_api_key
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return data


w_api_key = "1ef1ead3c5a57b589e8bcb34d1c41588"
city_id = "1270642"  # Gurgaon

data = get_weather_data(w_api_key, city_id)
print(data)
