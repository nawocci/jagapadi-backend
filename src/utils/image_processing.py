import tensorflow as tf
import numpy as np
import tempfile

def preprocess_image(img_path: str) -> np.ndarray:
    try:
        img = tf.keras.utils.load_img(img_path, target_size=(256, 256))
        img_array = tf.keras.utils.img_to_array(img)
        return np.expand_dims(img_array, axis=0)
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {e}")

def save_temp_image(file) -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    return temp_file.name