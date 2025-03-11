from django.db import models


class SensorReading(models.Model):
    sensor_id = models.IntegerField()
    timestamp = models.DateTimeField(
        help_text="Timestamp when the reading was taken at the sensor"
    )
    metadata = models.JSONField()

    def __str__(self):
        return f"SensorReading {self.sensor_id} at {self.timestamp}"


class APIKey(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
