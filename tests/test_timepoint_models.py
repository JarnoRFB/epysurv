import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from epysurv.models.timepoint import (
    CDC,
    HMM,
    RKI,
    Bayes,
    Boda,
    Cusum,
    EarsC1,
    EarsC2,
    EarsC3,
    Farrington,
    FarringtonFlexible,
    GLRNegativeBinomial,
    GLRPoisson,
    OutbreakP,
)


def load_predictions(filepath):
    predictions = pd.read_csv(
        filepath, index_col=0, parse_dates=True, infer_datetime_format=True
    )
    return predictions


algos_to_test = [
    EarsC1,
    EarsC2,
    EarsC3,
    Farrington,
    FarringtonFlexible,
    Cusum,
    Bayes,
    RKI,
    GLRNegativeBinomial,
    GLRPoisson,
    OutbreakP,
    CDC,
]


@pytest.mark.parametrize("Algo", algos_to_test)
def test_prediction(train_data, test_data, shared_datadir, Algo):
    """Regression tests against a change in the prediction behavior."""
    model = Algo()
    model.fit(train_data)
    pred = model.predict(test_data)
    saved_predictions = load_predictions(shared_datadir / f"{Algo.__name__}_pred.csv")
    assert_frame_equal(pred, saved_predictions)


# These algorithms take to long to be tested every time.
long_algos_to_test = [
    HMM,
    Boda,
]  # TODO: Boda throws strange error when run in the test.


@pytest.mark.skip
@pytest.mark.parametrize("Algo", long_algos_to_test)
def test_long_prediction(train_data, test_data, shared_datadir, Algo):
    """Regression tests against a change in the prediction behavior."""
    model = Algo()
    model.fit(train_data)
    pred = model.predict(test_data)
    saved_predictions = load_predictions(shared_datadir / f"{Algo.__name__}_pred.csv")
    assert_frame_equal(pred, saved_predictions)


def test_fit_does_not_change_input(train_data, test_data):
    model = EarsC1()
    original_train_data = train_data.copy()
    model.fit(train_data)
    assert_frame_equal(original_train_data, train_data)


def test_predict_does_not_change_input(train_data, test_data):
    model = EarsC1()
    original_train_data = train_data.copy()
    original_test_data = test_data.copy()
    _ = model.fit(train_data).predict(test_data)
    assert_frame_equal(original_train_data, train_data)
    assert_frame_equal(original_test_data, test_data)


def test_output_format(train_data, test_data):
    model = EarsC1()
    original_train_data = train_data.copy()
    original_test_data = test_data.copy()
    prediction = model.fit(train_data).predict(test_data)
    assert set(test_data.columns) == (set(prediction.columns) - {"alarm"})


def test_validate_data_on_fit(train_data):
    model = EarsC1()
    with pytest.raises(ValueError):
        model.fit(train_data.rename(columns={"n_cases": "wrong_column_name"}))


@pytest.mark.parametrize("Algo", algos_to_test)
def test_prediction_witout_labels(train_data, test_data, shared_datadir, Algo):
    """Test only works with same data as `test_prediction`, because sample data contains no outbreaks in the training set."""
    model = Algo()
    with pytest.warns(UserWarning):
        model.fit(train_data[["n_cases"]])
    pred = model.predict(test_data)
    saved_predictions = load_predictions(shared_datadir / f"{Algo.__name__}_pred.csv")
    assert_frame_equal(pred, saved_predictions)
