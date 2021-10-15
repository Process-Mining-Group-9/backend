import logging
from src.classes.mqtt_event import MqttEvent


class Database:
    def start(self):
        while True:
            msg: MqttEvent = self.pipe.recv()
            logging.info(f'Received message from MQTT: "{msg}"')

    def __init__(self, pipe_from_mqtt, config: dict):
        self.pipe = pipe_from_mqtt
        self.config = config
