import boto3
from dotenv import load_dotenv
from os.path import isfile, join

def upload_data(aws_access_key_id, aws_secret_access_key, file_name, bucket_name, bucket_file_path):

    # Create an S3 Client using AWS Credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    print('s3_client created')

    # Upload file (Key) to S3 Bucket
    s3_client.upload_file(
        Filename = file_name,
        Bucket = bucket_name,
        Key = bucket_file_path)
    