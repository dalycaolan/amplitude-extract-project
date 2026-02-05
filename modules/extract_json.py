import os          
import zipfile     
import gzip        
import shutil     
import tempfile
from datetime import datetime
import logging
import requests
from datetime import datetime
import time
from dotenv import load_dotenv
from pathlib import Path
import boto3

logger=logging.getLogger()

# Create a temporary directory for extraction

def unzip_and_store(file_path, file_date):

    temp_dir = tempfile.mkdtemp()
    # logger.info('Temporary directory made')

    # Create local output directory

    data_dir = f"json_data/{file_date}"
    os.makedirs(data_dir, exist_ok=True)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        # logger.info('Extracting gzip files...')
        zip_ref.extractall(temp_dir)

    day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
    day_path = os.path.join(temp_dir, day_folder)

    for root, _, files in os.walk(day_path):
        for file in files:
            if file.endswith('.gz'):
                # Process each .gz file
                print(file)

                gz_path = os.path.join(root, file)
                json_filename = file[:-3]  
                output_path = os.path.join(data_dir, json_filename)

                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file)

    shutil.rmtree(temp_dir)

    # logger.info('gzip files succesfully parsed into JSON and loaded successfully :)')
def extract_function(params, url, api_key,secret_key, count=0 ):

    os.makedirs('data',exist_ok=True)

    while count<3:

        # Make the GET request with basic authentication
        api_response = requests.get(url, params=params, auth=(api_key, secret_key))
            
        response_code=api_response.status_code
        destination_pf = f'data/'

        file_date = datetime.now().strftime('%Y%m%dT%H-%M-%S')
        destination_filepath = f"{destination_pf}amplitude_data_{file_date}.zip"
        json_filepath = f'json_data/{file_date}'

        logger.info('Attempting API request...')

        if response_code == 200:

            # The request was successful

            data = api_response.content 
            logger.info('Data retrieved successfully. Attempting to zip.')
            # JSON data files saved to a zip folder 'data.zip'
            with open(destination_filepath, 'wb') as file:
                file.write(data)

                print(f'Download successful lets goooo ☘️')
                logger.info(f'Download successful, storing as amplitude_data_{file_date}.zip') 
            
                try:
                    unzip_and_store(destination_filepath, file_date)
                    print('Storage successfull lets gooo ☘️ ☘️')
                    logger.info(f'Unzipping and storage successful, loaded into {json_filepath}')
                except:
                    with Exception as e:
                        logger.warning(f'Unzipping unsuccessful :(')
            break

        elif (response_code<200 and response_code>499) or response_code==429:
            
            # Print response reason and try again
            print(f'Warning: {api_response.reason}. Trying again...')
            logger.warning(api_response.reason) 
            time.sleep(10)
        
            count+=1


        else:
            
            # The request failed; print the error
            print(f'Error {response_code}: {api_response.text}')
            logger.error(f'Error {response_code}: {api_response.text}')

            break

def load_data(aws_access_key,aws_secret_key,aws_bucket_name):

    # Retrieve .json files and upload json files to S3 bucket

    # Create S3 Client using AWS Credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )


    # Extract the main zip file
    # zip_path = "data.zip"
    # unzip_and_store(zip_path,output_folder) 

    os.makedirs("json_data", exist_ok=True) 
    output_folder = "json_data"
    files_to_upload = []
    for root, _, filenames in os.walk(output_folder):
        for filename in filenames:
            full_path=os.path.join(root,filename)
            files_to_upload.append(full_path)

    for file in files_to_upload:
        file_path=Path(file)
        aws_file_destination = "python-import/" + file_path.name
        output_path = file
        s3_client.upload_file(output_path, aws_bucket_name, aws_file_destination)
        print(f"✓ Uploaded: {file}, name is {aws_file_destination}")
        os.remove(file)
