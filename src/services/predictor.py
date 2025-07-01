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
            predictions = self.model.predict(img_array, verbose=0)
            prediction_index = np.argmax(predictions[0])
            predicted_class = self.classes[prediction_index]
            confidence_score = float(np.max(predictions[0]) * 100)
            
            # Format the disease name for display
            formatted_disease = self._format_disease_name(predicted_class)
            details = self._get_description(formatted_disease)
            
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                'disease': formatted_disease,
                'confidence_score': confidence_score,
                'details': details,
                'date': current_date,
                'image_url': img_path
            }
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            raise RuntimeError(f"Prediction error: {e}")

    def _format_disease_name(self, predicted_class: str) -> str:
        """Format disease name for display"""
        if predicted_class == 'normal':
            return 'Healthy Rice Plant'
        else:
            # Replace underscores with spaces and title case
            return predicted_class.replace('_', ' ').title()

    def _get_description(self, disease: str) -> str:
        if 'healthy' in disease.lower() or disease.lower() == 'normal':
            prompt = f"Tulis panduan singkat satu paragraf tentang cara merawat kesehatan tanaman padi. Sertakan tips perawatan dasar seperti penyiraman, sinar matahari, dan kebutuhan tanah. Jawab dalam bahasa Indonesia."
        else:
            prompt = f"Tulis penjelasan singkat satu paragraf tentang penyakit {disease} pada tanaman padi. Jawab dalam bahasa Indonesia."
        
        response = model_genai.generate_content(prompt)
        return response.text