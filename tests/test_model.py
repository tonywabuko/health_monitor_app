import pytest
from model import train_model
import pandas as pd

def test_model_training():
    model = train_model()
    assert model is not None, "Model failed to train"

def test_anomaly_detection():
    model = train_model()
    test_data = pd.DataFrame([[180, 85, 39.0]], columns=["heart_rate", "spO2", "temperature"])
    prediction = model.predict(test_data)
    assert prediction[0] == -1, "Failed to detect anomaly"
