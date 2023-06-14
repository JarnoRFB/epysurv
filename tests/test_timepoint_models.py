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

from tests.utils import drop_column_if_exists, load_predictions

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

    # 'upperbound' does not make sense to check for equality, so let's remove it if it exists
    pred = drop_column_if_exists(pred, "upperbound")
    saved_predictions = drop_column_if_exists(saved_predictions, "upperbound")

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

    # 'upperbound' does not make sense to check for equality, so let's remove it if it exists
    pred = drop_column_if_exists(pred, "upperbound")
    saved_predictions = drop_column_if_exists(saved_predictions, "upperbound")

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
    assert set(test_data.columns) == (set(prediction.columns) - {"alarm", "upperbound"})


def test_validate_data_on_fit(train_data):
    model = EarsC1()
    with pytest.raises(ValueError):
        model.fit(train_data.rename(columns={"n_cases": "wrong_column_name"}))


def test_glrnb_parameters(train_data, test_data):
    # earlier values like theta amd mu0 were hard-coded and could not be passed in so very we get no exception
    # This execution is similar to the R surveillance documentation
    model = GLRNegativeBinomial(upperbound_statistic="cases", theta=1.2)
    # make sure we can fit and predict
    model.fit(train_data)
    _ = model.predict(test_data)


@pytest.mark.parametrize("Algo", algos_to_test)
def test_prediction_witout_labels(train_data, test_data, shared_datadir, Algo):
    """Test only works with same data as `test_prediction`, because sample data contains no outbreaks in the training set."""
    model = Algo()
    with pytest.warns(UserWarning):
        model.fit(train_data[["n_cases"]])
    pred = model.predict(test_data)
    saved_predictions = load_predictions(shared_datadir / f"{Algo.__name__}_pred.csv")

    # 'upperbound' does not make sense to check for equality, so let's remove it if it exists
    pred = drop_column_if_exists(pred, "upperbound")
    saved_predictions = drop_column_if_exists(saved_predictions, "upperbound")

    assert_frame_equal(pred, saved_predictions)


def test_farrington_flexible__raises_on_too_less_reference_data():

    model = FarringtonFlexible()

    total_periods = 100
    test_size = 20
    case_count = 10

    dates = pd.date_range("2017-07-09", periods=total_periods, freq="W")
    case_counts = [case_count] * total_periods

    df = pd.DataFrame({"n_cases": case_counts}, index=dates)

    train_data = df[: -1 * test_size]
    test_data = df[-1 * test_size :]

    model.fit(train_data)
    with pytest.raises(
        ValueError,
        match="You are trying to use reference data from 3 years back for predictions starting from 2019-01-20",
    ):
        _ = model.predict(test_data)
