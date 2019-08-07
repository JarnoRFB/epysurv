import platform
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from pandas.tseries import offsets
from rpy2.robjects import numpy2ri, pandas2ri, r
from rpy2.robjects.packages import importr

from epysurv.metrics.outbreak_detection import ghozzi_score


def silence_R_output():
    """Silence output from R code.

    This is useful, because some algorithm otherwise print every time they are invoked.
    """
    if platform.system() == "Linux":
        r.sink("/dev/null")
    elif platform.system() == "Windows":
        r.sink("NUL")


silence_R_output()
numpy2ri.activate()
pandas2ri.activate()
surveillance = importr("surveillance")


@dataclass
class TimepointSurveillanceAlgorithm:
    """Algorithms that predict outbreaks for every timepoint."""

    _training_data: pd.DataFrame = field(init=False, repr=False)

    def fit(self, data: pd.DataFrame):
        """Expects data with time series index, case counts and outbreak labels."""
        # Remove outbreaks cases from baseline.
        data = data.copy()
        data.n_cases -= data.n_outbreak_cases
        self._training_data = data

    def predict(self, data: pd.DataFrame):
        """Expects data with time series index and case counts."""
        self._data_in_the_future(data)

    def score(self, data_with_labels: pd.DataFrame):
        prediction_result = self.predict(data_with_labels)
        return ghozzi_score(prediction_result)

    def _validate_data(self, data: pd.DataFrame):
        self._contains_dates(data)
        self._contains_counts(data)

    def _contains_dates(self, data: pd.DataFrame):
        has_dates = "ds" in data.columns or isinstance(data.index, pd.DatetimeIndex)
        if not has_dates:
            raise ValueError("No dates")

    def _contains_counts(self, data: pd.DataFrame):
        if not {"n_cases", "n_outbreak_cases"} < set(data.columns):
            raise ValueError('No column named "n_cases"')

    def _data_in_the_future(self, data: pd.DataFrame):
        if data.index.min() <= self._training_data.index.max():
            raise ValueError("The prediction data overlaps with the training data.")


offset_to_freq = {offsets.Day: 365, offsets.Week: 52, offsets.MonthBegin: 12, offsets.MonthEnd: 12}

offset_to_attr = {offsets.Day: "day", offsets.Week: "week", offsets.MonthBegin: "month", offsets.MonthEnd: "month"}


def _get_freq(data) -> int:
    return offset_to_freq[type(data.index.freq)]


def _get_start_epoch(data: pd.DataFrame) -> str:
    return getattr(data.index[0], offset_to_attr[type(data.index.freq)])


class SurveillanceRPackageAlgorithm(TimepointSurveillanceAlgorithm):
    """Base class for the algorithm from the R package surveillance."""

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Predict outbreaks.

        Attributes
        ----------
        data
            Dataframe with DateTimeIndex containing the columns "n_cases".

        Returns
        -------
            Original dataframe with "alarm" column added.
        """
        super().predict(data)
        prediction_len = len(data)
        # Concat training and prediction data. make index array for range param.
        data = (
            pd.concat((self._training_data, data), keys=["train", "test"])
            .reset_index(level=0)
            .rename(columns={"level_0": "provenance"})
        )
        r_instance = self._prepare_r_instance(data)
        # R indexes are 0-based. Therefore we add 1.
        detection_range = robjects.IntVector(np.where(data.provenance == "test")[0] + 1)
        surveillance_result = self._call_surveillance_algo(r_instance, detection_range)
        alarm = self._extract_alarms(surveillance_result)
        predictions = data.copy()
        predictions["alarm"] = np.append((len(predictions) - len(alarm)) * [np.nan], alarm)
        predictions = predictions.iloc[-prediction_len:]
        return predictions

    def _None_to_NULL(self, obj):
        return robjects.NULL if obj is None else obj

    def _prepare_r_instance(self, data: pd.DataFrame):
        """Transform dataframe into R data structure on which the R algorithm can work."""
        raise NotImplementedError

    def _extract_alarms(self, surveillance_result):
        """Extract the binary alarm array from the surveillance result R data structure."""
        raise NotImplementedError

    def _call_surveillance_algo(self, sts, detection_range):
        raise NotImplementedError


class STSBasedAlgorithm(SurveillanceRPackageAlgorithm):
    """Base class for algorithms that operate on the STS (SurveillanceTimeSeries) class."""

    def _prepare_r_instance(self, data: pd.DataFrame):
        if data.index.freq is None:
            freq = pd.infer_freq(data.index)
            if freq is None:
                raise ValueError(f"The time series index has no valid frequency. Index={data.index}")
            data.index.freq = freq
        sts = surveillance.sts(
            start=r.c(data.index[0].year, _get_start_epoch(data)),
            epoch=robjects.IntVector([r["as.numeric"](r["as.Date"](d.isoformat()))[0] for d in data.index.date]),
            # epoch=data.index,
            freq=_get_freq(data),
            observed=data["n_cases"].values,
            epochAsDate=True,
        )
        return sts

    def _extract_alarms(self, surveillance_result):
        return np.asarray(surveillance_result.slots["alarm"])


class DisProgBasedAlgorithm(STSBasedAlgorithm):
    """Base class for algorithms that operate on the disProg (disease progress) class."""

    def _prepare_r_instance(self, data: pd.DataFrame):
        sts = super()._prepare_r_instance(data)
        return surveillance.sts2disProg(sts)

    def _extract_alarms(self, surveillance_result):
        return np.asarray(dict(zip(surveillance_result.names, list(surveillance_result)))["alarm"])
