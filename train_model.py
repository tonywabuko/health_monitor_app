import pandas as pd
import numpy as np
from model import train_model

# Simulate training data
np.random.seed(42)
data = pd.DataFrame({
    "heart_rate": np.random.normal(loc=75, scale=15, size=300),
    "blood_oxygen": np.random.normal(loc=97, scale=2, size=300)
})

train_model(data)
