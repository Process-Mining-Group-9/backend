import paho.mqtt.client as mqtt


class MQTT:
    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        print('Subscribing to ' + self.config['base_topic'])
        client.subscribe(self.config['base_topic'])

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        hierarchy: list[str] = msg.topic.split('/')
        if len(hierarchy) == 4:
            assignment = {
                'base': hierarchy[0],
                'source_id': hierarchy[1],
                'process_id': hierarchy[2],
                'activity': hierarchy[3]
            }

            print(f'Observed event with assignment: {assignment}; Payload: {msg.payload}')
            self.pipe.send((assignment, msg.payload.decode()))

    def start(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self.config['broker'], self.config['port'], 60)
        client.loop_forever()

    def __init__(self, pipe_to_db, config: dict):
        self.pipe = pipe_to_db
        self.config = config
