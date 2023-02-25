from flask import Flask, request
import json
import time
import asyncio
import boto3
from botocore.exceptions import ClientError
from resources.sqs import sqs_creator, message_send, message_receive, message_delete
from resources.s3 import bucket_creator, file_upload

app = Flask(__name__)

OUTPUT = {}

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

BUCKET = 'cse546-cc-autoscale-input-bucket'
bucket_creator(BUCKET)

request_queue = sqs_creator('request-queue')
response_queue = sqs_creator('response-queue')


async def get_responses(key):
    while True:
        time.sleep(0.5)
        try:
            response = message_receive(response_queue)
            if 'Messages' in response:
                for message in response['Messages']:
                    msg = json.loads(message['Body'])
                    OUTPUT[msg['Key']] = msg['Result']
                    await message_delete(response_queue, message['ReceiptHandle'])
            res = check_responses(key)
            if res:
                return res

        except ClientError as e:
            print(e)


def check_responses(key):
    if key in OUTPUT:
        res = key + ' ' + OUTPUT[key]
        del OUTPUT[key]
        return res


@app.route('/', methods=['POST'])
def upload_file():
    key = request.files['myfile'].filename
    file_upload(BUCKET, request.files['myfile'], key)
    message_send(request_queue,
                 json.dumps({'Bucket': BUCKET, 'Key': key}))
    res = asyncio.run(get_responses(key))
    return res


# asyncio.run(get_responses())
if __name__ == '__main__':
    app.run(debug=True, port=3000)
