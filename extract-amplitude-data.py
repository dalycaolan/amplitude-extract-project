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
destination_pf = f'data/'
destination_filepath = f"{destination_pf}amplitude_data.zip"
json_filepath = f'{destination_pf}json_data'

number_tries=0

while number_tries<3:

    if response_code == 200:
        # The request was successful
        data = response.content 
        print('Data retrieved successfully.')
        # JSON data files saved to a zip folder 'data.zip'
        with open(destination_filepath, 'wb') as file:
            file.write(data)

            print(f'Download successful lets goooo ☘️')
            logger.info(f'Download successful ☘️, storing as amplitude_data.zip') 
        
            try:
                unzip_and_store(destination_filepath)
                print('Storage successfull lets gooo ☘️ ☘️')
                logger.info(f'Unzipping and storage successful, loaded into {json_filepath} ☘️☘️')
            except:
                with Exception as e:
                    logger.warning(f'Unzipping and storage successful, loaded into {json_filepath} ☘️☘️')
    
        break

    elif response_code<200 and response_code>499:
        
        # Print response reason and try again
        print(response.reason)
        time.sleep(10)
        logger.warning(response.reason) 

        count+=1


    else:
        
        # The request failed; print the error
        print(f'Error {response_code}: {response.text}')

        break

