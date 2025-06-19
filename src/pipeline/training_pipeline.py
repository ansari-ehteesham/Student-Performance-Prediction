from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainingPipeline:
    def __init__(self):
        pass



if __name__ == "__main__":
    print("-"*25,"Data Ingestion Started","-"*25)
    data_ingestion = DataIngestion()
    train_path, test_path = data_ingestion.data_ingestion_initiate()
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