import logging
import google.generativeai as genai
from src.config import GENAI_API_KEY
from src.utils.image_processing import preprocess_image
import numpy as np
from datetime import datetime

# Configure Gemini
genai.configure(api_key=GENAI_API_KEY)
model_genai = genai.GenerativeModel("gemini-1.5-flash")

class DiseasePredictor:
    def __init__(self, model, classes):
        self.model = model
        self.classes = classes

    def predict(self, img_path: str) -> dict:
        try:
            img_array = preprocess_image(img_path)
            predictions = self.model.predict(img_array)
            prediction_index = np.argmax(predictions[0])
            predicted_class = self.classes[prediction_index]
            confidence_score = float(np.max(predictions[0]) * 100)
            
            plant, condition = self._format_prediction(predicted_class)
            details = self._get_description(plant, condition)
            
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                'disease': condition,
                'confidence_score': confidence_score,
                'details': details,
                'date': current_date,
                'image_url': img_path
            }
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            raise RuntimeError(f"Prediction error: {e}")

    def _format_prediction(self, predicted_class: str) -> tuple:
        try:
            plant, condition = predicted_class.split('___')
            return (
                plant.replace('_', ' '),
                condition.replace('_', ' ').title()
            )
        except ValueError:
            return predicted_class, "Unknown Condition"

    def _get_description(self, plant: str, disease: str) -> str:
        if 'healthy' in disease.lower():
            prompt = f"Write a short one paragraph guide on how to maintain the health of {plant} plants. Include basic care tips like watering, sunlight, and soil requirements."
        else:
            prompt = f"Write a short one paragraph explanation of {disease} disease on {plant}."
        
        response = model_genai.generate_content(prompt)
        return response.text