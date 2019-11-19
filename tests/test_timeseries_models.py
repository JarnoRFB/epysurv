import numpy as np
import pandas as pd

from epysurv.models.timeseries import Farrington, GLRPoisson  # type: ignore

from .utils import load_predictions


def test_farrington_timeseries_prediciton(tsc_generator, shared_datadir):
    model = Farrington(alpha=0.1)
    model.fit(tsc_generator.train_gen)
    pred = model.predict(tsc_generator.test_gen)
    saved_predictions = load_predictions(
        shared_datadir / "farrington_timeseries_predictions.csv",
    )

    pd.testing.assert_series_equal(pred.alarm, saved_predictions.alarm)


def test_outbreak_case_subtraction():
    def test_gen():
        df = pd.DataFrame(
            {"n_cases": np.ones(100) * 5, "n_outbreak_cases": np.ones(100) * 3},
            index=pd.date_range("2020", freq="W-MON", periods=100),
        )
        yield df, True

    model = Farrington()
    _ = model.predict(test_gen())
    assert np.alltrue(model._training_data.n_cases.values == 2)
