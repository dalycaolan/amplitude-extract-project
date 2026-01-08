import os          
import zipfile     
import gzip        
import shutil     
import tempfile  

# Create a temporary directory for extraction

def unzip_and_store(file_path):

    temp_dir = tempfile.mkdtemp()

    # Create local output directory

    data_dir = "json_data"
    os.makedirs(data_dir, exist_ok=True)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
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