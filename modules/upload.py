import boto3
from dotenv import load_dotenv
from os.path import isfile, join

def upload_data(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, FILE_NAME, BUCKET_NAME, BUCKET_FILE_PATH):

    # Create an S3 Client using AWS Credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    print('s3_client created')

    # Upload file (Key) to S3 Bucket
    s3_client.upload_file(
        Filename = FILE_NAME,
        Bucket = BUCKET_NAME,
        Key = BUCKET_FILE_PATH)
    