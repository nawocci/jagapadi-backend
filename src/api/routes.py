from flask import Blueprint, request, jsonify
from firebase_admin import auth
from src.utils.image_processing import save_temp_image
from src.services.firebase_service import FirebaseService
import os

api = Blueprint('api', __name__)
firebase_service = FirebaseService()

def verify_token(token: str) -> str:
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception as e:
        raise ValueError(f"Invalid token: {e}")

def init_routes(predictor):
    @api.route('/predict', methods=['POST'])
    def predict():
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        if 'token' not in request.headers:
            return jsonify({'error': 'No authentication token provided'}), 401

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            # Verify user token
            user_id = verify_token(request.headers['token'])
            
            # Process prediction
            temp_path = save_temp_image(file)
            prediction = predictor.predict(temp_path)
            
            # Save to Firebase, including the image
            firebase_service.save_prediction(user_id, prediction, temp_path)
            
            return jsonify(prediction)
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if 'temp_path' in locals():
                os.remove(temp_path)

    @api.route('/history', methods=['GET'])
    def get_history():
        if 'token' not in request.headers:
            return jsonify({'error': 'No authentication token provided'}), 401
            
        try:
            user_id = verify_token(request.headers['token'])
            # Get limit from query params, None if not specified
            limit = request.args.get('limit', type=int, default=None)
            predictions = firebase_service.get_user_predictions(user_id, limit)
            return jsonify({'predictions': predictions})
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500