from django.db import models

class Sensor(models.Model):
    """
    Represents an Arduino sensor in the system
    """
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    """
    Stores the actual readings from sensors
    """
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    motion_detected = models.BooleanField(null=True, blank=True)
    smoke_detected = models.BooleanField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        values = []
        if self.temperature is not None:
            values.append(f"Temp: {self.temperature}°C")
        if self.humidity is not None:
            values.append(f"Humidity: {self.humidity}%")
        if self.motion_detected is not None:
            values.append(f"Motion: {'Detected' if self.motion_detected else 'None'}")
        if self.smoke_detected is not None:
            values.append(f"Smoke: {'Detected' if self.smoke_detected else 'None'}")
        return f"{self.sensor.name} - {', '.join(values)} at {self.timestamp}"
