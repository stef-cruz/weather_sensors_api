from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Sensor, SensorData

only_lower_case_letters = RegexValidator(r"^[a-z\s]+$", 'Only lower case letters allowed.')


class SensorDataSerializer(serializers.ModelSerializer):
    sensor_id = PrimaryKeyRelatedField(queryset=Sensor.objects.all(), required=True)
    temperature = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    humidity = serializers.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], required=True)
    wind_speed = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    last_update = serializers.DateTimeField(format="%d/%m/%Y", required=False)

    class Meta:
        model = SensorData
        fields = ('sensor_id', 'temperature', 'humidity', 'wind_speed', 'last_update')


class SensorDataAverageSerializer(serializers.ModelSerializer):
    temp_avg = serializers.ReadOnlyField()
    humidity_avg = serializers.ReadOnlyField()
    wind_speed_avg = serializers.ReadOnlyField()
    last_update = serializers.DateTimeField(format="%d/%m/%Y", required=False)

    class Meta:
        model = SensorData
        fields = ('sensor_id', 'temp_avg', 'humidity_avg', 'wind_speed_avg', 'last_update')


class SensorSerializer(serializers.ModelSerializer):
    sensor_nickname = serializers.CharField(max_length=50, required=False)
    country_name = serializers.CharField(max_length=50, required=True, validators=[only_lower_case_letters])
    city_name = serializers.CharField(max_length=50, required=True, validators=[only_lower_case_letters])
    sensor_data_all = SensorDataAverageSerializer(many=True, required=False)

    class Meta:
        model = Sensor
        fields = ('id', 'sensor_nickname', 'country_name', 'city_name', 'sensor_data_all')
