# Arduino Sensor Dashboard

A real-time web dashboard for monitoring Arduino sensor data. This project provides a clean interface for viewing temperature, humidity, motion detection, and smoke detection data from an Arduino device.

## Prerequisites

- Python 3.8 or higher
- Arduino IDE
- Arduino board with sensors configured
- Virtual environment tool (venv recommended)

## Hardware Setup

1. Connect your sensors to the Arduino:
   - DHT22 (Temperature/Humidity) to pin 2
   - PIR Motion Sensor to pin 3
   - Smoke Sensor to pin A1
   - LED indicator to pin 13
   - Bell/Buzzer to pin 12

2. Upload the provided Arduino code (`arduino/sensor_code.ino`) to your board using the Arduino IDE.

## Software Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd arduino-sensor-project
   ```

2. Create and activate a virtual environment:
   ```bash
   cd web_interface
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Create a `.env` file in the `web_interface` directory:
   ```
   # Arduino Configuration
   ARDUINO_PORT=/dev/ttyUSB0  # Change this to your Arduino port
   ARDUINO_BAUDRATE=9600

   # Django Configuration
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Initialize the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a default sensor:
   ```bash
   python manage.py shell -c "from sensor_monitor.models import Sensor; Sensor.objects.get_or_create(name='Arduino Sensor 1', location='Main Room')"
   ```

7. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Running the Application

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

## Troubleshooting

1. **Arduino Connection Issues**
   - Verify the correct port in your `.env` file
   - Check if the Arduino is properly connected
   - Ensure you have the right permissions to access the port

2. **WebSocket Connection Issues**
   - Check browser console for error messages
   - Verify that the Django server is running
   - Ensure your firewall isn't blocking WebSocket connections

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic` again
   - Check if DEBUG is set to True in development
   - Verify your STATIC_URL and STATIC_ROOT settings

## Development

- The frontend is built with vanilla JavaScript and CSS
- Real-time updates are handled through WebSocket connections
- Sensor data is stored in SQLite database
- The project uses Django Channels for WebSocket support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 