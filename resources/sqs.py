import boto3
from botocore.config import Config

REGION = "us-east-1"

config = Config(region_name=REGION)

sqs = boto3.client('sqs', config=config)


def sqs_creator(name):
    try:
        res = sqs.create_queue(QueueName=name)
        return res['QueueUrl']
    except Exception as e:
        print("Exception: ", e)


def message_send(sqs_url, message):
    try:
        res = sqs.send_message(QueueUrl=sqs_url, MessageBody=message)
        return res
    except Exception as e:
        print("Exception: ", e)


def message_receive(sqs_url):
    try:
        res = sqs.receive_message(QueueUrl=sqs_url,
                                  VisibilityTimeout=1,
                                  WaitTimeSeconds=0,
                                  MaxNumberOfMessages=10)
        return res
    except Exception as e:
        print("Exception: ", e)


async def message_delete(sqs_url, message_handle):
    try:
        res = await sqs.delete_message(QueueUrl=sqs_url, ReceiptHandle=message_handle)
        return res
    except Exception as e:
        print("Exception: ", e)
