import io
import json
import signal
import numpy as np
from typing import Tuple, Dict, Any, Optional

from keras.models import load_model
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from PIL import Image


_model = None


def warm(model_path: str) -> None:
    # should be executed only in child processes
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    global _model
    if _model is None:
        _model = load_model(model_path)


def clean() -> None:
    # should be executed only in child processes
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    global _model
    _model = None


def prepare_image(image: Image, target: Tuple[int, int]) -> Image:
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    return image


def predict(raw_data: bytes, model: Optional[Any]=None) -> bytes:
    if model is None:
        model = _model

    if model is None:
        raise RuntimeError('Model should be loaded first')

    image = Image.open(io.BytesIO(raw_data))
    data: Dict[str, Any] = {}
    image = prepare_image(image, target=(224, 224))

    preds = model.predict(image)
    results = imagenet_utils.decode_predictions(preds)

    # loop over the results and add them to the list of
    # returned predictions
    data['predictions'] = [{'label': label, 'probability': float(prob)}
                           for _, label, prob in results[0]]

    data['success'] = True
    return json.dumps(data).encode('utf-8')
