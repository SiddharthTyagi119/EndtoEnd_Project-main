#creating a class that will create a folder after running the model on a new data and will save the new model in that folder.
#folder to save new model and we have to call all the classes of all the files
#comparison new model vs old model
#accept or reject



import os
from Insurance.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME,MODEL_FILE_NAME,TARGET_ENCODER_OBJECT_FILE_NAME
from glob import glob
from typing import Optional
import os

# Now lets start model validation


class ModelResolver:
    
    def __init__(self,model_registry:str = "saved_models",        #folder to save the new model
                transformer_dir_name="transformer",               #to store transformed data file
                target_encoder_dir_name = "target_encoder",       #to store encoded data
                model_dir_name = "model"):

        self.model_registry=model_registry

        #creating a dir to save the new model
        os.makedirs(self.model_registry,exist_ok=True)
        
        #dir to store the transformed data files
        self.transformer_dir_name = transformer_dir_name
        
        #dir to store encoded data
        self.target_encoder_dir_name=target_encoder_dir_name
        
        #define model 
        self.model_dir_name=model_dir_name
# 1
#just creating a new directory to save the new model
#saved model>>>dir 0 with pickle file then 1,2 and so on...
#the nummber  dir inc if we keep traing the model on new data 
    def get_latest_dir_path(self)->Optional[str]:
        try:
            #defining model registry dir 
            dir_names = os.listdir(self.model_registry)
            if len(dir_names)==0:
                return None
            
            #creating the dir with count 1 as if we run the data 1st on new data and so on
            #folders are creating in int inside saved model dir 
            dir_names = list(map(int,dir_names))
            
            #latest dir will be the one who run at last time
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")

            #create a saved model folder
        except Exception as e:
            raise e

# 2  
#to get latest model
    def get_latest_model_path(self):
        try:
            #latest dir path
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Model is not available")
                
                #latest model path will be this
                #saved model>>0>>model.pkl
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e
# 3
    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transformer is not available")
                
                #latest dir with transformed data path
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e
# 4
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Target encoder is not available")
                
                #latest dir with transformed encoded data path
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e

# 5 saving the latest directory
    def get_latest_save_dir_path(self)->str:
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir==None:
                
                #creating folder if not present and joining saved folder with the model dir {0}
                return os.path.join(self.model_registry,f"{0}")
                #checking latest dir
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry,f"{latest_dir_num+1}")
        except Exception as e:
            raise e

# 6 saving model
    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)   #model.pkl
        except Exception as e:
            raise e

# 7 saving transformer file (saving transformed data file)
    def get_latest_save_transformer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)  #transformer.pkl
        except Exception as e:
            raise e

# 8 saving encoder file
    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)  #encoder.pkl
        except Exception as e:
            raise e


    