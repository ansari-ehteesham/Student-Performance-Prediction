import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.utils import mysql_connection_establishment
from src.exception import CustomException
from src.logger import logging

class TrainingPipeline:
    def __init__(self):
        pass

    def update_database(self, cnx):
        try:
            if cnx.is_connected():
                cursor = cnx.cursor()

                merging_query = (
                    '''INSERT INTO performance
                    select * from secondary_table'''
                )

                cursor.execute(merging_query)

                deletion_query = (
                    "TRUNCATE TABLE secondary_table"
                )

                cursor.execute(deletion_query)
            cnx.commit()
            logging.info("Database has been Updated")
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def run(self, cnx):
        # updating the database
        self.update_database(cnx)

        print("-"*25,"Data Ingestion Started","-"*25)
        data_ingestion = DataIngestion()
        train_path, test_path = data_ingestion.data_ingestion_initiate(mysql=cnx)
        print("-"*25,"Data Ingestion Completed","-"*25)

        print("-"*25,"Data Transformation Started","-"*25)
        data_transforamtion = DataTransformation()
        train_arr, test_arr = data_transforamtion.initiate_data_transformation(train_path=train_path, test_path=test_path)
        print("-"*25,"Data Transformation Completed","-"*25)
        
        print("-"*25,"Model Training Started","-"*25)
        model_trainer = ModelTrainer()
        best_model = model_trainer.initiate_model_training(train_arr=train_arr, test_arr=test_arr)
        print("Best Model -",best_model)
        print("-"*25,"Model Training Completed","-"*25)
        