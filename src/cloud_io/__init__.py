import pandas as pd
from pymongo import MongoClient
from pymongo.database import Database
import sys
import re
from src.exception import CustomException


class MongoIO:
    mongo_client: MongoClient | None = None
    mongo_db: Database | None = None

    def __init__(self):
        # Using class-level caching to prevent re-initializing connections on every Streamlit rerun
        if MongoIO.mongo_client is None:
            # Your working connection string pointed directly to your new database
            mongo_url = "mongodb+srv://somnath:Somnath2003@customercategorization.vbknzhm.mongodb.net/myntra_reviews?retryWrites=true&w=majority"
            
            try:
                client = MongoClient(
                    mongo_url,
                    serverSelectionTimeoutMS=10000,    # 5-second connection limit
                    connectTimeoutMS=10000,            # 5-second socket timeout
                    tlsAllowInvalidCertificates=True # Bypasses potential local OpenSSL/TLS verification blocks
                )
                
                # Verify network connectivity instantly via a quick ping command
                client.admin.command("ping")
                
                MongoIO.mongo_client = client
                MongoIO.mongo_db = MongoIO.mongo_client["myntra_reviews"]
                
            except Exception as e:
                raise Exception(f"Failed to establish direct connection to MongoDB Atlas. Error: {str(e)[:300]}")

        self.mongo_client = MongoIO.mongo_client
        self.mongo_db = MongoIO.mongo_db

    def store_reviews(self, product_name: str, reviews: pd.DataFrame):
        try:
            if self.mongo_db is None:
                raise Exception("MongoDB is uninitialized or unreachable.")

            # Sanitize product name to create a safe collection title
            collection_name = product_name.replace(" ", "_")
            collection = self.mongo_db[collection_name]
            
            # Convert DataFrame records cleanly to dictionary rows
            records = reviews.to_dict('records')
            
            if records:
                collection.insert_many(records)

        except Exception as e:
            raise CustomException(e, sys)

    def get_reviews(self, product_name: str):
        try:
            if self.mongo_db is None:
                return []

            def normalize_key(value: str) -> str:
                value = (value or "").strip().lower()
                value = value.replace("_", " ")
                value = re.sub(r"\s+", " ", value)
                return value

            requested_raw = product_name or ""
            requested_norm = normalize_key(requested_raw)

            # Strategy 1: Check standard string variations directly
            candidates: list[str] = []
            collapse_spaces = re.sub(r"\s+", " ", requested_raw.strip())
            candidates.append(requested_raw.replace(" ", "_"))
            candidates.append(requested_raw.strip().replace(" ", "_"))
            candidates.append(collapse_spaces.replace(" ", "_"))
            candidates.append(collapse_spaces.lower().replace(" ", "_"))

            seen: set[str] = set()
            for name in candidates:
                if not name or name in seen:
                    continue
                seen.add(name)
                collection = self.mongo_db[name]
                data = list(collection.find({}, {"_id": 0}))
                if data:
                    return data

            # Strategy 2: Dynamic matching fallback by reading collection schemas
            try:
                existing_names = self.mongo_db.list_collection_names()
            except Exception:
                existing_names = []

            if existing_names:
                norm_to_actual: dict[str, str] = {}
                for existing in existing_names:
                    norm_to_actual[normalize_key(existing)] = existing

                matched = norm_to_actual.get(requested_norm)
                if matched:
                    collection = self.mongo_db[matched]
                    return list(collection.find({}, {"_id": 0}))

            return []

        except Exception as e:
            raise CustomException(e, sys)