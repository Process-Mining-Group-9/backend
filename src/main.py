from mqtt_event import MqttEvent
from paho.mqtt.client import Client, MQTTMessage
from multiprocessing import Process, Queue
import multiprocessing_logging
import yaml
import typing
import logging
import os
import time
import sender

config: dict = yaml.safe_load(open('../config.yaml'))
event_queue = Queue()


def on_connect(_client: Client, userdata, flags, rc) -> None:
    logging.info(f'Connected with result code {rc}')
    _client.subscribe(config['mqtt']['base_topic'])


def on_message(_client: Client, userdata, msg: MQTTMessage) -> None:
    hierarchy: typing.List[str] = msg.topic.split('/')
    if len(hierarchy) == 4:
        event = MqttEvent(timestamp=int(time.time()), base=hierarchy[0], source=hierarchy[1],
                          process=hierarchy[2], activity=hierarchy[3], payload=msg.payload.decode())
        logging.info(f'Notifying miner with observed event: "{event}"')
        event_queue.put(event, block=True, timeout=10)
    else:
        logging.warning(f'Ignoring event with non-matching topic structure: {msg.topic}')


def setup_logging(log_config: dict):
    file: str = log_config['file']
    log_format: str = log_config['format']
    level: int = log_config['level']
    os.makedirs(os.path.dirname(file), exist_ok=True)
    logging.basicConfig(filename=file, format=log_format, level=level)

    stream_handler = logging.StreamHandler()
    stream_handler.formatter = logging.Formatter(log_format)
    logging.getLogger().addHandler(stream_handler)

    multiprocessing_logging.install_mp_handler()


def setup_mqtt_client() -> Client:
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    broker = config['mqtt']['broker']
    port = config['mqtt']['port']
    client.connect(broker, port, 60)
    return client


def setup_event_sender() -> Process:
    sender_process = Process(target=sender.start, args=(event_queue, config['miner']['address']))
    sender_process.start()
    return sender_process


if __name__ == '__main__':
    setup_logging(config['log'])
    mqtt_client = setup_mqtt_client()
    sender = setup_event_sender()
    mqtt_client.loop_forever()  # Blocks forever

