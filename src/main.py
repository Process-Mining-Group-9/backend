from multiprocessing import Process, Pipe
import yaml
import mqtt.mqtt as mqtt
import db.db as db


def setup_mqtt(send_pipe, mqtt_config: dict):
    client = mqtt.MQTT(send_pipe, mqtt_config)
    proc = Process(target=client.start)
    proc.start()


def setup_db(recv_pipe, db_config: dict):
    proc = Process(target=db.start, args=(recv_pipe,))
    proc.start()


if __name__ == '__main__':
    config = yaml.safe_load(open('../config.yaml'))
    mqtt_db_recv, mqtt_db_send = Pipe(duplex=False)
    setup_mqtt(mqtt_db_send, config['mqtt'])
    setup_db(mqtt_db_recv, config['db'])
