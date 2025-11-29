import io
from typing import Tuple

import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions,
)

# Load once
_model = MobileNetV2(weights="imagenet")


def _preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    x = np.array(img, dtype=np.float32)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def predict_food(image_bytes: bytes) -> Tuple[str, float]:
    x = _preprocess_image(image_bytes)
    preds = _model.predict(x)
    decoded = decode_predictions(preds, top=1)[0][0]
    label = decoded[1]
    confidence = float(decoded[2])
    return label, confidence
