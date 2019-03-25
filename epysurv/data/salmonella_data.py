from typing import *
import os
import pandas as pd
from collections import namedtuple

from .utils import timedelta_weeks

TimeseriesClassificationData = namedtuple('TimeseriesClassificationData', ['train', 'test', 'train_gen', 'test_gen'])


def salmonella():
    """Count data from Salmonella newport in Germany."""
    train = _load_data('salmonella_train.csv')
    test = _load_data('salmonella_test.csv')
    return train, test


def timeseries_classifcation(train: pd.DataFrame, test: pd.DataFrame,
                             offset_in_weeks: int) -> TimeseriesClassificationData:
    """Convert standard timeseries for usage in time series classification."""
    train_gen, test_gen = timeseries_classifaction_generator(train, test, offset_in_weeks)
    return TimeseriesClassificationData(train, test, train_gen, test_gen)


def timeseries_classifaction_generator(
        train: pd.DataFrame, test: pd.DataFrame, offset_in_weeks: int) -> Tuple[Generator, Generator]:
    """Turn a time point classification problem into a time series classification problem."""
    offset = train.index[0] + timedelta_weeks(offset_in_weeks)
    train_generator = _growing_frame(train, offset=offset)
    whole_data = pd.concat((train, test))
    test_generator = _growing_frame(whole_data, offset=train.index[-1])
    return train_generator, test_generator


def _load_data(filename: str):
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), filename), index_col=0, parse_dates=True,
                       infer_datetime_format=True)
    data.index.freq = pd.infer_freq(data.index)
    return data


def _growing_frame(data: pd.DataFrame, offset: pd.Timestamp):
    before_begin_data = data.query('index <= @offset')
    after_begin_data = data.query('index > @offset')
    new_frame = before_begin_data.copy()
    for idx, row in after_begin_data.iterrows():
        new_frame.loc[idx] = row
        yield new_frame, new_frame.iloc[-1].outbreak
