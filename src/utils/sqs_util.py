import json

import config


class SqsUtil:
    @staticmethod
    def create_sqs_email_message(
        message_id: str, email_type: str, username: str, timestamp: str, token: str
    ) -> dict:
        message_url = f"{config.ALB_URL}/?token={token}"

        return dict(
            Id=message_id,
            MessageAttributes={
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
                "Url": {
                    "DataType": "String",
                    "StringValue": message_url,
                },
            },
            MessageBody=json.dumps({
                "EmailType": email_type,
                "Username": username,
                "Timestamp": timestamp,
                "Url": message_url,
            }),
            MessageDeduplicationId=message_id,
        )
