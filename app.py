from flask import Flask
import logging
import os
from src.api.routes import api, init_routes
from src.services.model_loader import load_model, load_classes
from src.services.predictor import DiseasePredictor

# Setup logging
logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)
    
    # Initialize model and predictor
    model = load_model()
    classes = load_classes()
    predictor = DiseasePredictor(model, classes)
    
    # Register routes
    init_routes(predictor)
    app.register_blueprint(api)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)