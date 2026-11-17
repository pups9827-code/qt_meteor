import requests

API_URL = "https://api.open-meteo.com/v1/forecast"


def get_forecast(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",       # Температура
            "wind_speed_10m",       # Ветер
            "surface_pressure",     # Давление
            "relative_humidity_2m", # Влажность
            "uv_index",             # УФ-индекс
            "cloud_cover",          # Облачность
            "precipitation",        # Осадки
        ],
        "wind_speed_unit": "ms",    # Ветер
        "forecast_hours": 24,
        "timezone": "auto",
    }

    response = requests.get(API_URL, params=params, timeout=20)
    response.raise_for_status()

    return response.json()