"""Implements class responsible for sending data to endpoint"""
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from decouple import config

from app.core.interfaces import MessageSender
from app.utils.logger import get_logger

TRACKING_SQS_URL = config('TRACKING_SQS_URL')
TRACKING_SQS_QUEUE_NAME = config('TRACKING_SQS_QUEUE_NAME')

logger = get_logger(__name__)
boto_config = Config(
    retries={
        'max_attempts': 5,
        'mode': 'standard'
    },
    connect_timeout=1,
    read_timeout=1
)


class SQSMessageSender(MessageSender):
    """Implements sending data to AWS SQS"""
    def __init__(
            self,
            endpoint_url: str = None,
            queue_name: str = None,
            ):
        self.endpoint_url: str = endpoint_url or TRACKING_SQS_URL
        self.queue_name: str = queue_name or TRACKING_SQS_QUEUE_NAME
        self.sqs = self._get_sqs_client(endpoint_url=self.endpoint_url)
        self._create_queue()
        self.queue_url = self._get_queue_url()

    def _get_sqs_client(self, endpoint_url):
        """Initializes client to access AWS SQS service"""
        sqs_client = boto3.client(
            'sqs',
            endpoint_url=endpoint_url,
        )
        return sqs_client

    def _get_queue_url(self):
        """Method to retrieve a queue url given its name"""
        try:
            response = self.sqs.get_queue_url(QueueName=self.queue_name)
            logger.debug("Queue creation response: %s", response)
            queue_url = response['QueueUrl']
        except ClientError as e:
            if e.response['Error']['Code'] == \
                    'AWS.SimpleQueueService.NonExistentQueue':
                log_message = f"Expected destination queue {self.queue_name}" \
                              " to exist, but it doesn't, creating a new one"
                logger.error(log_message)
                queue_url = self._create_queue()
            else:
                logger.error("Unexpected error: %s", e)
                raise

        return queue_url

    def _create_queue(self):
        """Try to create a new SQS queue"""
        try:
            response = self.sqs.create_queue(
                 QueueName=self.queue_name,
                 )
        except ValueError as e:
            raise RuntimeError("Failed to create queue, %s, %s",
                               self.queue_name, str(e)) from e
        return response['QueueUrl']

    def send_message(self, message: str):
        """Sends message to endpoint"""
        response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message,
                )
        logger.debug("Send message response: %s", response)
