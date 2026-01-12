# Retrieve .json files and upload json files to S3 bucket

# Load libraries
import os
import boto3
from dotenv import load_dotenv
from modules.extract_json import unzip_and_store

# Load .env file
load_dotenv()

# Read .env file
aws_access_key=os.getenv('AWS_ACCESS_KEY')
aws_secret_key=os.getenv('AWS_SECRET_KEY')
aws_bucket_name=os.getenv('BUCKET_NAME')

# Create S3 Client using AWS Credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# Extract the main zip file
# zip_path = "data.zip"
output_folder = "json_data"
# unzip_and_store(zip_path,output_folder) 

files_to_upload = []
for root, dirs, filenames in os.walk(output_folder):
    for filename in filenames:
        full_path=os.path.join(root,filename)
        files_to_upload.append(full_path)
print(files_to_upload)

for file in files_to_upload:
    aws_file_destination = "python-import/" + file
    output_path = file
    s3_client.upload_file(output_path, aws_bucket_name, aws_file_destination)
    print(f"✓ Uploaded: {file}")