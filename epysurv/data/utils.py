import pandas as pd


def timedelta_weeks(weeks: int):
    return pd.Timedelta(7 * weeks, unit="D")
