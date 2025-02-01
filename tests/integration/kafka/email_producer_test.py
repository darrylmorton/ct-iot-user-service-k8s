from confluent_kafka import Consumer

import tests.config as test_config
from tests.helper.email_helper import email_consumer
from tests.helper.routes_helper import RoutesHelper
from tests.helper.user_helper import create_signup_payload
from user_service.service import app


class TestEmailProducer:
    async def test_email_producer(self, db_cleanup):
        payload = create_signup_payload()

        await RoutesHelper.http_post_client(app, "/api/signup", payload)

        consumer_config = {
            "bootstrap.servers": "localhost:9092",
            "session.timeout.ms": 6000,
            "group.id": test_config.QUEUE_GROUP_ID,
            # "enable.auto.commit": True,
            "auto.offset.reset": "earliest",
            # "enable.auto.offset.store": True,
        }

        consumer = Consumer(consumer_config)

        actual_result = email_consumer(_consumer=consumer, timeout_seconds=10)

        assert len(actual_result) == 1

        assert (
            actual_result[0]["email_type"]
            == test_config.EMAIL_ACCOUNT_VERIFICATION_TYPE
        )
        assert actual_result[0]["username"] == test_config.USERNAME
