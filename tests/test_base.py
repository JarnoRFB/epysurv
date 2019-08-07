import numpy as np
import pandas as pd
import pytest

from epysurv.models.timepoint import _base


def random_cases_for_dates(dates):
    return {
        "n_cases": np.random.randint(low=5, high=10, size=len(dates)),
        "n_outbreak_cases": np.random.randint(low=0, high=5, size=len(dates)),
    }


def test_data_in_the_future():
    model = _base.TimepointSurveillanceAlgorithm()
    dates = pd.date_range(start="2011", end="2011-12-31", freq="W-Mon")
    future_dates = pd.date_range(start="2012-01-01", end="2013")
    train_data = pd.DataFrame(random_cases_for_dates(dates), index=dates)
    test_data = pd.DataFrame(random_cases_for_dates(future_dates), index=future_dates)
    model.fit(train_data)
    model.predict(test_data)


def test_data_in_the_future_should_raise():
    model = _base.TimepointSurveillanceAlgorithm()
    dates = pd.date_range(start="2011", end="2011-12-31", freq="W-Mon")
    future_dates = pd.date_range(start="2011-12-01", end="2013")
    train_data = pd.DataFrame(random_cases_for_dates(dates), index=dates)
    test_data = pd.DataFrame(random_cases_for_dates(future_dates), index=future_dates)
    model.fit(train_data)
    with pytest.raises(ValueError):
        model.predict(test_data)


def test_fit():
    model = _base.TimepointSurveillanceAlgorithm()
    dates = pd.date_range(start="2011", freq="W-Mon", periods=2)
    train_data = pd.DataFrame({"n_cases": [5, 6], "n_outbreak_cases": [0, 1]}, index=dates)
    train_data_before_fit = train_data.copy()
    model.fit(train_data)
    pd.testing.assert_frame_equal(train_data, train_data_before_fit)
    assert (model._training_data.n_cases.values == [5, 5]).all()


def test__get_freq(train_data):
    freq = _base._get_freq(train_data)
    assert freq == 52


def test__get_start_epoch(train_data):
    start_epoch = _base._get_start_epoch(train_data)
    assert start_epoch == 2
