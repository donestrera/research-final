from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sensor, SensorData
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from datetime import timedelta

# Create your views here.

def dashboard(request):
    """Render the main dashboard page."""
    return render(request, 'sensor_monitor/dashboard.html')

@csrf_exempt
def get_historical_data(request):
    """Get historical sensor data for a specified time range."""
    try:
        hours = int(request.GET.get('hours', 24))
        end_time = timezone.now()
        start_time = end_time - timedelta(hours=hours)
        
        # Get the sensor readings for the specified time range
        readings = SensorData.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time
        ).order_by('timestamp')
        
        # Format the data for the charts
        data = {
            'timestamps': [],
            'temperature': [],
            'humidity': [],
            'motion_events': [],
            'smoke_events': []
        }
        
        last_motion = False
        last_smoke = False
        
        for reading in readings:
            timestamp = reading.timestamp.isoformat()
            data['timestamps'].append(timestamp)
            data['temperature'].append(reading.temperature)
            data['humidity'].append(reading.humidity)
            
            # Track motion events (only when state changes)
            if reading.motion_detected != last_motion:
                data['motion_events'].append({
                    'timestamp': timestamp,
                    'status': reading.motion_detected
                })
                last_motion = reading.motion_detected
            
            # Track smoke events (only when state changes)
            if reading.smoke_detected != last_smoke:
                data['smoke_events'].append({
                    'timestamp': timestamp,
                    'status': reading.smoke_detected
                })
                last_smoke = reading.smoke_detected
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def get_security_events(request):
    """Get historical security events for a specified time range."""
    try:
        hours = int(request.GET.get('hours', 24))
        end_time = timezone.now()
        start_time = end_time - timedelta(hours=hours)
        
        # Get the sensor readings with security events
        readings = SensorData.objects.filter(
            timestamp__gte=start_time,
            timestamp__lte=end_time,
            motion_detected=True
        ).order_by('-timestamp')
        
        motion_events = []
        smoke_events = []
        
        for reading in readings:
            timestamp = reading.timestamp.isoformat()
            if reading.motion_detected:
                motion_events.append({
                    'timestamp': timestamp,
                    'type': 'Motion',
                    'location': reading.sensor.location
                })
            if reading.smoke_detected:
                smoke_events.append({
                    'timestamp': timestamp,
                    'type': 'Smoke',
                    'location': reading.sensor.location
                })
        
        return JsonResponse({
            'motion_events': motion_events,
            'smoke_events': smoke_events
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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
