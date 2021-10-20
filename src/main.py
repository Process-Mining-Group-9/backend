from mqtt_event import MqttEvent
from paho.mqtt.client import Client, MQTTMessage
import yaml
import typing

config: dict = yaml.safe_load(open('../config.yaml'))


def on_connect(_client: Client, userdata, flags, rc):
    print(f'Connected with result code {rc}')
    _client.subscribe(config['mqtt']['base_topic'])


def on_message(_client: Client, userdata, msg: MQTTMessage):
    hierarchy: typing.List[str] = msg.topic.split('/')
    if len(hierarchy) == 4:
        event = MqttEvent(base=hierarchy[0], source=hierarchy[1], process=hierarchy[2],
                          activity=hierarchy[3], payload=msg.payload.decode())
        print(f'Sending observed event on topic {msg.topic} to database. Event: "{event}"')
        # TODO: Implement async request queue to newly built DB API, and add decent logging as in the other project
    else:
        print(f'Ignoring event with non-matching topic structure: {msg.topic}.')


if __name__ == '__main__':
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    broker = config['mqtt']['broker']
    port = config['mqtt']['port']
    client.connect(broker, port, 60)
    client.loop_forever()

