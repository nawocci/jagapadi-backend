import os

# Model paths
MODEL_PATH = '/tmp/final_memory_optimized_mobilenet_model.keras'

# GCS Configuration
BUCKET_NAME = 'jagapadi-model'
MODEL_BLOB_NAME = 'final_memory_optimized_mobilenet_model.keras'

# Rice disease class names (hardcoded for new model)
RICE_DISEASE_CLASSES = [
    'bacterial_leaf_blight', 
    'bacterial_leaf_streak', 
    'bacterial_panicle_blight', 
    'blast', 
    'brown_spot', 
    'dead_heart', 
    'downy_mildew', 
    'hispa', 
    'normal', 
    'tungro'
]

# Firebase Configuration
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')

# Gemini API Configuration
GENAI_API_KEY = os.getenv("GENAI_API_KEY")