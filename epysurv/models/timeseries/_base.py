# type: ignore
import pandas as pd


class NonLearningTimeseriesClassificationMixin:
    def fit(self, data_generator):
        """These types of algorithms do not learn from previous time series."""
        pass

    def predict(self, data_generator) -> pd.DataFrame:
        alarms = []
        upperbounds = []
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

            # Check if "upperbound" is available and add if available
            if hasattr(prediction, "upperbound"):
                [upperbound] = prediction.upperbound
                upperbounds.append(upperbound)

            alarms.append(alarm)
            times.append(time)

        frame_dict = {"alarm": alarms}
        if len(upperbounds) > 0:
            frame_dict["upperbound"] = upperbounds

        return pd.DataFrame(frame_dict, index=pd.DatetimeIndex(times, freq="infer"))
