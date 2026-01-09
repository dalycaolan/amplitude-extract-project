import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time
import logging
from modules import unzip_and_store

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


logger.info('Credentials loaded in')

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

logger.info('Parameters defined')


# Make the GET request with basic authentication
response = requests.get(url, params=params, auth=(api_key, secret_key))

#Error handling
response_code=response.status_code
destination_pf = f'data/'

file_date = datetime.now().strftime('%Y%m%dT%H-%M-%S')
destination_filepath = f"{destination_pf}amplitude_data_{file_date}.zip"
json_filepath = f'json_data/{file_date}'

number_tries=0

while number_tries<3:

    logger.info('Attempting API request...')

    if response_code == 200:

        # The request was successful

        data = response.content 
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

    elif response_code<200 and response_code>499:
        
        # Print response reason and try again
        
        logger.warning(response.reason) 
        time.sleep(10)
    
        count+=1


    else:
        
        # The request failed; print the error
        print(f'Error {response_code}: {response.text}')
        logger.error(f'Error {response_code}: {response.text}')

        break

