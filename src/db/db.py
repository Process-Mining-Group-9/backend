def start(pipe_from_mqtt):
    while True:
        msg = pipe_from_mqtt.recv()
        print(f'Received message from MQTT: {msg}')
