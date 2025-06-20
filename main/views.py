import requests
from django.shortcuts import render
from .forms import CityForm
from decouple import config

# Create your views here.
def home(request):
    new_city, url, token_key = None, '', config('TOKEN_KEY', '')
    err_msg, message, message_class = '', '', ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            url = f'http://api.openweathermap.org/data/2.5/weather?q={new_city}&units=metric&appid={token_key}'
            existing_city_count = city.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City doesnt exist"
            else:
                err_msg = "City already exist in the database!"
        if err_msg :
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added successfully!'
            message_class = "alert-success"
    
    form = CityForm()
    cities = city.objects.all()

    weather_data = []

    for citi in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={citi}&units=metric&appid={token_key}'
        r = requests.get(url).json()
        city_weather  = {
            'city' : citi.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form':form,
        'message':message,
        'message_class':message_class
    }

    return render(request, "Main.html", context)