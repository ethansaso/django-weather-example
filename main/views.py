from django.shortcuts import render
import os
import urllib
import json

# Create your views here.
def index(request):
    if request.method == 'POST':
        # Make request for city given in POST body
        city = urllib.parse.quote(request.POST['city'])
        WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
        source = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}').read()

        # Convert JSON to dict
        list_of_data = json.loads(source)

        data = {
            "country_code": str(list_of_data['sys']['country']), 
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                        + str(list_of_data['coord']['lat']), 
            "temp": str(list_of_data['main']['temp']) + 'k', 
            "pressure": str(list_of_data['main']['pressure']), 
            "humidity": str(list_of_data['main']['humidity']), 
        }
        
        print(data)
    else:
        data = {}
    return render(request, "main/index.html", data)