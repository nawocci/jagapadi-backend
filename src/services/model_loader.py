import logging
import os

import tensorflow as tf
from google.cloud import storage
from src.config import (
    BUCKET_NAME, MODEL_PATH, CLASSES_PATH,
    MODEL_BLOB_NAME, CLASSES_BLOB_NAME
)

def download_file_from_gcs(bucket_name: str, source_blob_name: str, destination_file_name: str):
    try:
        logging.info(f"Downloading {source_blob_name} from GCS")
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        logging.info(f"File downloaded successfully")
    except Exception as e:
        logging.error(f"Failed to download {source_blob_name}: {e}")
        raise RuntimeError(f"Failed to download from GCS: {e}")

def load_model() -> tf.keras.Model:
    if not os.path.exists(MODEL_PATH):
        download_file_from_gcs(BUCKET_NAME, MODEL_BLOB_NAME, MODEL_PATH)
    
    try:
        return tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")

def load_classes() -> list:
    if not os.path.exists(CLASSES_PATH):
        download_file_from_gcs(BUCKET_NAME, CLASSES_BLOB_NAME, CLASSES_PATH)
    
    try:
        with open(CLASSES_PATH, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        raise RuntimeError(f"Error loading classes: {e}")