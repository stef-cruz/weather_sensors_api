from django.contrib import admin
from .models import Sensor, SensorData


class SensorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sensor_nickname',
        'country_name',
        'city_name'
    )


admin.site.register(Sensor, SensorAdmin)


class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sensor_id',
        'temperature',
        'humidity',
        'wind_speed',
        'last_update',
    )


admin.site.register(SensorData, SensorDataAdmin)
