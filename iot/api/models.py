from django.db import models


class SensorReading(models.Model):
    sensor_id = models.IntegerField()
    timestamp = models.DateTimeField(
        help_text="Timestamp when the reading was taken at the sensor"
    )
    metadata = models.JSONField()

    def __str__(self):
        return f"SensorReading {self.sensor_id} at {self.timestamp}"
