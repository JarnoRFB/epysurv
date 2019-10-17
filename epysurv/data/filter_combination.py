from collections import namedtuple
from dataclasses import dataclass, field

import pandas as pd

from .utils import timedelta_weeks


class SplitYears:
    """Data structure that holds the years data should be split into training and test set.

    start to middle is the training data. middle to end is the test data.
    """

    def __init__(self, start: pd.Timestamp, middle: pd.Timestamp, end: pd.Timestamp):
        if not (start < middle < end):
            raise ValueError("start, middle and end must be consecutive.")
        self.start = start
        self.middle = middle
        self.end = end

    @classmethod
    def from_ts_input(cls, start, middle, end):
        """Create instance from inputs that are passed through ``pd.Timestamp``."""
        start = pd.Timestamp(start)
        middle = pd.Timestamp(middle)
        end = pd.Timestamp(end)
        return cls(start, middle, end)


TimeseriesClassificationData = namedtuple(
    "TimeseriesClassificationData",
    ["train_final", "test_final", "train_gen", "test_gen"],
)

FREQ = "W-MON"


@dataclass
class FilterCombination:
    """Representation of case records filtered by combination of county and pathogen.

    Attributes
    ----------
    disease
        The disease from which the cases suffer.
    county
        The county in which the cases where reported.
    pathogen
        The pathogen subtype.
    data
        The case records.
    """

    disease: str
    county: str
    pathogen: str
    data: pd.DataFrame = field(repr=False)

    def expanding_windows(
        self, min_len_in_weeks: int, split_years: SplitYears
    ) -> TimeseriesClassificationData:
        """
        Transform case records into expanding time series.

        Parameters
        ----------
        min_len_in_weeks
            The minimum length of each time series.
        split_years
            The years at which to split the data into train and test data.

        Returns
        -------
        Compound object of train and test data as generators and dataframes.
        """
        self._validate_input(min_len_in_weeks, split_years)

        train_data = self.data.query(
            "@split_years.start <= ReportingDate < @split_years.middle"
        )
        test_data = self.data.query(
            "@split_years.start <= ReportingDate < @split_years.end"
        )

        offset = split_years.start + timedelta_weeks(min_len_in_weeks)

        true_train = (
            pd.DataFrame(
                index=pd.date_range(
                    offset, split_years.middle, freq=FREQ, closed="left"
                )
            )
            .join(_to_recent_timeseries(train_data))
            .fillna(0)
            .assign(outbreak=lambda df: df.n_outbreak_cases > 0)
        )
        true_test = (
            pd.DataFrame(
                index=pd.date_range(
                    split_years.middle, split_years.end, freq=FREQ, closed="left"
                )
            )
            .join(
                _to_recent_timeseries(
                    self.data.query(
                        "@split_years.middle <= ReportingDate < @split_years.end"
                    )
                )
            )
            .fillna(0)
            .assign(outbreak=lambda df: df.n_outbreak_cases > 0)
        )

        train_gen = self._expanding_frame(
            train_data,
            true_train,
            offset=offset,
            start=split_years.start,
            end=split_years.middle,
        )
        test_gen = self._expanding_frame(
            test_data,
            true_test,
            offset=split_years.middle,
            start=split_years.start,
            end=split_years.end,
        )

        return TimeseriesClassificationData(true_train, true_test, train_gen, test_gen)

    def _validate_input(self, min_len_in_weeks, split_years):
        # TODO: while this makes sense, it is turned off for now, because most of the data, does not
        # have a case in 2019 yet.
        # if self.data.ReportingDate.max() < split_years.end:
        #     raise ValueError(f'The end date must be before the last case, but is {split_years.end}')
        if split_years.start < self.data.ReportingDate.min():
            raise ValueError(
                f"The start date must be after the first case, but is {split_years.start}"
            )
        if split_years.middle < split_years.start + timedelta_weeks(min_len_in_weeks):
            raise ValueError(
                f"The start date plus the offset must be before the middle date, "
                f"but is {split_years.start + timedelta_weeks(min_len_in_weeks)}"
            )

    def _expanding_frame(
        self,
        data: pd.DataFrame,
        final_data: pd.DataFrame,
        offset: pd.Timestamp,
        start: pd.Timestamp,
        end: pd.Timestamp,
    ):
        for date in pd.date_range(offset, end, freq=FREQ, closed="left"):
            ts = (
                data
                # .copy()
                .query(
                    "ValidFrom <= @date & (ValidUntil > @date | @pd.isna(ValidUntil))"
                )
                .set_index("ReportingDate")
                .groupby(pd.Grouper(freq=FREQ))
                .agg({"IdRecord": "count", "IdRecordAusbruchOut": "count"})
                .rename(
                    columns={
                        "IdRecord": "n_cases",
                        "IdRecordAusbruchOut": "n_outbreak_cases",
                    }
                )
            )
            ts = (
                pd.DataFrame(index=pd.date_range(start, date, freq=FREQ))
                .join(ts)
                .fillna(0)
            )
            outbreak = final_data.loc[date].outbreak
            yield ts, outbreak


def _to_recent_timeseries(data: pd.DataFrame) -> pd.DataFrame:
    """Get a time series from case data, that represents the most recent state."""
    return (
        data.query("IsCurrent")
        .set_index("ReportingDate")
        .groupby(pd.Grouper(freq=FREQ))
        .agg({"IdRecord": "count", "IdRecordAusbruchOut": "count"})
        .rename(
            columns={"IdRecord": "n_cases", "IdRecordAusbruchOut": "n_outbreak_cases"}
        )
    )
