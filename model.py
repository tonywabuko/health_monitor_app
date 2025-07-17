import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def train_model():
    data = {
        "heart_rate": [72, 75, 71, 69, 180, 65, 85, 77, 66, 160, 62, 110, 58, 130],
        "spO2": [98, 97, 99, 96, 90, 99, 97, 95, 98, 88, 99, 92, 100, 85],
        "temperature": [36.7, 36.8, 37.0, 36.5, 39.2, 36.9, 37.1, 36.6, 36.8, 38.5, 36.4, 37.5, 36.3, 38.0]
    }

    model = Pipeline([
        ('scaler', StandardScaler()),
        ('iso_forest', IsolationForest(contamination=0.2, random_state=42))
    ])
    
    return model.fit(pd.DataFrame(data))
