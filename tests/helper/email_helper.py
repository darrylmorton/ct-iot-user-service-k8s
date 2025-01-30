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

            message = _consumer.poll(timeout=1.0)
            log.info(f"**** MESSAGE {message=}")

            if message is None:
                continue

            # if message.error():
            #     log.info(f"message.error(): {message.error()}")

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (message.topic(), message.partition(), message.offset())
                    )
                elif message.error():
                    raise KafkaException(message.error())
            else:
                message_body = json.loads(message.value())

                messages.append(message_body)
    finally:
        # _consumer.close()

        return messages
