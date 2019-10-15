import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from epysurv.simulations import point_source, seasonal_noise


def load_simulations(filepath):
    simulations = pd.read_csv(
        filepath, index_col=0, parse_dates=True, infer_datetime_format=True
    )
    return simulations


simulations_to_test = [
    (point_source, {"state_weight": 1, "seed": 1}),
    (seasonal_noise, {"length": 100, "seed": 1}),
]


@pytest.mark.parametrize("simulation_algo, params", simulations_to_test)
def test_simulate_outbreaks(simulation_algo, params, shared_datadir):
    """Test against changes in simulation behavior."""
    simulated = simulation_algo.simulate_outbreaks(**params)
    saved_simulation = load_simulations(
        shared_datadir / f"{simulation_algo.__name__.split('.')[-1]}_simulation.csv"
    )
    assert_frame_equal(simulated, saved_simulation)
