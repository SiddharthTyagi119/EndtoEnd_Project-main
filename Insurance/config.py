###setting our environment 
import pymongo
import pandas as pd
import numpy as np
import json
import os, sys
from dataclasses import dataclass


@dataclass
#creating a class for our environment variable and definig mongodb url which is loading from .env file
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")


env_var = EnvironmentVariable()
#defining mongo db client
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "expenses"
print(env_var.mongo_db_url)