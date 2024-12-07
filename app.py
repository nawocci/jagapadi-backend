from flask import Flask, request, jsonify
import logging
from predictor import predict_disease

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the image is part of the request
    if 'image' not in request.files or request.files['image'].filename == '':
        logging.error("No image file uploaded")
        return jsonify({'error': 'No image uploaded or selected'}), 400

    file = request.files['image']

    try:
        response = predict_disease(file)
        return jsonify(response)
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production