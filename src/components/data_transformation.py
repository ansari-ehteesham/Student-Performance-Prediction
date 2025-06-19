import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass(frozen=True)
class DataTrannsformationConfig:
    preprocess_obj_file = os.path.join("artifacts", "preprocess.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTrannsformationConfig()

    def get_data_transformation_obj(self, num_cols, cat_cols):
        try:
            # making pre-processing pipeline
            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("Pipeline has been Created for Categorical and Numerical Features")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, num_cols),
                    ("categorical_pipeline", categorical_pipeline, cat_cols)
                ]
            )

            logging.info("Preprocesser has been Created")

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            # reading the train and test dataset
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading the Dataset Completed")

            # Target Column
            target_col = "math_score"

            # extracting the numerical and categorical columns
            raw_numerical_cols = train_df.select_dtypes(include="number").columns.to_list()
            raw_numerical_cols.remove(target_col)

            categorical_cols = train_df.select_dtypes(include="O").columns.to_list()
            
            # Getting Preprocessor object
            preprocessing_obj = self.get_data_transformation_obj(num_cols=raw_numerical_cols, cat_cols=categorical_cols)

            # preparing the dataset for preprocessor
            input_feature_train = train_df.drop(columns=[target_col], axis=1)
            train_target_col = train_df[target_col]
            
            input_feature_test = test_df.drop(columns=[target_col], axis=1)
            test_target_col = test_df[target_col]

            logging.info("Applying preprocessing object on trian and test dataset")

            input_train_arr = preprocessing_obj.fit_transform(input_feature_train)
            input_test_arr = preprocessing_obj.transform(input_feature_test)

            # Concatenation of input feature and target feature as array
            train_arr = np.c_[
                input_train_arr, np.array(train_target_col)
            ]

            test_arr = np.c_[
                input_test_arr, np.array(test_target_col)
            ]

            save_object(file_path=self.data_transformation_config.preprocess_obj_file, obj=preprocessing_obj)
            logging.info("Preprocessing object saved Successfully...")

            return (
                train_arr,
                test_arr
            )

        except Exception as e:
            raise CustomException(e, sys)