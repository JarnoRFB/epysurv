# type: ignore
import pandas as pd


class NonLearningTimeseriesClassificationMixin:
    def fit(self, data_generator):
        """These types of algorithms do not learn from previous time series."""
        pass

    def predict(self, data_generator) -> pd.DataFrame:
        alarms = []
        times = []
        for x, _ in data_generator:
            # Fit on all data, except the last point, that is to be predicted.
            super().fit(x.iloc[:-1])
            prediction = super().predict(
                x.iloc[[-1]]
            )  # Use inner brackets to get dytpe preserving frame and not series.
            # As only a single value should be returned, we can access this single item.
            [alarm] = prediction.alarm
            [time] = prediction.index
            alarms.append(alarm)
            times.append(time)
        return pd.DataFrame({"alarm": alarms}, index=pd.DatetimeIndex(times))
