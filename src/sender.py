from mqtt_event import MqttEvent
from typing import List
from time import sleep
import logging
import random
import arrow
import httpx
import os


def start(event_list: List, address: str):
    sent: int = 0
    first_send = arrow.utcnow()

    while True:
        # Only for testing performance
        # event_list.append(MqttEvent(timestamp=arrow.utcnow().float_timestamp, source='testing', process='u1', activity=random.choice(['A', 'B', 'C', 'D', 'E'])))

        if event_list:
            event: MqttEvent = event_list[0]
            try:
                result = httpx.post(address + '/notify', json=event.to_dict(), headers={'X-Secret': os.environ['SECRET']})
                if result.is_success:
                    if sent == 0:
                        first_send = arrow.utcnow()
                    sent += 1

                    logging.info(f'Notified miner of new event with result: {result}. Event: {event}')
                    logging.info(f'Average inserts per second: {float(sent) / (arrow.utcnow() - first_send).seconds}')
                    del event_list[0]
                else:
                    raise Exception(f'Unsuccessful notify: {result}. Message: {result.text}')
            except Exception as e:
                logging.error(f'Exception while trying to notify miner of event. Exception: {e}. Event: {event}. Remaining: {len(event_list)}')
            finally:
                logging.info(f'Events remaining in Queue: {len(event_list)}')
        else:
            sleep(0.1)  # Sleep for a bit to avoid constant evaluation of queue
