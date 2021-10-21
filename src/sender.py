from multiprocessing import Queue
from time import sleep
from mqtt_event import MqttEvent
import httpx
import logging


def start(queue: Queue, address: str):
    while True:
        if not queue.empty():
            event: MqttEvent = queue.get(block=True, timeout=10)
            result = httpx.post(address + '/events/add', json=event.to_dict())
            logging.info(f'Posted event to DB with result: {result}')
        else:
            sleep(0.01)

