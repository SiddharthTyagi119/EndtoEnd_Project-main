from Insurance.entity import artifact_entity,config_entity
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from scipy.stats import ks_2samp
from typing import Optional
import os,sys 
import pandas as pd
from Insurance import utils
import numpy as np
from Insurance.config import TARGET_COLUMN

#defining the constructor  
class DataValidation:


    def __init__(self,
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"####    data validation    ####")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise InsuranceException(e, sys)
        
    
#to drop the column with missing values
#taking data as df 
    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
      
        try:
            
            #taking threshold
            threshold = self.data_validation_config.missing_threshold
            
            #checking null values
            null_report = df.isna().sum()/df.shape[0]

            #selecting column name which contains null above threshold
            logging.info(f"selecting column name which contains null above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index

            #creating report key name
            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.validation_error[report_key_name]=list(drop_column_names)

            #drop columns names
            df.drop(list(drop_column_names),axis=1,inplace=True)

            #if null values not present in the columns
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise InsuranceException(e, sys)


#checking if the columns are equal in both main file data and train,test
#original data is our base column and base data
#base df- main csv file and current df- data that generated in data ingestion
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
           
            base_columns = base_df.columns
            #created column
            current_columns = current_df.columns

            #checking the base columns are present in our current columns or not
            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column: [{base} is not available.]")
                    #appending the missing columns in the list
                    missing_columns.append(base_column)
            
            #checking the length of missing columns
            if len(missing_columns)>0:
                #it generate a file >> report.yaml to have valdation data report
                self.validation_error[report_key_name]=missing_columns
                return False
            return True
        except Exception as e:
            raise InsuranceException(e, sys)


#
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report=dict()

            base_columns = base_df.columns 
            current_columns = current_df.columns

            
            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]
                
                #checking the hypothesis
                same_distribution =ks_2samp(base_data,current_data)

                #if the distribution p value is greater than 0.05  then null hypothesis would true
                if same_distribution.pvalue>0.05:
                    #We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
                    
                    #different distribution
            
            #it helps to store the report in yaml file
            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise InsuranceException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            #working on base dataframe
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            
            #finding the null values
            base_df.replace({"na":np.NAN},inplace=True)
            logging.info(f"Replace na value in base df")

            #droping null values columns from base df 
            logging.info(f"Drop null values columns from base df")
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_values_within_base_dataset")

            #reading train df
            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            
            #reading test df
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
 
            #drop missing values columns
            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="missing_values_within_train_dataset")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="missing_values_within_test_dataset")
            
            exclude_columns = [TARGET_COLUMN]

            #converting the data type of the data
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)


            #checking all req columns in train and test
            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            #checking data drift
            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")
          
            #write the report
            logging.info("Write report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            #data validation artifact
            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)