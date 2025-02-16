from django.urls import path
from . import views

app_name = 'sensor_monitor'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]