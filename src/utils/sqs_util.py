import json


class SqsUtil:
    @staticmethod
    def create_sqs_email_message(
        message_id: str, email_type: str, username: str, timestamp: str
    ) -> dict:
        return dict(
            Id=message_id,
            MessageAttributes={
                "Id": {
                    "DataType": "String",
                    "StringValue": message_id,
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
                "Id": message_id,
                "EmailType": email_type,
                "Username": username,
                "Timestamp": timestamp,
            }),
            MessageDeduplicationId=message_id,
        )
