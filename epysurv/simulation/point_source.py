from dataclasses import dataclass
from typing import Optional, Sequence

import pandas as pd
import rpy2.robjects.packages as rpackages
from rpy2 import robjects

from epysurv.simulation.base import BaseSimulation
from epysurv.simulation.utils import add_date_time_index_to_frame, r_list_to_frame

surveillance = rpackages.importr("surveillance")
base = rpackages.importr("base")


@dataclass
class PointSource(BaseSimulation):
    """Simulation of epidemics which were introduced by point sources.

    The basis of this programme is a combination of a Hidden Markov Model
    (to get random timepoints for outbreaks) and a simple model
    (compare :class:`epysurv.simulation.seasonal_noise`) to simulate the baseline.

    Attributes
    ----------
    amplitude
        amplitude (range of sinus), default = 1.
    alpha
        parameter to move along the y-axis (negative values not allowed) with alpha >= amplitude, default = 1.
    beta
        regression coefficient, default = 0.
    frequency
        factor to determine the oscillation-frequency, default = 1.
    p
       probability to get a new outbreak at time i if there was one at time i-1, default 0.99.
    phi
       factor to create seasonal moves (moves the curve along the x-axis), default = 0.
    r
        probability to get no new outbreak at time i if there was none at time i-1, default 0.01.
    seed
        a seed for the random number generation

    References
    ----------
    http://surveillance.r-forge.r-project.org/
    """

    alpha: float = 1.0
    amplitude: float = 1.0
    beta: float = 0.0
    frequency: int = 1
    p: float = 0.99
    phi: int = 0
    r: float = 0.01
    seed: Optional[int] = None

    def simulate(
        self,
        length: int,
        state_weight: float = 0,
        state: Optional[Sequence[int]] = None,
    ) -> pd.DataFrame:
        """
        Parameters
        -------
        length
            number of weeks to model, default 100. length is ignored if state is given. In this case the length of state
            is used.
        state
            use a state chain to define the status at this timepoint (outbreak or not).  If not given, a Markov chain is
            generated by the programme, default None.
        state_weight
            additional weight for an outbreak which influences the distribution parameter mu, default = 0.

        Returns
        -------
        A DataFrame of an epidemic time series that contains n weeks where n=``length`` or length of ``state``.
        Each row in the DataFrame's represents one timesteps where each step is equivalent to one calender week.
        The DataFrame contains the case number in the column ``n_cases`` and the column ``is_outbreak`` contains
        a Boolean weather this week contains outbreak cases."""
        if self.seed:
            base.set_seed(self.seed)
        simulated = surveillance.sim_pointSource(
            p=self.p,
            r=self.r,
            length=length,
            A=self.amplitude,
            alpha=self.alpha,
            beta=self.beta,
            phi=self.phi,
            frequency=self.frequency,
            state=robjects.NULL if state is None else robjects.IntVector(state),
            K=state_weight,
        )

        simulated_as_frame = r_list_to_frame(simulated, ["observed", "state"])
        return (
            simulated_as_frame.pipe(add_date_time_index_to_frame)
            .rename(columns={"observed": "n_cases", "state": "is_outbreak"})
            .assign(n_outbreak_cases=lambda df: df["n_cases"] * df["is_outbreak"])
        )