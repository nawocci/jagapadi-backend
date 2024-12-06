# Plantanist Backend

This project serves as the backend for the Plantanist app. It is designed to handle various functionalities including:

- Image-based disease prediction: Users can scan a plant's leaf and receive a prediction of the disease it has.
- Database management: Include features for storing and managing user data, plant information, and prediction results.
- User authentication: The backend will support user registration, login, and authentication to ensure secure access to the app's features.
    
## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/nawocci/plantanist-backend.git
    cd plantanist-backend
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Start the Flask server:
    ```
    python app.py
    ```

## API Endpoints

### POST /predict

- **Description**: Predicts the disease from an uploaded image.
- **Request**: Multipart form-data with an image file.
- **Response**: JSON object with the predicted class and confidence score.

    ```json
    {
        "predicted_class": "Tomato___Bacterial_spot",
        "confidence_score": 98.76
    }
    ```

## License

This project is licensed under the MIT License.