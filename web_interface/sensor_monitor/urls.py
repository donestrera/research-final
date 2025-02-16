from django.urls import path
from . import views

app_name = 'sensor_monitor'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/sensor-data/', views.sensor_data, name='sensor_data'),
    path('api/create-alert/', views.create_alert, name='create_alert'),
    path('api/sensor-data/<int:sensor_id>/', views.get_sensor_data, name='get_sensor_data'),
    path('api/active-alerts/', views.get_active_alerts, name='get_active_alerts'),
    path('api/alerts/', views.alert_stream, name='alert_stream'),  # Add SSE endpoint
] 