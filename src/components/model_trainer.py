import os
import sys
import numpy as np
from dataclasses import dataclass
from datetime import date
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    GradientBoostingRegressor,
    AdaBoostRegressor,
    RandomForestRegressor
)
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, dataset_split

current_date = str(date.today())

@dataclass(frozen=True)
class ModelTrainingConfig:
    trained_model_path: str = os.path.join("artifacts", f"model-{current_date}.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainingConfig()

    def model_training(self, X_train, X_test, y_train, y_test, models_dict):
        try:
            number_of_model = len(models_dict)
            report = {}

            for i in range(number_of_model):
                model = list(models_dict.values())[i] # model selection
                logging.info(f"{model} is Selected")

                model.fit(X_train, y_train) # model training
                logging.info(f"{model} trianing is Finished")

                prediction = model.predict(X_test) # prediction on unseen data
                score = r2_score(y_test, prediction) # calculating the score
                logging.info(f"{model} model Score Checked")

                report[list(models_dict.keys())[i]] = score # storing the score with their model name
            
            logging.info("All Model Trained and their respective score has been Stored")
            return report
                
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_training(self, train_arr, test_arr):
        try:
            main_arr = (train_arr, test_arr)
            X_train, X_test, y_train, y_test = (
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:, -1]
            )
            
            models = {
                "Linear Regression": LinearRegression(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Ada Boosting": AdaBoostRegressor(),
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "K-Neighbors": KNeighborsRegressor(),
                "XG Boosting": XGBRegressor(),
                "Cat Boosting": CatBoostRegressor()
            }
            logging.info("All Model are loaded")

            all_model_report:dict = self.model_training(X_train, X_test, y_train, y_test, models)

            # getting the best model score
            best_model_score = max(sorted(all_model_report.values()))

            # getting the best model name
            best_model_name = list(all_model_report.keys())[
                list(all_model_report.values()).index(best_model_score)
                ]
            
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No Best Model is Found", sys)
            logging.info(f"Best Model Name - {best_model_name} with Score - {best_model_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_path,
                obj=best_model
            )

            return {best_model_name:best_model_score}
        except Exception as e:
            raise CustomException(e, sys)