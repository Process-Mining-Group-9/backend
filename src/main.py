from multiprocessing import Process, Pipe
from db.db import Database
from mqtt.mqtt import MQTT
import os
import multiprocessing_logging
import logging
import yaml


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


def setup_mqtt(send_pipe, mqtt_config: dict):
    client = MQTT(send_pipe, mqtt_config)
    proc = Process(target=client.start)
    proc.start()


def setup_db(recv_pipe, db_config: dict):
    db = Database(recv_pipe, db_config)
    proc = Process(target=db.start)
    proc.start()


if __name__ == '__main__':
    config: dict = yaml.safe_load(open('../config.yaml'))
    setup_logging(config['log'])
    logging.info('Initializing application processes')
    mqtt_db_recv, mqtt_db_send = Pipe(duplex=False)
    setup_mqtt(mqtt_db_send, config['mqtt'])
    setup_db(mqtt_db_recv, config['db'])
