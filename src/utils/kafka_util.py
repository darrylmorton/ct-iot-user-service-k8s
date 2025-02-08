import socket

import config
from logger import log


class KafkaUtil:
    @staticmethod
    def create_config() -> dict:
        return {
            # User-specific properties that you must set
            "client.id": socket.gethostname(),
            # "bootstrap.servers": f"{config.QUEUE_PROTOCOL}:{config.QUEUE_PORTS}",
            "bootstrap.servers": f"{config.QUEUE_HOST}:9092",
            # Fixed properties
            "acks": "all",
        }

    @staticmethod
    def create_email_message(
        timestamp: str,
        email_type: str,
        username: str,
        token: str,
    ) -> dict:
        return dict(
            email_type=email_type,
            username=username,
            timestamp=timestamp,
            token=token,
        )

    @staticmethod
    def delivery_report(err, msg):
        """
        Reports the success or failure of a message delivery.

        Args:
            err (KafkaError): The error that occurred on None on success.
            msg (Message): The message that was produced or failed.
        """

        if err is not None:
            log.error("Delivery failed for User record {}: {}".format(msg.key(), err))
            return

        log.debug(
            "User record {} successfully produced to {} [{}] at offset {}".format(
                msg.key(), msg.topic(), msg.partition(), msg.offset()
            )
        )
