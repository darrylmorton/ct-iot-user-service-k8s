import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pydoc_data.topics import topics
from typing import Any
from confluent_kafka import KafkaError, KafkaException

import config
from tests.helper import token_helper
from logger import log
import tests.config as test_config


def email_consumer(_consumer: Any, timeout_seconds=0) -> list[dict]:
    timeout = time.time() + timeout_seconds
    messages = []

    try:
        log.info(f"email_consuming....")

        def print_assignment(_consumer, partitions):
            log.info("Assignment:", partitions)

        _consumer.subscribe(["email-topic"]) # , on_assign=print_assignment)

        while True:
            if time.time() > timeout:
                log.info(f"Task timed out after {timeout_seconds}")
                break

            log.debug(f"consumer polling...")

            message = _consumer.poll(1.0)
            # log.info(f"**** MESSAGE {message=}")

            if message is None:
                continue

            if message.error():
                log.info(f"Consumer error: {message.error()}")
                continue
            #     raise KafkaException(message.error())

            log.debug('%% %s [%d] at offset %d with key %s:\n' %
                 (message.topic(), message.partition(), message.offset(),
                  str(message.key())))

            log.debug(f"message.value() {message.value()}")

            message_body = json.loads(message.value())
            messages.append(message_body)

    except KafkaException as e:
        log.error(f"email_consumer error: {e}")
    finally:
        # consumer.close()

        return messages
