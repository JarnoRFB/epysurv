import numpy as np
import pandas as pd
import pytest

from epysurv.models.timeseries import (  # type: ignore
    Farrington,
    FarringtonFlexible,
    GLRPoisson,
)

from .utils import load_predictions


def test_farrington_timeseries_prediciton(tsc_generator, shared_datadir):
    model = Farrington(alpha=0.1)
    model.fit(tsc_generator.train_gen)
    pred = model.predict(tsc_generator.test_gen)
    saved_predictions = load_predictions(
        shared_datadir / "farrington_timeseries_predictions.csv",
    )

    pd.testing.assert_series_equal(pred.alarm, saved_predictions.alarm)


def test_farrington_timeseries_prediction_columns(tsc_generator, shared_datadir):
    model = Farrington()
    model.fit(tsc_generator.train_gen)
    pred = model.predict(tsc_generator.test_gen)

    # check for columns
    pred_columns = list(pred.columns.values)

    # this one is always here
    assert "alarm" in pred_columns
    # but this one should be here if we call predict() with get_alarm_only = False
    assert "upperbound" in pred_columns


def test_farrington_flexible_timeseries_prediction_columns(
    tsc_generator, shared_datadir
):
    model = FarringtonFlexible()
    model.fit(tsc_generator.train_gen)
    pred = model.predict(tsc_generator.test_gen)

    # check for columns
    pred_columns = list(pred.columns.values)

    # this one is always here
    assert "alarm" in pred_columns
    # but this one should be here if we call predict() with get_alarm_only = False
    assert "upperbound" in pred_columns


def test_outbreak_case_subtraction():
    def test_gen():
        df = pd.DataFrame(
            {"n_cases": np.ones(100) * 5, "n_outbreak_cases": np.ones(100) * 3},
            index=pd.date_range("2020", freq="W-MON", periods=100),
        )
        yield df, True

    model = Farrington()
    _ = model.predict(test_gen())
    assert np.alltrue(model._training_data.n_cases.values == 2)
