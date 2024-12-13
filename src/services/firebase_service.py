import firebase_admin
from firebase_admin import credentials, firestore
import logging
from datetime import datetime
import os
from google.cloud import storage

from src.config import PROJECT_ID

# Initialize Firebase Admin SDK
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': PROJECT_ID
})
db = firestore.client()

class FirebaseService:
    @staticmethod
    def save_prediction(user_id: str, prediction_data: dict, image_path: str) -> str:
        try:
            # Add timestamp to prediction data
            prediction_data['timestamp'] = datetime.now()

            # Upload image to Cloud Storage
            image_url = FirebaseService.upload_image_to_gcs(user_id, image_path)
            prediction_data['image_url'] = image_url

            # Add to user's predictions collection
            doc_ref = db.collection('users').document(user_id)\
                       .collection('predictions').document()
            doc_ref.set(prediction_data)

            return doc_ref.id
        except Exception as e:
            logging.error(f"Error saving prediction: {e}")
            raise RuntimeError(f"Failed to save prediction: {e}")

    @staticmethod
    def upload_image_to_gcs(user_id: str, image_path: str) -> str:
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket('plantanist-image')  # Updated bucket name
            blob = bucket.blob(f'users/{user_id}/predictions/{os.path.basename(image_path)}')
            blob.upload_from_filename(image_path)
            return blob.public_url  # Return the public URL of the uploaded image
        except Exception as e:
            logging.error(f"Error uploading image to GCS: {e}")
            raise RuntimeError(f"Failed to upload image: {e}")

    @staticmethod
    def get_user_predictions(user_id: str, limit: int = None) -> list:
        try:
            query = db.collection('users').document(user_id)\
                     .collection('predictions')\
                     .order_by('timestamp', direction=firestore.Query.DESCENDING)

            # Apply limit only if specified
            if limit:
                query = query.limit(limit)

            predictions = []
            docs = query.stream()

            for doc in docs:
                prediction = doc.to_dict()
                prediction['id'] = doc.id
                predictions.append(prediction)

            return predictions
        except Exception as e:
            logging.error(f"Error fetching predictions: {e}")
            raise RuntimeError(f"Failed to fetch predictions: {e}")