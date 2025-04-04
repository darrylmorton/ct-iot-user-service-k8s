import json
import time
from typing import Any
from confluent_kafka import KafkaException

from logger import log
import tests.config as test_config


def email_consumer(_consumer: Any, timeout_seconds=0) -> list[dict]:
    timeout = time.time() + timeout_seconds
    messages = []

    try:
        log.debug("email_consuming....")

        _consumer.subscribe([test_config.QUEUE_TOPIC_NAME])

        while True:
            log.debug("consumer polling...")

            if time.time() > timeout:
                log.debug(f"Task timed out after {timeout_seconds}")
                break

            message = _consumer.poll(test_config.QUEUE_POLL_WAIT_SECONDS)

            if message is None:
                continue

            if message.error():
                raise KafkaException(message.error())

            log.debug(
                f"""{message.topic()=}, {message.partition()=}, 
                    {message.offset()=}, {str(message.key())=}"""
            )
            log.debug(f"{message.value()=}")

            message_body = json.loads(message.value())
            messages.append(message_body)

    except KafkaException as e:
        log.error(f"email_consumer error: {e}")
    finally:
        _consumer.unsubscribe()
        _consumer.close()

        return messages
