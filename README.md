# Architecture

## Recording of event logs
Event logs are published to a broker using the MQTT protocol, to which the backend service subscribes to. Each time a new event is published, the backend captures it, stores it, analyzes it, and shows it in a live view. It supports multiple log streams at once. The MQTT infrastructure is based on [Burattin et al.](https://orbit.dtu.dk/en/publications/mqtt-xes-real-time-telemetry-for-process-event-data)

### Technologies 
* [paho-mqtt](https://pypi.org/project/paho-mqtt/): MQTT library

## Storing of event logs
Each event log is stored in an append-only database or data store, including log, case id, activity, and potential payload.

### Technologies
* XES or CSV Files
* Any relational database

## Analysis 
On startup, models are mined from the existing logs in the database. Each time a new event is received, the model is adjusted so as if the event was part of the existing logs. This allows for live discovery of new activities and relations.

Each model is stored in memory, but caching or persistence in a document database is possible.

### Technologies
* [pm4py](https://pm4py.fit.fraunhofer.de/): Process mining library

## Storing of mined models
The mined models can either be stored in-memory or a persistent storage. In-memory storage requires rediscovery of existing logs at startup, which can be time-consuming if the logs are massive.

### Technologies
* [ZODB](https://zodb.org/en/latest/): Python Object database
* [MongoDB](https://www.mongodb.com/): Document-based database (JSON format)

## REST API
The backend provides an API for the front-end to call in order to get a list of logs, event logs, etc. and to add new MQTT streams, apply different discovery models, etc.

### Technologies
* [Flask](https://flask.palletsprojects.com/en/2.0.x/): Micro web framework, great for building REST API's
* [Django REST Framework](https://www.django-rest-framework.org/): Extension of Django to build REST API's

## WebSocket API
The WebSocket API provides the actual models of the processes and live instances of traces as they happen. After setting up a connection, the model for some event log is sent. Each time an event for that model is received, an update is pushed to the client with data on where in the model the instance currently is, and an update to the mined model, if relevant.

### Technologies
* [websockets](https://pypi.org/project/websockets/): WebSocket library for Python
* 
