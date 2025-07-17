import pandas as pd
import numpy as np


def simulate_data(n=10):
    np.random.seed(42)
    return pd.DataFrame({
        "heart_rate": np.random.normal(75, 10, n),
        "blood_oxygen": np.random.normal(97, 2, n)
    })
