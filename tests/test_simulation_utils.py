import pandas as pd

from rpy2 import robjects

from epysurv.simulations.utils import r_list_to_frame, add_date_time_index_to_frame


def test_add_date_time_index_to_frame():
    df = add_date_time_index_to_frame(pd.DataFrame({"a": [1, 2, 3]}))
    freq = pd.infer_freq(df.index)
    assert freq == "W-MON"


def test_r_list_to_frame():
    example_r_list = robjects.r("simulated = list(n_cases = 1:10)")
    as_frame = r_list_to_frame(example_r_list, ["n_cases"])

    expected_frame = pd.DataFrame(
        {"n_cases": list(range(1, 11)), "timestep": list(range(1, 11))}
    )

    pd.testing.assert_frame_equal(as_frame, expected_frame)
