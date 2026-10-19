import requests  # билблиотека которая отпраляет запрос в интерент

API_URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude" : 55.664538,
    "longitude": 37.453783,
    "hourly": "temperature_2m",
}

response = requests.get(API_URL, params=params, timeout=20)
print(response.status_code) # если 200 то успешно

data = response.json() # преобразует json ответ в python ответ

print(data["hourly"]["time"][0])
print(data["hourly"]["temperature_2m"][0])