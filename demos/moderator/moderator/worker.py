import pickle
import numpy as np

_model = None


def warm(model_path):
    global _model
    if _model is None:
        with open(model_path, 'rb') as f:
            pipeline = pickle.load(f)
        _model = pipeline
    return True


def predict_probability(comments):
    results = _model.predict_proba(np.array(comments))
    return np.array(results).T[1].tolist()
