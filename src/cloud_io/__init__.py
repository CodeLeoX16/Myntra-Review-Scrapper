import pandas as pd
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
import os, sys
import re
from src.constants import MONGODB_FALLBACK_URL_KEY, MONGODB_URL_KEY, MONGO_DATABASE_NAME
from src.exception import CustomException


class MongoIO:
    mongo_client: MongoClient | None = None
    mongo_db: Database | None = None

    def __init__(self):
        if MongoIO.mongo_client is None:
            def _get_setting(key: str) -> str | None:
                value = os.getenv(key)
                if value:
                    return value

                # Helpful for local runs: load variables from a .env file if present.
                try:
                    from dotenv import load_dotenv

                    load_dotenv()
                    value = os.getenv(key)
                    if value:
                        return value
                except Exception:
                    pass

                # Helpful for Streamlit Cloud: prefer st.secrets if available.
                try:
                    import streamlit as st

                    value = st.secrets.get(key)
                    if value:
                        return value
                except Exception:
                    pass

                return None

            primary_url = _get_setting(MONGODB_URL_KEY)
            fallback_url = _get_setting(MONGODB_FALLBACK_URL_KEY)
            if primary_url is None and fallback_url is None:
                raise Exception(
                    f"Environment key: {MONGODB_URL_KEY} is not set. "
                    f"Optionally set {MONGODB_FALLBACK_URL_KEY} to a standard mongodb:// URI."
                )

            def _connect(url: str):
                # Fail fast so we can retry with fallback if SRV DNS is flaky.
                client = MongoClient(url, serverSelectionTimeoutMS=8000, connectTimeoutMS=8000)
                client.admin.command("ping")
                return client

            last_error: Exception | None = None
            client = None
            for candidate in [primary_url, fallback_url]:
                if not candidate:
                    continue
                try:
                    client = _connect(candidate)
                    last_error = None
                    break
                except (ConfigurationError, ServerSelectionTimeoutError) as e:
                    last_error = e
                except Exception as e:
                    last_error = e

            if client is None:
                raise Exception(f"Could not connect to MongoDB. Last error: {str(last_error)[:300]}")

            MongoIO.mongo_client = client
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
            if self.mongo_db is None:
                return []

            def normalize_key(value: str) -> str:
                value = (value or "").strip().lower()
                value = value.replace("_", " ")
                value = re.sub(r"\s+", " ", value)
                return value

            requested_raw = product_name or ""
            requested_norm = normalize_key(requested_raw)

            # Fast path: try a few common collection-name variants.
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

            # If the direct attempts return nothing, try to match an existing collection by normalization.
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


