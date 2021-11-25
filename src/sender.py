from mqtt_event import MqttEvent
from typing import List
from time import sleep
import httpx
import logging
import os


def start(event_list: List, address: str):
    while True:
        if event_list:
            event: MqttEvent = event_list[0]
            try:
                result = httpx.post(address + '/notify', json=event.to_dict(), headers={'X-Secret': os.environ['SECRET']})
                if result.is_success:
                    logging.info(f'Notified miner of new event with result: {result}. Event: {event}')
                    del event_list[0]
                else:
                    raise Exception(f'Unsuccessful notify: {result}. Message: {result.text}')
            except Exception as e:
                logging.error(f'Exception while trying to notify miner of event. Exception: {e}. Event: {event}. Remaining: {len(event_list)}')
            finally:
                logging.debug(f'Events remaining in Queue: {len(event_list)}')
        else:
            sleep(0.1)  # Sleep for a bit to avoid constant evaluation of queue

