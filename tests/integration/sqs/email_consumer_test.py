from tests.helper.email_helper import email_consumer, create_sqs_queue
from tests.helper.routes_helper import RoutesHelper
from tests.helper.user_helper import create_signup_payload
import tests.config as test_config
from user_service.service import app


class TestEmailConsumer:
    async def test_email_producer(self, db_cleanup, email_producer):
        email_queue, _ = create_sqs_queue(
            queue_name=test_config.SQS_EMAIL_QUEUE_NAME,
            dlq_name=test_config.SQS_EMAIL_DLQ_NAME,
        )

        payload = create_signup_payload()

        await RoutesHelper.http_post_client(app, "/api/signup", payload)

        actual_result = email_consumer(email_queue, 10)

        assert len(actual_result) == 1
        assert (
            actual_result[0]["EmailType"]
            == test_config.SQS_EMAIL_ACCOUNT_VERIFICATION_TYPE
        )
        assert actual_result[0]["Username"] == test_config.SES_TARGET
