import os
import sys
import dill
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging


def loading_env_varibales():
    load_dotenv()
    logging.info("Loaded .env Variables")

def mysql_connection_establishment(database_name):
    try:
        loading_env_varibales()
        cnx = mysql.connector.connect(
            user = os.getenv("MYSQL_USER"),
            password = os.getenv("MYSQL_PASSWORD"),
            host="localhost",
            database = database_name
        )
        logging.info("Conection Established Succefullly with MySQL")

        return cnx
    except Exception as e:
        raise CustomException(e, sys)
    
def fetch_dataset(mysql_connection):
    try:
        logging.info("Trying to fetch the Dataset")
        with mysql_connection.cursor() as cursor:
            mysql_query = cursor.execute("SELECT * FROM performance")
            columns_name = [i[0] for i in cursor.description]
            all_rows = cursor.fetchall()
            cursor.close()
        return all_rows, columns_name
    except Exception as e:
        raise CustomException(e, sys)
    
def convert_dataset_as_dataframe(dataset, column):
    try:
        df = pd.DataFrame(dataset, columns=column)
        logging.info("DataFrame has been Created")
        return df
    except Exception as e:
        raise CustomException(e, sys)
    
def dataset_split(raw_dataset,):
    try:
        logging.info("Splitting Dataset into Train and Test Dataset")
        
        X_train, X_test = train_test_split(raw_dataset, test_size=0.2, random_state=42)
        logging.info(f"Successfully Splitted Train and Test Dataset into 2 parts")
        return X_train, X_test

    except Exception as e:
        raise CustomException(e, sys)

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Model Dumping Successfully")

    except Exception as e:
        raise  CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as obj:
            return dill.load(obj)
    except Exception as e:
        raise CustomException(e, sys)
    
def inserting_data_mysql(mysql, data):
    if mysql.is_connected():
        cursor = mysql.cursor()
        add_data_query = (
                "INSERT INTO secondary_table"
                "(gender, race_ethnicity, parental_level_of_education, lunch, test_preparation, math_score, reading_score, writing_score) "
                "VALUES (%(gender)s, %(race_ethnicity)s, %(parental_level_of_education)s, %(lunch)s, %(test_preparation)s, %(math_score)s, %(reading_score)s, %(writing_score)s)"
            )
        cursor.execute(add_data_query, data)
        mysql.commit()
        cursor.close()
        logging.info("Data has been uploaded to MySQL Database")
        return None