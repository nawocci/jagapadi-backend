import os

# Model paths
MODEL_PATH = '/tmp/plant_disease_model.h5'
CLASSES_PATH = '/tmp/classes.txt'

# GCS Configuration
BUCKET_NAME = 'plantanist-model'
MODEL_BLOB_NAME = 'plant_disease_model.h5'
CLASSES_BLOB_NAME = 'classes.txt'

# Gemini API Configuration
GENAI_API_KEY = os.getenv("GENAI_API_KEY")