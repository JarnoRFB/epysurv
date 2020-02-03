import inspect

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from epysurv.simulation import (
    PointSource,
    SeasonalNoiseNegativeBinomial,
    SeasonalNoisePoisson,
)


def load_simulations(filepath):
    simulations = pd.read_csv(
        filepath, index_col=0, parse_dates=True, infer_datetime_format=True
    )
    return simulations


@pytest.mark.parametrize(
    "SimulationAlgo", [PointSource, SeasonalNoisePoisson, SeasonalNoiseNegativeBinomial]
)
def test_simulate_outbreaks(SimulationAlgo, shared_datadir):
    """Test against changes in simulation behavior."""
    simulation_model = SimulationAlgo(seed=1)
    if "state_weight" in inspect.signature(simulation_model.simulate).parameters:
        simulated = simulation_model.simulate(length=100, state_weight=1)
    else:
        simulated = simulation_model.simulate(length=100)
    saved_simulation = load_simulations(
        shared_datadir / f"{SimulationAlgo.__name__}_simulation.csv"
    )
    assert_frame_equal(simulated, saved_simulation)


@pytest.mark.parametrize(
    "SimulationAlgo", [PointSource, SeasonalNoisePoisson, SeasonalNoiseNegativeBinomial]
)
def test_simulation_model_format(SimulationAlgo):
    simulation_model = SimulationAlgo()
    simulated = simulation_model.simulate(length=1)
    assert "n_cases" in simulated.columns


def test_seasonality():
    snnb = SeasonalNoiseNegativeBinomial()
    assert snnb._seasonality(1) == 0.15032710271748156
