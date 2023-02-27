import json
import os
import time

from image_classification import model, process
from resources.s3 import download_file, file_upload, bucket_creator
from resources.sqs import get_queue_url, message_receive, message_delete, message_send

req_queue_url = get_queue_url("request-queue")
res_queue_url = get_queue_url("response-queue")
output_bucket = "cse546-image-processing-op"
bucket_creator(output_bucket)

if not req_queue_url or not res_queue_url:
    raise Exception("Request or Response queue not created. Please create before starting app-tier.")

model = model()


def process_images():
    timer = 0
    timeout=True
    while True:
        time.sleep(2.5)
        try:
            response = message_receive(
                req_queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=timer
            )
            if "Messages" in response:
                message = response["Messages"][0]
                receipt_handle = message["ReceiptHandle"]
                params = json.loads(message["Body"])
                file_path = params["Key"]
                download_file(params['Bucket'], params['Key'], file_path)
                prediction, status = process(model, file_path)
                if status:
                    txt_file_name = file_path.split('.')[0] + ".txt"
                    file = open(txt_file_name, "w")
                    result = json.loads(prediction)['Result']
                    file.write(file_path + ", " + result)
                    file.close()
                    with open(txt_file_name, 'rb') as f:
                        file_upload(output_bucket, f, txt_file_name)
                    message_delete(req_queue_url, receipt_handle)
                    message_send(res_queue_url, prediction, DelaySeconds=0)
                    os.remove(file_path)
                    os.remove(txt_file_name)
                timer = 0
        except Exception as e:
            print(e)
        else:
            timer = 2


process_images()
