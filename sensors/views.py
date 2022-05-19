from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import SensorSerializer, SensorDataSerializer, SensorDataAverageSerializer
from .models import Sensor, SensorData


class SensorViews(APIView):
    def post(self, request):
        serialize_sensor = SensorSerializer(data=request.data)
        if serialize_sensor.is_valid():
            serialize_sensor.save()
            return Response({"status": "success", "data": serialize_sensor.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serialize_sensor.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        sensors = Sensor.objects.all()
        serialize_sensor = SensorSerializer(sensors, many=True)

        # Request with an ID, metrics returned should be average
        if id:
            sensor = get_object_or_404(Sensor, id=id)
            serialize_sensor = SensorSerializer(sensor)
            return Response({"status": "success", "data": serialize_sensor.data}, status=status.HTTP_200_OK)

            # Requests for one or more sensor IDs
        if 'sensor_id' in request.query_params:
            param_sensor_id = request.query_params.get('sensor_id').split(',')
            get_ids_from_db = Sensor.objects.filter(id__in=param_sensor_id)
            if not get_ids_from_db:
                return Response({"status": "error", "data": "ID does not exist in the database."},
                                status=status.HTTP_400_BAD_REQUEST)
            serialize_sensor_data = SensorSerializer(get_ids_from_db, many=True)
            return Response({"status": "success", "data": serialize_sensor_data.data}, status=status.HTTP_200_OK)

        return Response({"status": "success", "data": serialize_sensor.data}, status=status.HTTP_200_OK)

    def put(self, request, id=None):
        sensor = get_object_or_404(Sensor, id=id)
        serialize_sensor = SensorSerializer(sensor, data=request.data, partial=True)
        if serialize_sensor.is_valid():
            serialize_sensor.save()
            return Response({"status": "success", "data": serialize_sensor.data}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"status": "error", "data": serialize_sensor.errors}, status=status.HTTP_400_BAD_REQUEST)


class SensorDataViews(APIView):
    def post(self, request):
        serialize_sensor_data = SensorDataSerializer(data=request.data)
        if serialize_sensor_data.is_valid():
            serialize_sensor_data.save()
            return Response({"status": "success", "data": serialize_sensor_data.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serialize_sensor_data.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        sensors = SensorData.objects.all()
        serialize_sensor_data = SensorDataSerializer(sensors, many=True)

        if id:
            sensor = get_object_or_404(SensorData, id=id)
            serialize_sensor_data = SensorDataSerializer(sensor)
            return Response({"status": "success", "data": serialize_sensor_data.data}, status=status.HTTP_200_OK)

        # Request with date range, not greater than a month.
        if 'start_date' and 'end_date' in request.query_params:
            # format expected '%a %b %d %H:%M:%S %Y', e.g. Mon May 16 00:00:00 2022, Fri Jul 01 00:00:00 2022
            param_start_date = datetime.strptime(request.query_params.get('start_date'), '%a %b %d %H:%M:%S %Y').date()
            param_end_date = datetime.strptime(request.query_params.get('end_date'), '%a %b %d %H:%M:%S %Y').date()

            if param_start_date > param_end_date:
                return Response({"status": "error", "data": "End date should not be greater than start date"},
                                status=status.HTTP_400_BAD_REQUEST)
            if (param_end_date - param_start_date) > timedelta(days=30):
                return Response({"status": "error", "data": "Max range allowed is 30 days"},
                                status=status.HTTP_400_BAD_REQUEST)

            data_db = sensors.filter(last_update__range=[str(param_start_date), str(param_end_date)])

            serialize_sensor_data = SensorDataSerializer(data_db, many=True)
            return Response({"status": "success", "data": serialize_sensor_data.data}, status=status.HTTP_200_OK)

        # Requests for one or more sensor IDs
        if 'sensor_id' in request.query_params:
            param_sensor_id = request.query_params.get('sensor_id').split(',')
            get_ids_from_db = SensorData.objects.filter(sensor_id__in=param_sensor_id)
            if not get_ids_from_db:
                return Response({"status": "error", "data": "ID does not exist in the database."},
                                status=status.HTTP_400_BAD_REQUEST)
            serialize_sensor_data = SensorDataAverageSerializer(get_ids_from_db, many=True)
            return Response({"status": "success", "data": serialize_sensor_data.data}, status=status.HTTP_200_OK)

        return Response({"status": "success", "data": serialize_sensor_data.data}, status=status.HTTP_200_OK)

    def put(self, request, id=None):
        sensor = get_object_or_404(SensorData, id=id)
        serialize_sensor_data = SensorDataSerializer(sensor, data=request.data, partial=True)
        if serialize_sensor_data.is_valid():
            serialize_sensor_data.save()
            return Response({"status": "success", "data": serialize_sensor_data.data},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"status": "error", "data": serialize_sensor_data.errors},
                            status=status.HTTP_400_BAD_REQUEST)
