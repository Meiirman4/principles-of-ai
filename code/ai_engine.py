import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

_model = None

def load_model():
    global _model
    if _model is None:
        print(" [AI] Loading MobileNetV2 Model...")
        _model = MobileNetV2(weights='imagenet')

def predict_image(image_bytes):
    global _model
    if _model is None: load_model()
    
    try:
        # Process Image
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = img.resize((224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Predict
        preds = _model.predict(x)
        decoded = decode_predictions(preds, top=1)[0]
        # Return label (e.g., 'pizza') and confidence (e.g., 0.98)
        return decoded[0][1], float(decoded[0][2])
    except Exception as e:
        print(f" [AI Error] {e}")
        return None, 0