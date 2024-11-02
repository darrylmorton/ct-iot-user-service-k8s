import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

import config
from logger import log

from utils.sqs_util import SqsUtil


class EmailProducer:
    def __init__(self):
        log.debug("initializing EmailProducer...")

        self.sqs = boto3.resource("sqs", region_name=config.AWS_REGION)
        self.email_queue = self.sqs.Queue(f"{config.SQS_EMAIL_QUEUE_NAME}.fifo")
        self.email_dlq = self.sqs.Queue(f"{config.SQS_EMAIL_DLQ_NAME}.fifo")

    async def produce(self, email_type: str, username: str):
        message = SqsUtil.create_sqs_email_message(
            message_id=str(uuid.uuid4()),
            username=username,
            email_type=email_type,
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
        )
        log.debug(f"produce - sqs message {message=}")

        try:
            if email_type and username:
                self.email_queue.send_messages(Entries=[message])

                log.debug("produce - message sent")

            return message
        except ClientError as error:
            log.error(f"Couldn't produce email_queue messages error {error}")

            raise error
