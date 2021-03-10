import pytest
import pandas as pd
import numpy as np

from house_prices.train import eval_metrics

def test_dummy_eval_metrics():
    actual = pd.Series(np.array([100, 200, 300, 400, 500]))
    predicted = pd.Series(np.array([100, 200, 350, 400, 400]))
    (rmse, mae, r2) = eval_metrics(actual, predicted)
    assert rmse == 50.0
    assert mae == 30.0
    assert r2 == 0.875