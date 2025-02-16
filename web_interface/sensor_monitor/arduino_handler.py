import serial
import json
import logging
import threading
import time
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import SensorData

logger = logging.getLogger(__name__)

class ArduinoHandler:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.running = False
        self.channel_layer = get_channel_layer()
        self._connect()

    def _connect(self):
        """Establish connection with Arduino"""
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            logger.info(f"Connected to Arduino on {self.port}")
            return True
        except serial.SerialException as e:
            logger.error(f"Failed to connect to Arduino: {str(e)}")
            return False

    def start(self):
        """Start reading data from Arduino"""
        if not self.serial:
            if not self._connect():
                return False

        self.running = True
        self.thread = threading.Thread(target=self._read_loop)
        self.thread.daemon = True
        self.thread.start()
        return True

    def stop(self):
        """Stop reading data from Arduino"""
        self.running = False
        if self.serial:
            self.serial.close()

    def _read_loop(self):
        """Main loop for reading data from Arduino"""
        while self.running:
            try:
                if self.serial.in_waiting:
                    line = self.serial.readline().decode('utf-8').strip()
                    if line:
                        self._process_data(line)
            except serial.SerialException as e:
                logger.error(f"Serial communication error: {str(e)}")
                self._reconnect()
            except Exception as e:
                logger.error(f"Error reading from Arduino: {str(e)}")
            time.sleep(0.1)

    def _reconnect(self):
        """Attempt to reconnect to Arduino"""
        logger.info("Attempting to reconnect to Arduino...")
        while self.running:
            if self._connect():
                break
            time.sleep(5)

    def _process_data(self, data):
        """Process incoming data from Arduino"""
        try:
            sensor_data = json.loads(data)
            
            # Create sensor reading
            reading = SensorData.objects.create(
                sensor_id=1,
                temperature=sensor_data.get('temperature'),
                humidity=sensor_data.get('humidity'),
                motion_detected=sensor_data.get('motionDetected'),
                smoke_detected=sensor_data.get('smokeDetected')
            )

            # Broadcast to WebSocket
            async_to_sync(self.channel_layer.group_send)(
                "sensor_updates",
                {
                    "type": "sensor_update",
                    "message": {
                        "sensor_id": 1,
                        "data": sensor_data,
                        "timestamp": reading.timestamp.isoformat()
                    }
                }
            )

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON data received: {data}")
        except Exception as e:
            logger.error(f"Error processing Arduino data: {str(e)}")

# Global Arduino handler instance
arduino_handler = None

def initialize_arduino():
    """Initialize the global Arduino handler"""
    global arduino_handler
    if arduino_handler is None:
        arduino_handler = ArduinoHandler(
            port=settings.ARDUINO_PORT,
            baudrate=settings.ARDUINO_BAUDRATE
        )
        arduino_handler.start()
    return arduino_handler

def get_arduino_handler():
    """Get the global Arduino handler instance"""
    global arduino_handler
    if arduino_handler is None:
        arduino_handler = initialize_arduino()
    return arduino_handler 