from datetime import date

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import Avg

only_lower_case_letters = RegexValidator(r"^[a-z\s]+$", 'Only lower case letters allowed.')


class Sensor(models.Model):
    # Model that stores the sensor metadata. ID is set by Django automatically.
    sensor_nickname = models.CharField(max_length=50, blank=True, null=True)
    country_name = models.CharField(max_length=50, blank=False, null=True, validators=[only_lower_case_letters])
    city_name = models.CharField(max_length=100, blank=False, null=True, validators=[only_lower_case_letters])

    def __str__(self):
        return str(self.id)


class SensorData(models.Model):
    # Model that stores the sensor data associated with a sensor. Foreign key with sensor model.
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True, related_name='sensor_data_all')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=True)
    humidity = models.IntegerField(blank=False, null=True, validators=[MaxValueValidator(100), MinValueValidator(1)])
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=True)
    last_update = models.DateTimeField(auto_now_add=True, blank=False, null=True)

    def __str__(self):
        return str(self.sensor_id)

    @property
    def temp_avg(self):
        return SensorData.objects.filter(sensor_id=self.sensor_id).aggregate(Avg('temperature'))

    @property
    def humidity_avg(self):
        return SensorData.objects.filter(sensor_id=self.sensor_id).aggregate(Avg('humidity'))

    @property
    def wind_speed_avg(self):
        return SensorData.objects.filter(sensor_id=self.sensor_id).aggregate(Avg('wind_speed'))
