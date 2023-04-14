#we already have one model trained now if we run the model next time on data then a new model will saved
#in new dir. we will evaluate the new model with the old model.we will comare the accuracy of both the model
#if the accuracy of new model is inc compare to last one then it will saved and will deloy that model else we will go with
#the base model.
#the new model will not saved if the new model acc is ower than the old model.
from Insurance.predictor import ModelResolver
from Insurance.entity import config_entity,artifact_entity
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.utils import load_object
from sklearn.metrics import r2_score
import pandas  as pd
import sys,os
from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.config import TARGET_COLUMN

class ModelEvaluation:
#defining the things related to current model
    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        #because to train new model on the below things
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact      
        ):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact

            #defining model resolver class
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise InsuranceException(e,sys)



    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            

            logging.info("if saved model folder has model then we will compare "
            "which model is best trained one or the model from saved model folder")

            #calling latest directory 
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            
            #checking accuracy -high or low
            #our latest dir(saved model) will not have new model inside 0th dir if the new  model 
            #accuracy is low than the previous model
            #if folder is not creating then it means new model accuracy is not higher
            if latest_dir_path==None:
                #if none then old model will continue, new model accuracy is low hence accuracy is none
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact


            #Finding location of previous  model (transformer model and target encoder)
            logging.info("Finding location of transformer model and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            #loadng the model related things via load objects
            logging.info("Previous trained objects of transformer, model and target encoder")
            #Previous trained  objects
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path)
            

            #our current model will save in the below format 
            logging.info("Currently trained model objects")
            #Currently trained model objects
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model  = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)
            

            # take test data for testing test data 
            #loading test data
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            #defining target data as y true
            y_true = target_df
            # target_encoder.transform(target_df)
            # accuracy using previous trained model
            

            #in our test data we save some object dtatype , so we need to transform them 
            """We need to create label encoder object for each categorical variable. We will check later"""
            #loading the transformed data (old model)
            input_feature_name = list(transformer.feature_names_in_)
            for i in input_feature_name:       
                if test_df[i].dtypes =='object':
                    test_df[i] =target_encoder.fit_transform(test_df[i])  

            #transforming the input features
            input_arr =transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)

            ######comparison between new model and old model
            

            #checking the score of old model
            print(f"Prediction using previous model: {y_pred[:5]}")
            previous_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")
           
            # accuracy using current trained model
            #for current model
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr =current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true = target_df
            # current_target_encoder.transform(target_df)
            # current_target_encoder.inverse_transform(y_pred[:5])

            #checking the score of new model
            print(f"Prediction using trained model: {y_pred[:5]}")
            current_model_score = r2_score(y_true=y_true, y_pred=y_pred)

           
           
            ########    final comparison between both models
            
            logging.info(f"Accuracy using current trained model: {current_model_score}")
            if current_model_score<=previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact
        except Exception as e:
            raise InsuranceException(e,sys)