from django.urls import include, path, re_path
from rest_framework import routers
from . import views
from .views import SensorViews, SensorDataViews

urlpatterns = [
    path('sensors/', SensorViews.as_view()),
    path('sensors/<int:id>', SensorViews.as_view()),
    path('sensor_data/', SensorDataViews.as_view()),
    path('sensor_data/<int:id>', SensorDataViews.as_view())
]
