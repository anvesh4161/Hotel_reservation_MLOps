import sys
import os

# Get the root directory (parent of src)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)  # Add root directory to Python path

from src.custom_exception import CustomException  # Import again after adding path

import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
#from src.custom_exception import CustomException
from src.logger import get_logger
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion started with {self.bucket_name} and file is  {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"CSV FILE IS SUCCESSFULLY DOWNLOADED TO {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the CSV file")
            raise CustomException("Failed to download CSV file", e)
        
    def split_data(self):
        try:
            logger.info("Starting the splitting process")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"TRAIN data saved to {TRAIN_FILE_PATH}")
            logger.info(f"TEST data saved to {TEST_FILE_PATH}")

        except Exception as e:
            logger.error("Error while splitting the data")
            raise CustomException("Failed to split the data into training and test sets", e)
        
    def run(self):

        try:
            logger.info("Starting data ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data Ingestion completed successfully")

        except Exception as ce:
            logger.error(f"Custom Exception : {str(ce)}")
            
        finally:
            logger.info("Data Ingestion Completed")

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

