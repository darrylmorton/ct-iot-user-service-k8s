from datetime import datetime, timezone
from unittest.mock import patch

from confluent_kafka import Consumer

import tests.config as test_config
from tests.helper.token_helper import create_token
from tests.helper.email_helper import email_consumer
from tests.helper.routes_helper import RoutesHelper
from tests.helper.user_helper import create_signup_payload
from user_service.service import app
from utils.kafka_util import KafkaUtil


class TestEmailProducer:
    token = create_token(
        secret=test_config.JWT_SECRET_CONFIRM_ACCOUNT,
        data={
            "username": test_config.USERNAME,
            "email_type": test_config.EMAIL_VERIFICATION_TYPES[0],
        },
    )
    token_url = KafkaUtil.create_token_url(token)
    hash_token_url = KafkaUtil.create_hash_token_url(token_url)

    @patch("utils.kafka_util.KafkaUtil.create_email_message")
    async def test_email_producer(self, mock_create_email_message, db_cleanup):
        mock_create_email_message.return_value = dict(
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
            email_type=test_config.EMAIL_VERIFICATION_TYPES[0],
            username=test_config.USERNAME,
            first_name=test_config.FIRST_NAME,
            token_url=self.token_url,
            token_url_hash=self.hash_token_url,
        )

        payload = create_signup_payload()

        await RoutesHelper.http_post_client(app, "/api/signup", payload)

        consumer_config = {
            "bootstrap.servers": "localhost:9092",
            "session.timeout.ms": 6000,
            "group.id": test_config.QUEUE_GROUP_ID,
            "auto.offset.reset": "earliest",
            "enable.auto.offset.store": True,
        }

        consumer = Consumer(consumer_config)

        actual_result = email_consumer(_consumer=consumer, timeout_seconds=10)

        assert len(actual_result) > 0

        assert actual_result[0]["email_type"] == test_config.EMAIL_VERIFICATION_TYPES[0]
        assert actual_result[0]["username"] == test_config.USERNAME
        assert actual_result[0]["first_name"] == test_config.FIRST_NAME
        assert actual_result[0]["token_url"] == self.token_url
        assert actual_result[0]["token_url_hash"] == self.hash_token_url
