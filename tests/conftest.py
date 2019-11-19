import pickle
from collections import namedtuple

import pandas as pd
import pytest

from epysurv import data
from epysurv.data.filter_combination import (
    FilterCombination,
    SplitYears,
    TimeseriesClassificationData,
)

TSCGenerator = namedtuple("TSCGenerator", "train_gen test_gen")


@pytest.fixture
def train_data(shared_datadir):
    return _load_data(shared_datadir / "salmonella_train.csv")


@pytest.fixture
def test_data(shared_datadir):
    return _load_data(shared_datadir / "salmonella_test.csv")


def _load_data(filepath):
    data = pd.read_csv(
        filepath, index_col=0, parse_dates=True, infer_datetime_format=True,
    )
    data.index.freq = pd.infer_freq(data.index)
    return data


@pytest.fixture
def tsc_generator(train_data, test_data):
    train_generator, test_generator = data.timeseries_classifaction_generator(
        train_data, test_data, offset_in_weeks=5 * 52
    )
    return TSCGenerator(train_generator, test_generator)


@pytest.fixture
def filter_combination(shared_datadir):
    with open(shared_datadir / "cases.pickle", "rb") as handle:
        cases = pickle.load(handle)
    cases_in_berlin = cases.query('county == "Berlin"')
    return FilterCombination(
        disease="SAL", county="Berlin", pathogen="SAL", data=cases_in_berlin
    )


@pytest.fixture
def expanding_windows(filter_combination):
    tsc_data = filter_combination.expanding_windows(
        min_len_in_weeks=104,
        split_years=SplitYears.from_ts_input("2005", "2009", "2011"),
    )
    return tsc_data


@pytest.fixture(params=["timeseries", "cases"])
def tsc_data(request, tsc_generator, expanding_windows):
    if request.param == "timeseries":
        return tsc_generator
    elif request.param == "cases":
        return expanding_windows
