from django.urls import path 
from . import views 
  
urlpatterns = [ 
    path('', views.index, name='index'), 
    path('<str:city>', views.weather, name='weather'), 
    path('update-weather-params/<str:city>', views.update_weather_params, name='update_weather_params'), 
] 