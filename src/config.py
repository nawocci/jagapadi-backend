import os

# Model paths
MODEL_PATH = '/tmp/plant_disease_model.h5'
CLASSES_PATH = '/tmp/classes.txt'

# GCS Configuration
BUCKET_NAME = 'jagapadi-model'
MODEL_BLOB_NAME = 'plant_disease_model.h5'
CLASSES_BLOB_NAME = 'classes.txt'

# Firebase Configuration
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')

# Gemini API Configuration
GENAI_API_KEY = os.getenv("GENAI_API_KEY")