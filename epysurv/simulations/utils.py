import pandas as pd

from typing import Sequence


def r_list_to_frame(r_list, names: Sequence[str], with_time_indeces=True):
    rlist_as_frame = pd.DataFrame({name: list(r_list.rx2(name)) for name in names})
    if with_time_indeces:
        with_date_time_index = add_date_time_index_to_frame(rlist_as_frame)
        with_date_time_index["timestep"] = list(range(1, len(with_date_time_index) + 1))
        return with_date_time_index
    else:
        return rlist_as_frame


def add_date_time_index_to_frame(df: pd.DataFrame, start="2020"):
    df.index = pd.date_range(start=start, periods=len(df), freq="W-MON")
    df.index.name = "dates"
    return df
