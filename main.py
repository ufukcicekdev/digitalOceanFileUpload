import os
import boto3
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Load settings using environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_STORAGE_DICT_PATH = os.getenv('AWS_STORAGE_DICT_PATH')

# Path to the "UploadDict" folder in the root directory
upload_folder_path = 'UploadDict'

# Create a Boto3 client
session = boto3.session.Session()
s3 = session.client('s3',
                   region_name=AWS_S3_REGION_NAME,
                   endpoint_url=AWS_S3_ENDPOINT_URL,
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Iterate through files in the folder and upload them to remote storage
for root, dirs, files in os.walk(upload_folder_path):
    for file_name in files:
        local_file_path = os.path.join(root, file_name)
        remote_file_name = f'{AWS_STORAGE_DICT_PATH}{file_name}'

        try:
            print(f'Uploading file to remote storage: {file_name}')
            s3.upload_file(local_file_path, AWS_STORAGE_BUCKET_NAME, remote_file_name, ExtraArgs={'ACL': 'public-read'})
        except Exception as e:
            print(f'Error: {str(e)}')

print('All files have been successfully uploaded.')
