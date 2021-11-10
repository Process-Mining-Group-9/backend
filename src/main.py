from mqtt_event import MqttEvent
from paho.mqtt.client import Client, MQTTMessage
from multiprocessing import Process, Queue
import multiprocessing_logging
import os
import typing
import logging
import json
import arrow
import sender

event_queue = Queue()


def on_connect(_client: Client, userdata, flags, rc) -> None:
    _client.subscribe(os.environ['MQTT_BASE_TOPIC'])
    logging.info(f'Connected to {os.environ["MQTT_BROKER"]}:{os.environ["MQTT_PORT"]} on topic {os.environ["MQTT_BASE_TOPIC"]} with result code {rc}')


def on_message(_client: Client, userdata, msg: MQTTMessage) -> None:
    hierarchy: typing.List[str] = msg.topic.split('/')
    if len(hierarchy) == 4:
        payload: dict = json.loads(msg.payload.decode()) if msg.payload else dict()
        event = MqttEvent(timestamp=payload['timestamp'] if 'timestamp' in payload else arrow.utcnow().timestamp(),
                          base=hierarchy[0], source=hierarchy[1], process=hierarchy[2],
                          activity=hierarchy[3], payload=msg.payload.decode())
        event_queue.put(event, block=True, timeout=10)
    else:
        logging.warning(f'Ignoring event with non-matching topic structure: {msg.topic}')


def setup_logging():
    file: str = os.environ['LOG_FILE']
    log_format: str = os.environ['LOG_FORMAT']
    level: int = int(os.environ['LOG_LEVEL'])
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
    broker = os.environ['MQTT_BROKER']
    port = int(os.environ['MQTT_PORT'])
    client.connect(broker, port, 60)
    return client


def setup_event_sender() -> Process:
    sender_process = Process(target=sender.start, args=(event_queue, os.environ['MINER_ADDRESS']))
    sender_process.start()
    return sender_process


if __name__ == '__main__':
    setup_logging()
    mqtt_client = setup_mqtt_client()
    sender = setup_event_sender()
    mqtt_client.loop_forever()  # Blocks forever

