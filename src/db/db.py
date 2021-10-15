import logging
import typing
import os
import sqlite3
import datetime
from glob import glob
from pathlib import Path
from src.classes.mqtt_event import MqttEvent


class Database:
    def create_table(self, name: str) -> sqlite3.Connection:
        con = sqlite3.connect(self.config['dir'] + name + '.db')
        cursor = con.cursor()
        cursor.execute('CREATE TABLE events (timestamp TEXT, process TEXT, activity TEXT, payload TEXT)')
        con.commit()
        return con

    def store_message(self, msg: MqttEvent):
        conn = self.connections.get(msg.source)
        if not conn:
            conn = self.create_table(msg.source)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO events VALUES ('{datetime.datetime.utcnow().isoformat()}', "
                       f"'{msg.process}', '{msg.activity}', '{msg.payload}')")
        conn.commit()

    def get_messages(self, process: str) -> typing.List[MqttEvent]:
        # TODO: Implement
        return []

    def start(self):
        logging.info('Listening for new events to record to a database.')
        try:
            while True:
                msg: MqttEvent = self.pipe.recv()
                logging.info(f'Received message from MQTT client: "{msg}"')
                self.store_message(msg)
        except Exception as e:
            logging.error(f'Exception while listening to new events. Exception: {e}')
            logging.info('Restarting database service')
            self.stop()
            self.__setup_db()
            self.start()

    def stop(self):
        logging.info('Closing all database connections and stopping the client.')
        for conn in self.connections.values():
            conn.close()

    def __setup_db(self):
        os.makedirs(self.config['dir'], exist_ok=True)
        db_files: typing.List[str] = glob(self.dir + "*.db")
        for file in db_files:
            name = Path(file).stem
            self.connections[name] = sqlite3.connect(file)

    def __init__(self, pipe_from_mqtt, config: dict):
        self.pipe = pipe_from_mqtt
        self.config: dict = config
        self.dir: str = config['dir']
        self.connections: typing.Dict[str, sqlite3.Connection] = dict()
        self.__setup_db()
