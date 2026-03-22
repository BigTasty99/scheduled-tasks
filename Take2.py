import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient



api_key= os.environ.get("OWM_API_KEY")
MY_LAT = 36.549980
MY_LONG = 139.870010
OWM_Endpoint="https://api.openweathermap.org/data/2.5/forecast"
account_sid=os.environ.get("ACCOUNT_SID")
auth_token=os.environ.get("AUTH_TOKEN")


weather_params={
    "lat":MY_LAT,
    "lon":MY_LONG,
    "appid":api_key,
    "units":"metric",
    "cnt":4,
}

response=requests.get(url=OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data=response.json()
# print(weather_data["list"][0]["weather"][0]["id"])

will_rain=False
for forecast in weather_data["list"]:
    condition_code=forecast["weather"][0]["id"]
    if int(condition_code)<700:
        will_rain=True
if will_rain:
    proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Bring an umbrella!",
        from_=os.environ.get("TWILIO_NUMBER"),
        to=os.environ.get("VERIFIED_NUMBER"),
    )

    print(message.status)
