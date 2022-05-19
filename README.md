# Weather API

Weather API is a service that receives weather data from various sensors that report the metrics temperature, humidity and wind speed.

## Table of Contents


- [Features](#features)
    -  [Endpoints](#endpoints)
    -  [Fields](#fields)
    -  [Features](#features)
- [Tech & Tools](#tech-and-tools)
- [DB Schema](#db-schema)
- [Tests](#tests)
    - [Python Linter](#python-linter)
    - [Unit tests](#unit-tests)
- [System Design](#system-design)
- [How to run this project locally](#how-to-run-this-project-locally)
- [Known issues](#known-issues)
- [Features left to implement](#features-left-to-implement)

## Features
- This application allows get, post and put HTTP requests.
- There are 2 tables in the database, sensors and sensor_id. 
- Users should first register the sensor, then post data to the sensor id.
- The application returns the average value for the metrics temperature, humidity and wind speed.
- The use can use the parameters sensors_id to query one or more ids, start_date and end_date to filter the results by date.

### Endpoints:
`/v1/sensors` > stores sensor metadata  
`/v1/sensor_data` > stores sensor data


### Fields:

Sensor API:

|Field name|Field type|Required|Validation|
|---|---|---|---|
|`sensor_nickname`|string|False|False|
|`country_name`|string|True|True. Only allows lower case string|
|`city_name`|string|True|True. Only allows lower case string|

Sensor_Data API:

|Field name|Field type|Required|Validation|
|---|---|---|---|
|`sensor_id`|int|True|-|
|`temperature`|decimal(3,2)|True|True. Only allows length 100, precision 2 |
|`humidity`|int|True|True. % range from 1-100 |
|`wind_speed`|decimal|True|True. Only allows length 100, precision 2 |
|`last_update`|date|False|False. Should not be added to the request, it is auto generated in the DB.|

#### Get requests: 

`http://127.0.0.1:8000/v1/sensors/`   
`http://127.0.0.1:8000/v1/sensor_data/`    

*Param `sensor_id`*:  
`http://127.0.0.1:8000/v1/sensor_data/?sensor_id={sensor_id1, sensor_id2}`  


Requests can be made for one or more sensors.


*Param `start_date` & `end_date`*:  
`http://127.0.0.1:8000/v1/sensor_data/?start_date={start_date}&end_date={end_date}`  

Format expected _Mon May 16 00:00:00 2022_, Date range cannot be longer than a month.

*Get data from the terminal using the following commands*:    
`curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/v1/sensors/`  
`curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/v1/sensor_data/`  

#### Post requests:
`http://127.0.0.1:8000/v1/sensors/`    
Format supported JSON. Example of valid payload:  

    {
    "sensor_nickname": "nickname",  
    "country_name": "country",  
    "city_name": "city"  
    }


Example of response:

    {
    "status": "success",
    "data": [
        {
        "id": "1",  
        "sensor_nickname": "nickname",  
        "country_name": "country",  
        "city_name": "city"
        }
    ] 
    }



`http://127.0.0.1:8000/v1/sensor_data/`    

Format supported JSON. Example of valid payload:  

    {
    "sensor_id": "2",  
    "temperature": 150,  
    "humidity": 50,  
    "wind_speed": 150   
    }


Example of response:

    {
    "status": "success",
    "data": [
        {
        "sensor_id": "2",  
        "temperature": 150,  
        "humidity": 50,  
        "wind_speed": 150
        }
    ] 
    }


*Post data from the terminal using the following commands*:  
`curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/v1/sensors/ '{ "sensor_nickname": "mooo", "country_name": "spain", "city_name": "murcia" }'`  
`curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/v1/sensor_data/ -d '{ "sensor_id": "1", "temperature": 150, "humidity": 50, "wind_speed": 150 }'`   


#### Put requests: 
`http://127.0.0.1:8000/v1/sensors/{id}`    
Format supported JSON. Example of valid payload:  

    {
    "sensor_nickname": "nickname_changed"
    }


Example of response:  

    {
    "status": "success",
    "data": [
        {
        "sensor_id": "1",  
        "sensor_nickname": "nickname_changed",  
        "country_name": "country",  
        "city_name": "city"
        }
    ] 
    }


`http://127.0.0.1:8000/v1/sensor_data/{id}`    
Format supported JSON. Example of valid payload:  

    {
    "id": "1",
    "temperature": "-5"
    }


Example of response:  

    {
    "status": "success",
    "data": [
        {
        "id": "1",  
        "temperature": "-5",  
        "humidity": "50",  
        "wind_speed": "15",
        }
    ] 
    }



*Put data from the terminal using the following commands*:  
`curl -X PUT -H "Content-Type: application/json" http://127.0.0.1:8000/v1/sensors/1 '{ "sensor_nickname": "another_nickname" }'`  
`curl -X PUT -H "Content-Type: application/json" http://127.0.0.1:8000/v1/sensor_data/1 -d '{ "sensor_id": "1", "temperature": 10}'`  


## Tech and Tools

- Python
- Django Restful Framework
- Pycharm as the IDE
- Postman to test the endpoints

## DB Schema

<img src="https://github.com/stefcruz/weather_api/blob/master/readme/dbschema.png">

## Tests

### Python Linter
Pycharm has the Pylint linter built-in.

### Unit tests

I used the django test framework to write the endpoint tests. For this proof of concept I created valid and invalid post, get and put requests for the sensor API only.  

To run the tests on your local, follow the steps on [how to run this project locally](#how-to-run-this-project-locally) and run the commands:  
`./manage.py test` # for all tests on the project  
`./manage.py test sensors.tests` # for all tests inside folder tests from the sensors app  
`./manage.py test sensors.tests.GetSensorTestCase.test_get_request` # to run the test_get_request from the class GetSensorTestCase  

All tests passed:  
<img src="https://github.com/stefcruz/weather_api/blob/master/readme/test_passed.png">  

## System Design

The delete http request has not been created on this project.

<img src="https://github.com/stefcruz/weather_api/blob/master/readme/system_design.png">

## How to run this project locally

1. Clone this git repo on your local or using an IDE
2. Navigate to the project directory `cd ~/weather_api`
3. Create virtual environment `apt-get install python3-venv` or `sudo apt-get install python3-venv` if your user doesn't have the permissions
4. Create directory `mkdir venv`
5. Navigate to the directory `cd venv`
6. Run the command `python3 -m venv djangoenv`
7. Activate environment `source djangoenv/bin/activate`
8. Install requirements `cd ..` and `pip install -r requirements.txt`
9. Make migrations `./manage.py makemigrations`  
10. Apply migrations `./manage.py migrate`  
10. Run server `./manage.py runserver`  
11. Navigate to API url http://127.0.0.1:8000/v1/sensors/ or http://127.0.0.1:8000/v1/sensor_data/

## Known issues
- Validation to the get request with sensor_id parameter when string is used as a param. The request `http://127.0.0.1:8000/v1/sensors/?sensor_id=x` will fail.
- There is an issue with sensor data showing multiple times for each sensor. The average metrics are returned correctly (calculated in the DB) however it displays all the sensor_data entries in the database. Ideally it should only display one set of data for each sensor.  

Current behaviour:  
<img src="https://github.com/stefcruz/weather_api/blob/master/readme/current-behaviour-1.png">

Expected behaviour:  
<img src="https://github.com/stefcruz/weather_api/blob/master/readme/expected-behaviour-1.png">

## Features left to implement

- Front end
- Delete http request
- Create tests for the SensorData endpoints
- Create tests for the serializers on both endpoints
- The date format on the the get request is too complicated, it should allow the user to use format DD/MM/YYYY.
