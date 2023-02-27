import boto3
from botocore.config import Config

REGION = "us-east-1"

config = Config(region_name=REGION)

sqs = boto3.client('sqs', config=config)


def get_queue_url(name):
    res = sqs.get_queue_url(QueueName=name)
    if "QueueUrl" in res:
        return res["QueueUrl"]
    return False


def sqs_creator(name):
    try:
        res = sqs.create_queue(QueueName=name)
        return res['QueueUrl']
    except Exception as e:
        print("Exception: ", e)


def message_send(sqs_url, message, DelaySeconds=0):
    try:
        res = sqs.send_message(QueueUrl=sqs_url, MessageBody=message, DelaySeconds=DelaySeconds)
        return res
    except Exception as e:
        print("Exception: ", e)


def message_receive(sqs_url, MaxNumberOfMessages=10, WaitTimeSeconds=0):
    try:
        res = sqs.receive_message(QueueUrl=sqs_url,
                                  VisibilityTimeout=1,
                                  WaitTimeSeconds=WaitTimeSeconds,
                                  MaxNumberOfMessages=MaxNumberOfMessages)
        return res
    except Exception as e:
        print("Exception: ", e)


def message_delete(sqs_url, message_handle):
    try:
        res = sqs.delete_message(QueueUrl=sqs_url, ReceiptHandle=message_handle)
        return res
    except Exception as e:
        print("Exception: ", e)
