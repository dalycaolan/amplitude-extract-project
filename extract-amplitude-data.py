import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time
import logging
<<<<<<< HEAD
from modules import unzip_and_store
=======
import zipfile
import gzip
>>>>>>> da830115a2c9ad77656d34c0670998504f4b1093

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

#Create start and end date dynamically, end date yesterday and roll back seven days

end_date = datetime.now() - timedelta(days=1)
end = end_date.strftime('%Y%m%d')+'T00'


start_date = datetime.now() - timedelta(days=7)
start = start_date.strftime('%Y%m%d')+'T00'


import requests

# API endpoint is the EU residency server
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start,
    'end': end
}


# Make the GET request with basic authentication
response = requests.get(url, params=params, auth=(api_key, secret_key))

#Error handling

response_code=response.status_code
<<<<<<< HEAD
destination_filepath = "data/amplitude_data.zip"
=======


>>>>>>> da830115a2c9ad77656d34c0670998504f4b1093

number_tries=0

while number_tries<3:

    if response_code == 200:
        # The request was successful
        data = response.content 
        print('Data retrieved successfully.')
        # JSON data files saved to a zip folder 'data.zip'
<<<<<<< HEAD
        with open(destination_filepath, 'wb') as file:
            file.write(data)

            print(f'Download successful lets goooo ☘️')
            logger.info(f'Download successful ☘️, stored as amplitude_data.zip') 

        unzip_and_store(destination_filepath)
=======
        with open(f'amplitude_data_{start}_{end}.zip', 'wb') as file:
            file.write(data)

            print(f'Download successful lets goooo ☘️')
            logger.info(f'Download successful ☘️, stored as amplitude_data_{start}_{end}.zip') 
>>>>>>> da830115a2c9ad77656d34c0670998504f4b1093

        break

    elif response_code<200 and response_code>499:
        
        print(response.reason)
        time.sleep(10)
        logger.warning(response.reason) 

        count+=1


    else:
        # The request failed; print the error
        print(f'Error {response_code}: {response.text}')

        break

