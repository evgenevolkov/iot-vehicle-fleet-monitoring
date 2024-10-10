"""
Implementation of Lambda function that shifts tracking messages from
SQS queue to DynamoDB table.
"""
import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def lambda_handler(event, context):
    """Lambda function entry point"""
    for record in event['Records']:
        message_body = json.loads(record['body'])
        vehicle_id = message_body.get('vehicle_id', 'unknown')
        table.put_item(
            Item={
                'vehicle_id': vehicle_id,
                'data': message_body
            }
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }
