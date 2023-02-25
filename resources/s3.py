from botocore.config import Config
import boto3

REGION = 'us-east-1'
BClient = boto3.client('s3', region_name=REGION, config=Config(signature_version='s3v4'))


def bucket_creator(name):
    try:
        res = BClient.create_bucket(Bucket=name)
        return res
    except Exception as e:
        print('Exception: ', e)


def file_upload(bucket, file, file_path):
    try:
        res = BClient.put_object(Bucket=bucket, Key=file_path, Body=file)
        return res
    except Exception as e:
        print('Exception: ', e)
