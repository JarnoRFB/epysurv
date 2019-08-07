import numpy as np
import pandas as pd
from pytest import raises

from epysurv.data.filter_combination import SplitYears


def test_basic_output(tsc_data):
    frame, y = next(tsc_data.train_gen)
    assert isinstance(frame, pd.DataFrame)
    assert y in (0, 1)


def test_time_series_classification_generator_train_spacing(tsc_data):
    frame_lengths = [len(X) for X, _ in tsc_data.train_gen]
    assert np.alltrue(pd.Series(frame_lengths).diff().dropna() == 1)


def test_time_series_classification_generator_test_spacing(tsc_data):
    frame_lengths = [len(X) for X, _ in tsc_data.test_gen]
    assert np.alltrue(pd.Series(frame_lengths).diff().dropna() == 1)


def test_train_ends_before_test(tsc_data):
    frame_lengths_train = [len(X) for X, _ in tsc_data.train_gen]
    frame_lengths_test = np.array([len(X) for X, _ in tsc_data.test_gen])
    for frame_length_train in frame_lengths_train:
        assert np.alltrue(frame_length_train < frame_lengths_test)


def test_train_frequency(tsc_data):
    for frame, y in tsc_data.train_gen:
        assert pd.infer_freq(frame.index) == "W-MON"


def test_test_frequency(tsc_data):
    for frame, y in tsc_data.test_gen:
        assert pd.infer_freq(frame.index) == "W-MON"


def test_raises_on_early_start(filter_combination):
    with raises(ValueError, match="The start date"):
        filter_combination.expanding_windows(
            min_len_in_weeks=104, split_years=SplitYears.from_ts_input("1999", "2009", "2011")
        )


# TODO: reactivate later
# def test_raises_on_late_end(filter_combination):
#     with raises(ValueError, match='The end date'):
#         filter_combination.expanding_windows(min_len_in_weeks=104,
#                                              split_years=SplitYears.from_ts_input('2005', '2009', '2020'))


def test_raises_on_high_offset(filter_combination):
    with raises(ValueError, match="The start date plus the offset"):
        filter_combination.expanding_windows(
            min_len_in_weeks=500, split_years=SplitYears.from_ts_input("2005", "2009", "2011")
        )


def test_split_year_order():
    with raises(ValueError, match="consecutive"):
        SplitYears.from_ts_input("2011", "2012", "2010")
