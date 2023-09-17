import requests
import datetime
import pytz
from django.shortcuts import render

# Create your views here.


def index(request):
    API_KEY = open(
        "C:\\Users\\lenovo\\Desktop\\Django_folder\\Weather-Cast\\weather_project\\API_KEY",
        "r",
    ).read()
    current_weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    )
    forecast_url = (
        "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"
    )

    if request.method == "POST":
        city1 = request.POST["city1"]
        city2 = request.POST.get("city2", None)

        weather_data1, daily_forcasts1 = fetch_weather_and_forcast(
            city1, API_KEY, current_weather_url, forecast_url
        )

        if city2:
            weather_data2, daily_forcasts2 = fetch_weather_and_forcast(
                city2, API_KEY, current_weather_url, forecast_url
            )
        else:
            weather_data2, daily_forcasts2 = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forcasts1": daily_forcasts1,
            "weather_data2": weather_data2,
            "daily_forcasts2": daily_forcasts2,
        }
        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_weather_and_forcast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    print(response)
    lat, lon = response["coord"]["lat"], response["coord"]["lon"]
    print(lat, lon)
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    print(forecast_response)

    weather_data = {
        "city": city,
        "temperature": round(response["main"]["temp"] - 273.15),
        "description": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"],
    }

    daily_forcasts = []
    for daily_data in forecast_response["list"][:5]:
        print(daily_data["dt"])
        print(
            datetime.datetime.fromtimestamp(
                daily_data["dt"], tz=pytz.timezone("Africa/Algiers")
            ).strftime("%A")
        )
        daily_forcasts.append(
            {
                "day": datetime.datetime.utcfromtimestamp(daily_data["dt"])
                .astimezone(pytz.timezone("Africa/Algiers"))
                .strftime("%A"),
                "min_temp": round(daily_data["main"]["temp_min"] - 273.15),
                "max_temp": round(daily_data["main"]["temp_max"] - 273.15),
                "description": daily_data["weather"][0]["description"],
                "icon": daily_data["weather"][0]["icon"],
            }
        )
    return weather_data, daily_forcasts
