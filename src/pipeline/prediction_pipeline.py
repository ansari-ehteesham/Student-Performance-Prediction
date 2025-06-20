import os
import sys

from src.components.model_trainer import ModelTrainingConfig
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object

class PredictionPipeline:
    def __init__(self):
        self.model_path:str = ModelTrainingConfig().trained_model_path
        self.preprocess_path :str = os.path.join("artifacts", "preprocess.pkl")
        if not os.path.exists(self.model_path):
            trained_model_list = [file for file in os.listdir(os.path.dirname(self.model_path)) if "model" in file]
            self.model_path = os.path.join(
                os.path.dirname(self.model_path),
                max(trained_model_list)
            )
        
        logging.info(f"{self.model_path} is using for Prediction")

    def prediction(self, df):
        try:
            model = load_object(file_path=self.model_path)
            preprocessor = load_object(file_path=self.preprocess_path)
            logging.info("Model and Preprocessor is Loaded Successfully..")

            transformed_data = preprocessor.transform(df)
            preds = model.predict(transformed_data)
            logging.info("Prediction is Completed")
            return preds
        except Exception as e:
            raise CustomException(e, sys)
        

    

    