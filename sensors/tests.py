from rest_framework import status
from rest_framework.test import APITestCase

from sensors.models import Sensor


class GetSensorTestCase(APITestCase):
    """ Test module for GET sensor API """

    def setUp(self):
        self.sensor1 = Sensor.objects.create(
            sensor_nickname='barca', country_name='spain', city_name='barcelona')

        self.sensor2 = Sensor.objects.create(
            sensor_nickname='dub', country_name='ireland', city_name='dublin')

    def test_get_request(self):
        response = self.client.get('/v1/sensors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_single_id_valid(self):
        response = self.client.get(f'/v1/sensors/{self.sensor1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_single_id_invalid(self):
        response = self.client.get('/v1/sensors/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_request_several_ids_valid(self):
        response = self.client.get(f'/v1/sensors/?sensor_id={self.sensor1.id},{self.sensor2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_several_ids_invalid(self):
        response = self.client.get(f'/v1/sensors/?sensor_id=300,400')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostSensorTestCase(APITestCase):
    """ Test module for POST sensor API """

    def setUp(self):
        self.valid_payload = {
            'sensor_nickname': 'barca',
            'country_name': 'spain',
            'city_name': 'barcelona'
        }
        self.invalid_payload = {
            'sensor_nickname': 'dub',
            'country_name': '',
            'city_name': 'spain'
        }

    def test_post_request_valid(self):
        response = self.client.post('/v1/sensors/', self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sensor.objects.count(), 1)
        self.assertEqual(Sensor.objects.get(id=1).sensor_nickname, 'barca')

    def test_post_request_invalid(self):
        response = self.client.post('/v1/sensors/', self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PutSensorTestCase(APITestCase):
    """ Test module for PUT sensor API """

    def setUp(self):
        self.sensor1 = Sensor.objects.create(
            sensor_nickname='barcelona', country_name='spain', city_name='barcelona')
        self.sensor2 = Sensor.objects.create(
            sensor_nickname='dub', country_name='ireland', city_name='dublin')
        self.valid_payload = {
            'sensor_nickname': 'catalunia',
            'country_name': 'spain',
            'city_name': 'barcelona'
        }
        self.invalid_payload = {
            'sensor_nickname': 'dub',
            'country_name': '',
            'city_name': 'spain'
        }

    def test_put_request_valid(self):
        response = self.client.put(f'/v1/sensors/{self.sensor1.id}', self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sensor.objects.get(id=1).sensor_nickname, 'catalunia')

    def test_put_request_invalid(self):
        response = self.client.put(f'/v1/sensors/{self.sensor2.id}', self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
