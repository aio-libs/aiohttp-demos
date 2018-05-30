import pickle


_model = None


def warm(model_path):
    global _model
    if _model is None:
        with open(model_path, 'rb') as f:
            pipeline = pickle.load(f)
        _model = pipeline
    return True


def predict(comment):
    return _model.predict(comment)


def predict_proba(comment):
    return _model.predict_proba(comment)
