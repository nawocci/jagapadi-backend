import tensorflow as tf
import numpy as np
import tempfile

def preprocess_image(img_path: str) -> np.ndarray:
    try:
        # Load image with target size 224x224 for the new model
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        # Normalize pixel values to [0, 1] range
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        return img_array
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {e}")

def save_temp_image(file) -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    return temp_file.name