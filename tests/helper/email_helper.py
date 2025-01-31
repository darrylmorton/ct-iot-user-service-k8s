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

        _consumer.subscribe(["email-topic"])

        while True:
            log.debug(f"consumer polling...")

            if time.time() > timeout:
                log.info(f"Task timed out after {timeout_seconds}")
                break

            message = _consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                log.info(f"Consumer error: {message.error()}")
                continue

            log.debug(
                f'{message.topic()=}, {message.partition()=}, {message.offset()=}, {str(message.key())=}'
            )
            log.debug(f"{message.value()=}")

            message_body = json.loads(message.value())
            messages.append(message_body)

    except KafkaException as e:
        log.error(f"email_consumer error: {e}")
    finally:

        return messages
