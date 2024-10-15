from urllib.error import HTTPError
from django.shortcuts import render
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
        units = request.GET.get('units', 'standard')
        WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
        try:
            source = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units={units}').read()

            # Convert JSON to dict
            list_of_data = json.loads(source)

            data = {
                "city": urllib.parse.unquote(city).title(),
                "country_code": str(list_of_data['sys']['country']), 
                "coordinate": str(list_of_data['coord']['lon']) + ' '
                            + str(list_of_data['coord']['lat']), 
                "temp": str(list_of_data['main']['temp']) + (' °C' if units == 'metric' else ' K'),
                "pressure": str(list_of_data['main']['pressure']), 
                "humidity": str(list_of_data['main']['humidity']), 
            }
        except HTTPError:
            data = {"error": '404', "city": city}
    else:
        data = {}
    return render(request, "main/weather.html", data)