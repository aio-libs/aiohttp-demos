import pickle
from collections import namedtuple

import numpy as np

_model = None

Scores = namedtuple("Scores", ["toxic", "severe_toxic",
                               "obscence", "insult", "identity_hate"])


def warm(model_path):
    global _model
    if _model is None:
        with model_path.open('rb') as fp:
            pipeline = pickle.load(fp)
            _model = pipeline
    return True


def predict(message):
    results = _model.predict_proba([message])
    results = np.array(results).T[1].tolist()[0]
    return Scores(*results)
