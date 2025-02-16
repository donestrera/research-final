from django.urls import re_path
from . import views

websocket_urlpatterns = [
    re_path(r'ws/sensors/$', views.SensorConsumer.as_asgi()),
] 