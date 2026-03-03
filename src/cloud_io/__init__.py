import pandas as pd
from pymongo import MongoClient
import os, sys
from src.constants import *
from src.exception import CustomException


class MongoIO:
    mongo_client = None
    mongo_db = None

    def __init__(self):
        if MongoIO.mongo_client is None:
            mongo_db_url = os.getenv(MONGODB_URL_KEY)
            if mongo_db_url is None:
                raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
            MongoIO.mongo_client = MongoClient(mongo_db_url)
            MongoIO.mongo_db = MongoIO.mongo_client[MONGO_DATABASE_NAME]
        self.mongo_client = MongoIO.mongo_client
        self.mongo_db = MongoIO.mongo_db

    def store_reviews(self,
                      product_name: str, reviews: pd.DataFrame):
        try:
            collection_name = product_name.replace(" ", "_")
            collection = self.mongo_db[collection_name]
            records = reviews.to_dict('records')
            if records:
                collection.insert_many(records)

        except Exception as e:
            raise CustomException(e, sys)

    def get_reviews(self,
                    product_name: str):
        try:
            collection_name = product_name.replace(" ", "_")
            collection = self.mongo_db[collection_name]
            data = list(collection.find({}, {'_id': 0}))
            return data

        except Exception as e:
            raise CustomException(e, sys)


