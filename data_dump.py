#to import the data in mongo db
import pymongo # pip install pymongo
import pandas as pd
import json
#import ssl
#import certifi

#adding the mongo client for connectivity 
client = pymongo.MongoClient("mongodb+srv://siddharth:Corona#12#@cluster0.quvfzni.mongodb.net/?retryWrites=true&w=majority")
db = client.test

#data path
DATA_FILE_PATH = (r"E:\Data science\Project\EndtoEnd_Project-main\insurance.csv")

DATABASE_NAME = "INSURANCE"
COLLECTION_NAME = "INSURANCE_PROJECT"


if __name__=="__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    df.reset_index(drop = True, inplace = True)
    
    #transpose the data
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    
    #insert the data into database
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)