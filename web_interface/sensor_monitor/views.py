from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Sensor, SensorData, Alert
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import redis
from django.conf import settings
from datetime import datetime
import time

# Create your views here.

def alert_stream(request):
    """
    Server-Sent Events endpoint for real-time alerts
    """
    def event_stream():
        pubsub = redis_instance.pubsub()
        pubsub.subscribe('alerts')
        
        # Send initial keep-alive
        yield 'data: {}\n\n'
        
        try:
            for message in pubsub.listen():
                if message['type'] == 'message':
                    yield f'data: {message["data"]}\n\n'
                time.sleep(0.1)  # Prevent CPU overload
        except Exception as e:
            print(f"SSE Error: {str(e)}")
        finally:
            pubsub.unsubscribe('alerts')
            pubsub.close()
    
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
