import tensorflow as tf
import numpy as np
from google.cloud import storage
from typing import List, Tuple
import os
import logging

# Paths
MODEL_PATH = '/tmp/plant_disease_model.h5'
CLASSES_PATH = '/tmp/classes.txt'
BUCKET_NAME = 'plantanist-model'
MODEL_BLOB_NAME = 'plant_disease_model.h5'
CLASSES_BLOB_NAME = 'classes.txt'

# Set up logging
logging.basicConfig(level=logging.INFO)

def download_file_from_gcs(bucket_name: str, source_blob_name: str, destination_file_name: str):
    try:
        logging.info(f"Downloading {source_blob_name} from GCS to {destination_file_name}")
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        logging.info(f"File {source_blob_name} downloaded successfully.")
    except Exception as e:
        logging.error(f"Failed to download {source_blob_name}: {e}")
        raise RuntimeError(f"Failed to download {source_blob_name} from GCS: {e}")

def load_model(model_path: str) -> tf.keras.Model:
    try:
        logging.info(f"Loading model from {model_path}")
        return tf.keras.models.load_model(model_path)
    except Exception as e:
        logging.error(f"Error loading model from {model_path}: {e}")
        raise RuntimeError(f"Error loading model from {model_path}: {e}")

def load_classes(file_path: str) -> List[str]:
    try:
        logging.info(f"Loading classes from {file_path}")
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        logging.error(f"Class file not found at {file_path}.")
        raise RuntimeError(f"Class file not found at {file_path}. Please provide a valid classes.txt file.")
    except Exception as e:
        logging.error(f"Error reading class file {file_path}: {e}")
        raise RuntimeError(f"Error reading class file {file_path}: {e}")

def preprocess_image(img_path: str) -> np.ndarray:
    try:
        logging.info(f"Preprocessing image {img_path}")
        img = tf.keras.utils.load_img(img_path, target_size=(256, 256))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        logging.error(f"Error preprocessing image {img_path}: {e}")
        raise ValueError(f"Error preprocessing image {img_path}: {e}")

def classify_image(img_path: str, model: tf.keras.Model, classes: List[str]) -> Tuple[str, float]:
    try:
        img_array = preprocess_image(img_path)
        predictions = model.predict(img_array)
        prediction_index = np.argmax(predictions[0])
        predicted_class = classes[prediction_index]
        confidence_score = np.max(predictions[0]) * 100
        logging.info(f"Predicted class: {predicted_class} with confidence: {confidence_score}%")
        return predicted_class, confidence_score
    except Exception as e:
        logging.error(f"Error during classification: {e}")
        raise RuntimeError(f"Error during classification: {e}")

def download_model_and_classes():
    if not os.path.exists(MODEL_PATH):
        logging.info(f"Model file not found locally, downloading from GCS.")
        download_file_from_gcs(BUCKET_NAME, MODEL_BLOB_NAME, MODEL_PATH)
    else:
        logging.info(f"Model file found locally at {MODEL_PATH}.")

    if not os.path.exists(CLASSES_PATH):
        logging.info(f"Classes file not found locally, downloading from GCS.")
        download_file_from_gcs(BUCKET_NAME, CLASSES_BLOB_NAME, CLASSES_PATH)
    else:
        logging.info(f"Classes file found locally at {CLASSES_PATH}.")

# Ensure files are downloaded before running the app
download_model_and_classes()
