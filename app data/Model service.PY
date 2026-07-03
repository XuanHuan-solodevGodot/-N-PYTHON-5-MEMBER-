import numpy as np
import joblib


def load_model(path="random_forest.pkl"):
    """Loads the trained RandomForest model. Returns (model, error_message_or_None)."""
    try:
        return joblib.load(path), None
    except Exception as e:
        return None, str(e)


def predict_wine_class(model, values):
    """Runs a prediction for one sample. Returns (predicted_class, confidence_percent)."""
    data = np.array([values])
    prediction = model.predict(data)[0]
    probability = max(model.predict_proba(data)[0]) * 100
    return prediction, probability