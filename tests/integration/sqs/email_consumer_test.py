import json
from unittest.mock import patch

from tests.helper.email_helper import email_consumer, create_sqs_queue
from tests.helper.routes_helper import RoutesHelper
from tests.helper.user_helper import create_signup_payload
from logger import log
import tests.config as test_config
from user_service.service import app

# @patch("sqs.email_producer.EmailProducer")


class TestEmailConsumer:
    async def test_email_producer(self, db_cleanup, email_producer):
        email_queue, email_dlq = create_sqs_queue(
            queue_name=test_config.SQS_EMAIL_QUEUE_NAME,
            dlq_name=test_config.SQS_EMAIL_DLQ_NAME,
        )

        # mock_email_producer.produce(
        #     email_type=test_config.SQS_EMAIL_ACCOUNT_VERIFICATION_TYPE,
        #     username=test_config.SES_TARGET,
        # )
        # mock_email_producer.email_queue = email_queue
        # mock_email_producer.dlq = email_dlq

        payload = create_signup_payload()

        await RoutesHelper.http_post_client(app, "/api/signup", payload)

        actual_result = email_consumer(email_queue, 10)
        # message_body = json.loads(actual_result.)

        log.debug(f"***** {actual_result=}")
        # "event": "***** actual_result=[{'Id': '226299d9-65a3-42db-9106-1824c35e1091', 'EmailType': 'ACCOUNT_VERIFICATION', 'Username': 'ct.iot.qa@gmail.com', 'Timestamp': '2024-11-02T16:51:39.898726+00:00'}]
        result = actual_result[0]
        log.debug(f"***** {result['Id']=}")

        assert result["EmailType"] == test_config.SQS_EMAIL_ACCOUNT_VERIFICATION_TYPE
        assert result["Username"] == test_config.SES_TARGET
