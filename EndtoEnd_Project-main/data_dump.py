#to import the data in mongo db
import pymongo # pip install pymongo
import pandas as pd
import json
import ssl
import certifi




#client = pymongo.MongoClient("mongodb+srv://siddharth:siddharth12@cluster0.aip3cis.mongodb.net/?retryWrites=true&w=majority")
#db = client.test


client = pymongo.MongoClient("mongodb+srv://siddharth:siddharth12@cluster0.aip3cis.mongodb.net/?retryWrites=true&w=majority")
db = client.test


DATA_FILE_PATH = (r"E:\Data science\Project-01\EndtoEnd_Project\insurance.csv")

DATABASE_NAME = "INSURANCE"
COLLECTION_NAME = "INSURANCE_PROJECT1"


if __name__=="__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    df.reset_index(drop = True, inplace = True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)