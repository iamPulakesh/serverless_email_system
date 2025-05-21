import boto3
import os
from datetime import datetime
import json

def lambda_handler(event, context):
    ses = boto3.client('ses', region_name='your-region')  # e.g., 'ap-south-1'
    dynamodb = boto3.resource('dynamodb', region_name='your-region')
    sqs = boto3.client('sqs', region_name='your-region')

    # Replace with your actual resource names
    DYNAMO_TABLE_NAME = 'YourDynamoDBTableName'
    DLQ_URL = 'https://sqs.your-region.amazonaws.com/your-account-id/YourDLQName'
    SENDER = "your-verified-sender@example.com"

    table = dynamodb.Table(DYNAMO_TABLE_NAME)

    # Parse body (for API Gateway or direct test event)
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event

    # Extract details from the request
    RECIPIENT = body.get('to')
    SUBJECT = body.get('subject')
    BODY_TEXT = body.get('message')

    try:
        # Send email
        response = ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': [RECIPIENT]},
            Message={
                'Subject': {'Data': SUBJECT},
                'Body': {'Text': {'Data': BODY_TEXT}}
            }
        )

        # Log success in DynamoDB
        table.put_item(
            Item={
                'id': response['MessageId'],
                'to': RECIPIENT,
                'subject': SUBJECT,
                'status': 'success',
                'timestamp': datetime.utcnow().isoformat()
            }
        )

        return {
            'statusCode': 200,
            'body': 'Email sent! Message ID: ' + response['MessageId']
        }

    except Exception as e:
        error_message = str(e)

        # Log failure in DynamoDB
        table.put_item(
            Item={
                'id': 'N/A',
                'to': RECIPIENT,
                'subject': SUBJECT,
                'status': 'failed',
                'error': error_message,
                'timestamp': datetime.utcnow().isoformat()
            }
        )

        # Send to DLQ
        try:
            sqs.send_message(
                QueueUrl=DLQ_URL,
                MessageBody=json.dumps({
                    'sender': SENDER,
                    'recipient': RECIPIENT,
                    'subject': SUBJECT,
                    'body': BODY_TEXT,
                    'error': error_message,
                    'timestamp': datetime.utcnow().isoformat()
                })
            )
        except Exception as sqs_error:
            print("Failed to send to DLQ:", str(sqs_error))

        return {
            'statusCode': 500,
            'body': 'Email failed to send: ' + error_message
        }
