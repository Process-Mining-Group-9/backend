from mqtt_event import MqttEvent
from paho.mqtt.client import Client, MQTTMessage
from multiprocessing import Process, Queue
import sender
import yaml
import typing

config: dict = yaml.safe_load(open('../config.yaml'))
event_queue = Queue()


def on_connect(_client: Client, userdata, flags, rc) -> None:
    print(f'Connected with result code {rc}')
    _client.subscribe(config['mqtt']['base_topic'])


def on_message(_client: Client, userdata, msg: MQTTMessage) -> None:
    hierarchy: typing.List[str] = msg.topic.split('/')
    if len(hierarchy) == 4:
        event = MqttEvent(base=hierarchy[0], source=hierarchy[1], process=hierarchy[2],
                          activity=hierarchy[3], payload=msg.payload.decode())
        print(f'Sending observed event on topic {msg.topic} to database. Event: "{event}"')
        event_queue.put(event, block=True, timeout=10)
    else:
        print(f'Ignoring event with non-matching topic structure: {msg.topic}.')


def setup_mqtt_client() -> Client:
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    broker = config['mqtt']['broker']
    port = config['mqtt']['port']
    client.connect(broker, port, 60)
    return client


def setup_event_sender() -> Process:
    sender_process = Process(target=sender.start, args=(event_queue, config['db']['address']))
    sender_process.start()
    return sender_process


if __name__ == '__main__':
    mqtt_client = setup_mqtt_client()
    sender = setup_event_sender()
    mqtt_client.loop_forever()  # Blocks forever

