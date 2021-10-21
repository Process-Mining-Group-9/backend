from multiprocessing import Queue
from time import sleep
from mqtt_event import MqttEvent
import httpx


def start(queue: Queue, address: str):
    while True:
        if not queue.empty():
            event: MqttEvent = queue.get(block=True, timeout=10)
            result = httpx.post(address + '/events/add', json=event.to_dict())
        else:
            sleep(0.05)

