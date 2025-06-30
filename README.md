# JagaPadi Backend

This project serves as the backend for the JagaPadi app. It is designed to handle various functionalities including:

- Image-based paddy disease prediction: Users can scan a rice plant's leaf and receive a prediction of the disease it has.
- Database management: Include features for storing and managing user data, paddy plant information, and prediction results.
- User authentication: The backend will support user registration, login, and authentication to ensure secure access to the app's features.
    
## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/nawocci/jagapadi-backend.git
    cd jagapadi-backend
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

- **Description**: Predicts the disease from an uploaded paddy plant image.
- **Request**: Multipart form-data with an image file.
- **Response**: JSON object with the disease, details, confidence score, date, and image URL.

    ```json
    {
        "disease": "Bacterial leaf blight",
        "details": "Bacterial leaf blight is a common disease in rice plants caused by Xanthomonas oryzae. Symptoms include water-soaked lesions on leaves that turn yellow and then brown. The disease spreads rapidly in warm, humid conditions and can significantly reduce yield if not managed properly.",
        "confidence_score": 98.76,
        "date": "2024-03-20 15:30:45",
        "image_url": "https://storage.googleapis.com/jagapadi-image/users/user_id/predictions/image.jpg"
    }
    ```

### GET /history

- **Description**: Retrieves user's prediction history
- **Headers**: 
  - `token`: Firebase authentication token
- **Query Parameters**:
  - `limit` (optional): Number of entries to return. If not specified, returns all entries.
- **Response**: JSON array of entries ordered by date (newest first)

    ```json
    {
        "predictions": [
            {
                "id": "prediction_id",
                "disease": "Brown spot",
                "details": "Brown spot is a fungal disease affecting rice plants...",
                "confidence_score": 98.76,
                "date": "2024-03-20 15:30:45",
                "timestamp": "2024-03-20T15:30:45.123Z",
                "image_url": "https://storage.googleapis.com/jagapadi-image/users/user_id/predictions/image.jpg"
            }
        ]
    }
    ```

## License

This project is licensed under the MIT License.