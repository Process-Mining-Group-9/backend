from multiprocessing import Queue
from time import sleep
from mqtt_event import MqttEvent
import httpx
import logging


def start(queue: Queue, address: str):
    while True:
        if not queue.empty():
            event: MqttEvent = queue.get(block=True, timeout=10)
            try:
                result = httpx.post(address + '/notify', json=event.to_dict())
                if result.is_success:
                    logging.info(f'Notified miner of new event with result: {result}. Event: {event}')
                else:
                    raise Exception(f'Unsuccessful notify: {result}')
            except Exception as e:
                logging.error(f'Exception while trying to notify miner of event. Exception: {e}. Event: {event}')
                queue.put(event, block=True, timeout=10)  # Put it back at the end of the queue and try again later
                sleep(1)
            finally:
                logging.debug(f'Events remaining in Queue: {queue.qsize()}')
        else:
            sleep(0.1)  # Sleep for a bit to avoid constant evaluation of queue

