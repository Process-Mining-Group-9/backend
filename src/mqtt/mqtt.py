import logging
import typing
import paho.mqtt.client as mqtt
from src.classes.mqtt_event import MqttEvent


class MQTT:
    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        logging.info(f'Connected with result code {rc}')
        client.subscribe(self.config['base_topic'])

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        hierarchy: typing.List[str] = msg.topic.split('/')
        if len(hierarchy) == 4:
            event = MqttEvent(hierarchy[0], hierarchy[1], hierarchy[2], hierarchy[3], msg.payload.decode())
            logging.info(f'Sending observed event on topic {msg.topic} to database. Event: "{event}"')
            self.pipe.send(event)
        else:
            logging.warning(f'Ignoring event with non-matching topic structure: {msg.topic}.')

    def start(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        broker = self.config['broker']
        port = self.config['port']
        logging.info(f'Connecting to MQTT Broker "{broker}" on Port {port}')
        client.connect(broker, port, 60)
        client.loop_forever()

    def __init__(self, pipe_to_db, config: dict):
        self.pipe = pipe_to_db
        self.config = config
