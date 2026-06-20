import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


OpenWeatherMap_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
MY_LAT = 6.493111
MY_LONG = 3.384163
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "appid": api_key,
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
    proxy_client = TwilioHttpClient()
    if "https_proxy" in os.environ:
    proxy_client.session.proxies = {"https": os.environ["https_proxy"]}
    else:
    proxy_client.session.proxies = {}
    client = Client(account_sid, auth_token,http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today.Remember to bring an umbrella☔.",
        from_="+13853960574",
        to="+2347079424227",
    )
    print(message.status)

