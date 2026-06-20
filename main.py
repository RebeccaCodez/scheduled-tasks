import os
import requests
from twilio.rest import Client



OpenWeatherMap_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.environ.get("OWM_API_KEY")
MY_LAT = 6.493111
MY_LONG = 3.384163
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

weather_params = {
    "appid": API_KEY,
    "lat": MY_LAT,
    "lon": MY_LONG,
    "cnt": 4,
}

response = requests.get(url=OpenWeatherMap_Endpoint, params= weather_params)
response.raise_for_status()
weather_data = response.json()

# weather_id= weather_data["list"][randint(0,4)]["weather"][0]["id"]
# if weather_id < 700:
#     print("Bring an Umbrella!")
# else:
#     print(" Umbrella perhaps?")

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    client = Client(ACCOUNT_SID,AUTH_TOKEN)
    message = client.messages.create(
        body="It's going to rain today.Remember to bring an umbrella☔.",
        from_="+13853960574",
        to="+2347079424227",
    )
    print(message.status)

