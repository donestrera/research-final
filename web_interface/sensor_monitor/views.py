from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sensor, SensorData
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Create your views here.

def dashboard(request):
    """Render the main dashboard page."""
    return render(request, 'sensor_monitor/dashboard.html')

class SensorConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for handling sensor data updates."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        await self.channel_layer.group_add("sensors", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard("sensors", self.channel_name)
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            await self.channel_layer.group_send(
                "sensors",
                {
                    "type": "sensor_update",
                    "data": data
                }
            )
        except json.JSONDecodeError:
            print("Error decoding JSON data")
    
    async def sensor_update(self, event):
        """Send sensor updates to WebSocket."""
        await self.send(text_data=json.dumps(event["data"]))
