import firebase_admin
from firebase_admin import credentials, firestore
import logging
from datetime import datetime

from src.config import PROJECT_ID

# Initialize Firebase Admin SDK
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': PROJECT_ID
})
db = firestore.client()

class FirebaseService:
    @staticmethod
    def save_prediction(user_id: str, prediction_data: dict) -> str:
        try:
            # Add timestamp to prediction data
            prediction_data['timestamp'] = datetime.now()
            
            # Add to user's predictions collection
            doc_ref = db.collection('users').document(user_id)\
                       .collection('predictions').document()
            doc_ref.set(prediction_data)
            
            return doc_ref.id
        except Exception as e:
            logging.error(f"Error saving prediction: {e}")
            raise RuntimeError(f"Failed to save prediction: {e}")

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