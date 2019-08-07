import pandas as pd
import pytest
from pytest import approx

from epysurv.metrics import ghozzi_score


@pytest.fixture
def prediction_results():
    return pd.DataFrame({"outbreak": [1, 1, 0, 0], "n_outbreak_cases": [6, 10, 0, 0]})


def test_ghozzi_score_mixed(prediction_results):
    prediction_results["alarm"] = [1, 0, 0, 1]
    assert ghozzi_score(prediction_results) == approx((6 - 10 + 0 - 8) / 16)


def test_ghozzi_score_always_outbreak(prediction_results):
    prediction_results["alarm"] = [1, 1, 1, 1]
    assert ghozzi_score(prediction_results) == approx((6 + 10 - 8 - 8) / 16)


def test_ghozzi_score_never_outbreak(prediction_results):
    prediction_results["alarm"] = [0, 0, 0, 0]
    assert ghozzi_score(prediction_results) == approx(-1)


def test_ghozzi_score_correct(prediction_results):
    prediction_results["alarm"] = prediction_results["outbreak"]
    assert ghozzi_score(prediction_results) == approx(1)


def test_ghozzi_score_always_incorrect(prediction_results):
    prediction_results["alarm"] = 1 - prediction_results["outbreak"]
    assert ghozzi_score(prediction_results) == approx((-6 + -10 - 8 - 8) / 16)
