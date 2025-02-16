from django.urls import path
from . import views

app_name = 'sensor_monitor'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/historical-data/', views.get_historical_data, name='historical_data'),
    path('api/security-events/', views.get_security_events, name='security_events'),
]