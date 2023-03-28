from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import sys, os
from Insurance.entity.config_entity import DataIngestionConfig
from Insurance.entity import config_entity
from Insurance.components.data_ingestion import DataIngestion
from Insurance.components.data_validation import DataValidation
from Insurance.components.data_transformation import DataTransformation
from Insurance.components.model_trainer import ModelTrainer
#from Insurance.components.model_evaluation import ModelEvaluation
#from Insurance.components.model_pusher import ModelPusher


#def test_logger_and_expection():
   # try:
       # logging.info("Starting the test_logger_and_exception")
        #result = 3/0
       # print(result)
       # logging.info("Stoping the test_logger_and_exception")
    #except Exception as e:
      #  logging.debug(str(e))
       # raise InsuranceException(e, sys)

if __name__=="__main__":
     try:
          #start_training_pipeline()
          #test_logger_and_expection()
          
       #calling the function to read data
       # get_collection_as_dataframe(database_name ="INSURANCE", collection_name = 'INSURANCE_PROJECT')

       #this is taking  our data after getting from db and we calling this from config_entity.
       #in below 3 lines we are calling function to create  the data artifact and then initiate data_ingestion. 
       training_pipeline_config = config_entity.TrainingPipelineConfig()
       data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
       print(data_ingestion_config.to_dict())
       #calling data ingestion class
       data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
       #calling data ingestion artifact
       data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
       
       # Data Validation
       data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
       data_validation = DataValidation(data_validation_config=data_validation_config,
                         data_ingestion_artifact=data_ingestion_artifact)
        
       data_validation_artifact = data_validation.initiate_data_validation()

       #Data Transformation

       # calling the data transformer config
       data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
       #calling data transformation
       data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
       data_ingestion_artifact=data_ingestion_artifact)
       #calling the data transformaion artifact
       data_transformation_artifact = data_transformation.initiate_data_transformation()

      #model trainer
       model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
       model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
       model_trainer_artifact = model_trainer.initiate_model_trainer()


      
     except Exception as e:
          print(e)