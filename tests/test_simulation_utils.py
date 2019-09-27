import pandas as pd
import pytest

from rpy2 import robjects

from epysurv.simulation.seasonal_noise import simulate_outbreaks
from epysurv.simulation.utils import r_list_to_frame, add_date_time_index_to_frame


def test_add_date_time_index_to_frame():
    df = add_date_time_index_to_frame(pd.DataFrame({"a": [1, 2, 3]}))
    freq = pd.infer_freq(df.index)
    assert freq is not None


def test_r_list_to_frame():
    example_r_list = robjects.r("simulated = list(n_cases = 1:10)")
    as_frame = r_list_to_frame(example_r_list, ["n_cases"])
    assert all(as_frame["timestep"].values == range(1, len(as_frame) + 1))
