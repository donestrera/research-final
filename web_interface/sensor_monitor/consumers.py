import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
import logging

logger = logging.getLogger(__name__)

class SensorConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time sensor data updates
    """
    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of initial connection
        """
        try:
            # Join sensor_updates group
            await self.channel_layer.group_add(
                "sensor_updates",
                self.channel_name
            )
            await self.accept()
            logger.info(f"WebSocket connected: {self.channel_name}")
        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            raise StopConsumer()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason
        """
        try:
            # Leave sensor_updates group
            await self.channel_layer.group_discard(
                "sensor_updates",
                self.channel_name
            )
            logger.info(f"WebSocket disconnected: {self.channel_name}, code: {close_code}")
        except Exception as e:
            logger.error(f"WebSocket disconnect error: {str(e)}")

    async def sensor_update(self, event):
        """
        Handler for sensor_update events
        """
        try:
            # Send message to WebSocket
            await self.send(text_data=json.dumps(event['message']))
        except Exception as e:
            logger.error(f"Error sending sensor update: {str(e)}")
            await self.close(code=1011)  # Internal error

    async def receive(self, text_data):
        """
        Handle incoming messages from WebSocket clients
        """
        try:
            # Parse the incoming message
            data = json.loads(text_data)
            # Log receipt of message
            logger.debug(f"Received message: {data}")
            # You can add custom message handling here if needed
        except json.JSONDecodeError:
            logger.error("Received invalid JSON data")
        except Exception as e:
            logger.error(f"Error processing received message: {str(e)}") 