import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time
import logging
from modules.extract_json import unzip_and_store, extract_function, load_data
import boto3

# Creating logs directory if it does not exist

logs_dir= 'logs'
if os.path.exists(logs_dir):
    pass
else:
    os.mkdir(logs_dir)

filename = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_filename = f"logs/api_response_logs_{filename}.log"

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)


logger=logging.getLogger()

file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# For easy copying and pasting

# logger.debug("This is a debug message")    
# logger.info("System working")            
# logger.warning("Something unexpected")        
# logger.error("An error occurred")             
# logger.critical("Critical system error")

#Load in credentials

load_dotenv()

api_key=os.getenv('AMP_API_KEY')
secret_key= os.getenv('AMP_SECRET_KEY')
amp_region=os.getenv('AMP_DATA_REGION')

# Read .env file
aws_access_key=os.getenv('AWS_ACCESS_KEY')
aws_secret_key=os.getenv('AWS_SECRET_KEY')
aws_bucket_name=os.getenv('BUCKET_NAME')

# Create S3 Client using AWS Credentials
s3_client = boto3.client(
    's3',
    # aws_access_key_id=aws_access_key,
    # aws_secret_access_key=aws_secret_key
)


logger.info('Credentials loaded in')

#Create start and end date dynamically, end date yesterday and roll back seven days

end_date = datetime.now() - timedelta(days=1)
end = end_date.strftime('%Y%m%d')+'T00'


start_date = datetime.now() - timedelta(hours=1)
start = start_date.strftime('%Y%m%d')+'T00'


# response = s3_client.list_objects_v2(Bucket=aws_bucket_name)

# Extract the 'Contents' key which contains the object metadata
# list_of_jsons=[]
# if 'Contents' in response:
#     for obj in response['Contents']:
#         list_of_jsons.append(obj['Key'].replace('python-import/',''))
# else:
#     print("Bucket is empty or does not exist.")

# print(list_of_jsons)

# boto3.list_s3_objects(aws_bucket_name)

# API endpoint is the EU residency server
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start,
    'end': end
}

logger.info('Parameters defined')

extract_function(params, url, api_key,secret_key)

load_data()


# number_tries=0

# while number_tries<3:

#     # Make the GET request with basic authentication
#     response = requests.get(url, params=params, auth=(api_key, secret_key))

# #Error handling
#     response_code=response.status_code
#     destination_pf = f'data/'

#     file_date = datetime.now().strftime('%Y%m%dT%H-%M-%S')
#     destination_filepath = f"{destination_pf}amplitude_data_{file_date}.zip"
#     json_filepath = f'json_data/{file_date}'

#     logger.info('Attempting API request...')

#     if response_code == 200:

#         # The request was successful

#         data = response.content 
#         logger.info('Data retrieved successfully. Attempting to zip.')
#         # JSON data files saved to a zip folder 'data.zip'
#         with open(destination_filepath, 'wb') as file:
#             file.write(data)

#             print(f'Download successful lets goooo ☘️')
#             logger.info(f'Download successful, storing as amplitude_data_{file_date}.zip') 
        
#             try:
#                 unzip_and_store(destination_filepath, file_date)
#                 print('Storage successfull lets gooo ☘️ ☘️')
#                 logger.info(f'Unzipping and storage successful, loaded into {json_filepath}')
#             except:
#                 with Exception as e:
#                     logger.warning(f'Unzipping unsuccessful :(')
    
#         break

#     elif response_code<200 and response_code>499:
        
#         # Print response reason and try again
        
#         logger.warning(response.reason) 
#         time.sleep(10)
    
#         count+=1


#     else:
        
#         # The request failed; print the error
#         print(f'Error {response_code}: {response.text}')
#         logger.error(f'Error {response_code}: {response.text}')

#         break

