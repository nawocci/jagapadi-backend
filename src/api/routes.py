from flask import Blueprint, request, jsonify
from src.utils.image_processing import save_temp_image
import os

api = Blueprint('api', __name__)

def init_routes(predictor):
    @api.route('/predict', methods=['POST'])
    def predict():
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            temp_path = save_temp_image(file)
            response = predictor.predict(temp_path)
            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if temp_path:
                os.remove(temp_path)