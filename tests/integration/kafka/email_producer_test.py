from confluent_kafka import Consumer

import tests.config as test_config
from logger import log
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
            "session.timeout.ms": 300000,
            "group.id": "email-topic",
            "enable.auto.commit": False,
            "auto.offset.reset": "earliest",
            "enable.auto.offset.store": False,
        }
        _consumer = Consumer(consumer_config)

        actual_result = email_consumer(_consumer=_consumer, timeout_seconds=20)
        log.debug(f"{actual_result=}")

        assert len(actual_result) == 1

        # assert (
        #     actual_result[0]["email_type"] == test_config.EMAIL_ACCOUNT_VERIFICATION_TYPE
        # )
        # assert actual_result[0]["username"] == test_config.USERNAME
