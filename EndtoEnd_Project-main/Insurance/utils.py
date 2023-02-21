#To get the data from database so to read them in local
import numpy as np
import pandas as pd
import os
import sys
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client
from Insurance.logger import logging

def get_collection_as_dataframe(database_name:str,collection_name:str):
    try:
        logging.info(f"Reading data from database:{database_name} and collection:{collection_name}")
        df=pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f"find column:{df.columns}")
        if "_id" in df.columns:
            logging.info(f"dropping the columns: _id")
            df=df.drop("_id",axis=1)
        logging.info(f"rows and columds in df:{df.shape}")
        return df
    except Exception as e:
        raise InsuranceException(e,sys)