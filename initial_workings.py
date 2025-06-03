import boto3
from dotenv import load_dotenv
import os
from os.path import isfile, join
from modules.upload import(upload_data)

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')
bucket_file_path = os.getenv('BUCKET_FILE_PATH')
output_folder = 'json_data'

onlyfiles = [f for f in os.listdir(output_folder) if isfile(join(output_folder, f))]

for file in onlyfiles:
    file_name = output_folder + '/' + file
    bucket_file_name = bucket_file_path + 'campaign/' + file
    upload_data(aws_access_key_id, aws_secret_access_key, file_name, bucket_name, bucket_file_name)
    print(file_name)
