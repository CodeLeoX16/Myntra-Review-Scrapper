from src.cloud_io import MongoIO
from src.exception import CustomException
import sys


def fetch_product_names_from_cloud() -> list[str]:
    try:
        mongo = MongoIO()
        if mongo.mongo_db is None:
            return []
        collection_names = mongo.mongo_db.list_collection_names()
        return [collection_name.replace('_', ' ') for collection_name in collection_names]

    except Exception as e:
        raise CustomException(e, sys)
