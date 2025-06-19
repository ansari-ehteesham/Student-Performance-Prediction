from src.components.data_ingestion import DataIngestion, DataIngestionConfig
from src.components.data_transformation import DataTrannsformationConfig, DataTransformation


if __name__ == "__main__":
    print("-"*25,"Data Ingestion Started","-"*25)
    data_ingestion = DataIngestion()
    train_path, test_path = data_ingestion.data_ingestion_initiate()
    print("-"*25,"Data Ingestion Completed","-"*25)

    print("-"*25,"Data Transformation Started","-"*25)
    data_transforamtion = DataTransformation()
    train_arr, test_arr = data_transforamtion.initiate_data_transformation(train_path=train_path, test_path=test_path)
    print("-"*25,"Data Transformation Completed","-"*25)