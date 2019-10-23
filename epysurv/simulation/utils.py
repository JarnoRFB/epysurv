import pandas as pd
import rpy2

from typing import Sequence


def r_list_to_frame(r_list, names: Sequence[str]) -> rpy2.robjects.vectors.ListVector:
    """Transforms a (named) list in R to a Pandas DataFrame"""
    rlist_as_frame = pd.DataFrame({name: list(r_list.rx2(name)) for name in names})
    # Add timestep column to unify frames since some simulations return a timestep column but others don't
    rlist_as_frame["timestep"] = list(range(1, len(rlist_as_frame) + 1))
    return rlist_as_frame


def add_date_time_index_to_frame(df: pd.DataFrame, start="2020") -> "pd.DataFrame":
    df.index = pd.date_range(start=start, periods=len(df), freq="W-MON")
    df.index.name = "dates"
    return df
