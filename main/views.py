from urllib.error import HTTPError
from django.shortcuts import render
from django.http import JsonResponse
import os
import urllib
import json

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def weather(request, city):
    if request.method == 'GET':
        # Make request for city given in GET body
        city = urllib.parse.quote(city.replace('-', ' '))
        units = request.GET.get('units', 'imperial')
        lang = request.GET.get('lang', 'en')
        WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
        try:
            source = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units={units}&lang={lang}').read()

            # Convert JSON to dict
            list_of_data = json.loads(source)

            data = {
                "city": str(list_of_data['name']),
                "country_code": str(list_of_data['sys']['country']), 
                "coordinate": str(list_of_data['coord']['lon']) + ' '
                            + str(list_of_data['coord']['lat']), 
                "description": str(list_of_data['weather'][0]['description']),
                "temp": str(list_of_data['main']['temp']) + (' °C' if units == 'metric' else ' °F'),
                "pressure": str(list_of_data['main']['pressure']), 
                "humidity": str(list_of_data['main']['humidity']), 
            }
        except HTTPError:
            data = {"error": '404', "city": urllib.parse.unquote(city).title()}
    else:
        data = {}
    return render(request, "main/weather.html", data)

def update_weather_params(request, city):
    city = urllib.parse.quote(city.replace('-', ' '))
    units = request.GET.get('units', 'imperial')
    lang = request.GET.get('lang', 'en')

    WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units={units}&lang={lang}"
    print(url)
    source = urllib.request.urlopen(url).read()

    # Convert JSON to dict
    data = json.loads(source)

    return JsonResponse({
        "temp": f"{data['main']['temp']} {' °C' if units == 'metric' else ' °F'}",
        "description": f"{data['weather'][0]['description']}",
        "name": f"{data['name']}"
    })