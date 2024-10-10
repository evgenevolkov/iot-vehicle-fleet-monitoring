import boto3
import pytest


@pytest.mark.timeout(2)
@pytest.fixture(name="sqs_client")
# Instantiate boto SQS client
def sqs_client_fixture():
    sqs = boto3.client(
        'sqs',
        # LocalStack's endpoint for AWS services
        endpoint_url='http://localhost:4566',
        region_name='eu-central-1',
        # Dummy credentials for LocalStack
        aws_access_key_id='mock_access_key',
        aws_secret_access_key='mock_secret_key'
    )
    yield sqs

@pytest.mark.timeout(2)
def test_can_send_sqs_message_to_localstack_sqs(sqs_client):
    """Test if sqs client can send a message to localstack sqs queue"""
    try:
        response = sqs_client.send_message(
            QueueUrl='http://localhost:4566/000000000000/vehicle-tracking',
            MessageBody='pytest test_can_send_sqs_message_to_localstack_sqs'
        )
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200, (
            f"Expected response with status code 200, got: {response}"
            )
    except Exception as e:
        pytest.fail(f"Failed to send a message to SQS. Error: {e}")
