import os
import sys
import pandas as pd
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
from src.utils import (fetch_dataset, 
                       convert_dataset_as_dataframe,
                       dataset_split)

@dataclass(frozen=True)
class DataIngestionConfig:
    train_dataset_path: str = os.path.join("artifacts", "train.csv")
    test_dataset_path: str = os.path.join("artifacts", "test.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def data_ingestion_initiate(self, mysql):
        try:
            # creating directory
            if not (os.path.exists(self.data_ingestion_config.train_dataset_path)) or not (os.path.exists(self.data_ingestion_config.test_dataset_path)):
                os.makedirs(os.path.dirname(self.data_ingestion_config.train_dataset_path), exist_ok=True)
                os.makedirs(os.path.dirname(self.data_ingestion_config.test_dataset_path), exist_ok=True)
                logging.info("Artifacts directory has been Created")

            # Establishing Connection with MySQL
            if mysql and mysql.is_connected():
                result, columns_name = fetch_dataset(mysql_connection=mysql)
            raw_dataframe = convert_dataset_as_dataframe(dataset=result, column=columns_name)
            
            # splitting the dataset
            train, test = dataset_split(raw_dataset=raw_dataframe)

            # saving the splitted dataset
            train.to_csv(self.data_ingestion_config.train_dataset_path, index=False, header=True)
            test.to_csv(self.data_ingestion_config.test_dataset_path, index=False, header=True)

            logging.info("Train and Test Data has been Stored Succesfully")

            return (
                self.data_ingestion_config.train_dataset_path,
                self.data_ingestion_config.test_dataset_path,
            )

        except Exception as e:
            raise CustomException(e, sys)