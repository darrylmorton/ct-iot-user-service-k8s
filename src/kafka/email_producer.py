import asyncio
import calendar
import json
import time
import uuid
from datetime import datetime, timezone
from threading import Thread
from confluent_kafka import Producer, KafkaException

import config
from logger import log
from utils.kafka_util import KafkaUtil
from utils.token_util import TokenUtil


class EmailProducer:
    def __init__(self, loop=None):
        log.debug("initializing EmailProducer...")

        self.config = KafkaUtil.create_config()
        self.producer = Producer(self.config)
        self.topic = config.QUEUE_TOPIC_NAME

        self._loop = loop or asyncio.get_event_loop()
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self.producer.poll(config.QUEUE_POLL_WAIT_SECONDS)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, email_type: str, username: str):
        """
        An awaitable produce method.
        """
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, KafkaException(err)
                )
            else:
                self._loop.call_soon_threadsafe(result.set_result, msg)

        message = KafkaUtil.create_email_message(
            username=username,
            email_type=email_type,
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
            token=TokenUtil.encode_token(username, email_type),
        )

        self.producer.produce(
            topic=self.topic,
            key=str(uuid.uuid4()),
            value=json.dumps(message),
            timestamp=calendar.timegm(time.gmtime()),
            on_delivery=ack,
        )
        self.producer.flush()
        self.close()

        return message
