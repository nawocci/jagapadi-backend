# app.py
from flask import Flask, request, jsonify
from model import classify_image, load_model, load_classes
from llm import get_disease_description
import tempfile
import os
import logging

app = Flask(__name__)

# Load the model and classes
model = load_model('/tmp/plant_disease_model.h5')
classes = load_classes('/tmp/classes.txt')

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the image is part of the request
    if 'image' not in request.files or request.files['image'].filename == '':
        logging.error("No image file uploaded")
        return jsonify({'error': 'No image uploaded or selected'}), 400

    file = request.files['image']

    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)

    try:
        logging.info(f"Received image {file.filename} for prediction.")
        predicted_class, confidence_score = classify_image(temp_file.name, model, classes)

        # Format the predicted class
        try:
            plant, disease = predicted_class.split('___')
            plant = plant.replace('_', ' ')
            disease = disease.replace('_', ' ').title()
        except ValueError:
            logging.error(f"Error splitting predicted class '{predicted_class}' into plant and disease.")
            plant, disease = predicted_class, "Unknown Disease"

        # Get the disease description
        description = get_disease_description(plant, disease)

        response = {
            'plant': plant,
            'disease': disease,
            'confidence_score': float(confidence_score),
            'description': description
        }
        logging.info(f"Prediction result: {response}")
        return jsonify(response)
    except RuntimeError as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({'error': f"Prediction error: {e}"}), 500
    finally:
        os.remove(temp_file.name)  # Clean up the temporary file

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production