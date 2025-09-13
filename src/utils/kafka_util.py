import hashlib
import socket

import config
from logger import log


class KafkaUtil:
    @staticmethod
    def create_config() -> dict:
        """
        Creates a configuration dictionary for Kafka producer.

        Returns:
            dict: A dictionary containing Kafka configuration properties.
        """

        return {
            # User-specific properties that you must set
            "client.id": socket.gethostname(),
            # "bootstrap.servers": f"{config.QUEUE_PROTOCOL}:{config.QUEUE_PORTS}",
            "bootstrap.servers": f"{config.QUEUE_HOST}:9092",
            # Fixed properties
            "acks": "all",
        }

    @staticmethod
    def create_token_url(token: str) -> str:
        """
        Creates a token URL for account confirmation.

        Args:
            token (str): The token to include in the URL.
        """

        return f"{config.ULB_URL}/confirm-account?token={token}"

    @staticmethod
    def create_hash_token_url(token_url: str) -> str:
        """
        Creates an SHA-256 hash of the token URL.

        Args:
            token_url (str): The token URL to hash.

        Returns:
            str: The SHA-256 hash of the token URL.
        """

        return hashlib.sha256(token_url.encode()).hexdigest()

    @staticmethod
    def create_email_message(
        timestamp: str,
        email_type: str,
        username: str,
        first_name: str,
        token_url: str,
        token_url_hash: str,
    ) -> dict:
        """
        Creates an email message dictionary.

        Args:
            timestamp (str): The timestamp of the message.
            email_type (str): The type of email.
            username (str): The username of the recipient.
            first_name (str): The first name of the recipient.
            token_url (str): The token URL for the email.
            token_url_hash (str): The hash of the token URL.

        Returns:
            dict: A dictionary containing the email message details.
        """

        return dict(
            timestamp=timestamp,
            email_type=email_type,
            username=username,
            first_name=first_name,
            token_url=token_url,
            token_url_hash=token_url_hash,
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
