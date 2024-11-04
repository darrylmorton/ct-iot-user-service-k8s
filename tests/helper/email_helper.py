import json
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import boto3

from logger import log
import tests.config as test_config


def create_sqs_queue(queue_name: str, dlq_name="") -> tuple[Any, Any]:
    sqs = boto3.resource("sqs", region_name=test_config.AWS_REGION)
    queue_attributes = {
        "WaitSeconds": f"{queue_name}",
    }
    dlq = None

    if dlq_name:
        dlq = sqs.create_queue(
            QueueName=f"{dlq_name}.fifo", Attributes=queue_attributes
        )

        dlq_policy = json.dumps({
            "deadLetterTargetArn": dlq.attributes["QueueArn"],
            "maxReceiveCount": "10",
        })

        queue_attributes["RedrivePolicy"] = dlq_policy

    queue = sqs.create_queue(
        QueueName=f"{queue_name}.fifo", Attributes=queue_attributes
    )

    return queue, dlq


def create_email_message(
    email_type: str,
    username: str,
    message_id=uuid.uuid4(),
    timestamp=datetime.now(tz=timezone.utc).isoformat(),
) -> dict:
    return dict(
        Id=str(message_id),
        MessageAttributes={
            "Id": {
                "DataType": "String",
                "StringValue": str(message_id),
            },
            "EmailType": {
                "DataType": "String",
                "StringValue": email_type,
            },
            "Username": {
                "DataType": "String",
                "StringValue": username,
            },
            "Timestamp": {
                "DataType": "String",
                "StringValue": timestamp,
            },
        },
        MessageBody=json.dumps({
            "Id": str(message_id),
            "EmailType": email_type,
            "Username": username,
            "Timestamp": timestamp,
        }),
        MessageDeduplicationId=str(message_id),
    )


def email_consumer(email_queue: Any, timeout_seconds=0) -> list[dict]:
    timeout = time.time() + timeout_seconds
    messages = []

    while True:
        if time.time() > timeout:
            log.info(f"Task timed out after {timeout_seconds}")
            break

        email_messages = email_queue.receive_messages(
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=test_config.QUEUE_WAIT_SECONDS,
        )

        if len(email_messages) > 0:
            for email_message in email_messages:
                message_body = json.loads(email_message.body)
                messages.append(message_body)

                email_message.delete()

    return messages
