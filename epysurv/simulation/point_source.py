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
    r"""Simulation of epidemics which were introduced by point sources.

    The basis of this programme is a combination of a Hidden Markov Model
    (to get random time points for outbreaks) and a simple model
    (compare :class:`epysurv.simulation.SeasonalNoise`) to simulate the baseline.

    Parameters
    ----------
    amplitude
        Amplitude of the sine. Determines the possible range of simulated seasonal cases.
    alpha
        Parameter to move along the y-axis (negative values are not allowed) with `alpha` >= `amplitude`.
    frequency
        Factor in oscillation term. Is multiplied with the annual term :math:`\omega` and the current time point.
    p
        Probability to get a new outbreak at time :math:`t` if there was one at time :math:`t-1`.
    r
        Probability to get no new outbreak at time :math:`t` if there was none at time :math:`t-1`.
    seasonal_move
        A term added to time point :math:`t` to move the curve along the x-axis.
    seed
        Seed for the random number generation.
    trend
        Controls the influence of the current week on :math:`\mu`.

    References
    ----------
        http://surveillance.r-forge.r-project.org/
    """

    alpha: float = 1.0
    amplitude: float = 1.0
    frequency: int = 1
    p: float = 0.99
    r: float = 0.01
    seasonal_move: int = 0
    seed: Optional[int] = None
    trend: float = 0.0

    def simulate(
        self,
        length: int,
        state_weight: float = 0,
        state: Optional[Sequence[int]] = None,
    ) -> pd.DataFrame:
        """Simulate outbreaks.

        Parameters
        ----------
        length
            Number of weeks to model. ``length`` is ignored if ``state`` is given. In this case, the length of
            ``state`` is used.
        state
            Use a state chain to define the status at this time point (outbreak or not). If not given, a Markov chain is
            generated automatically.
        state_weight
            Additional weight for an outbreak which influences the distribution parameter mu.

        Returns
        -------
            A ``DataFrame`` of simulated case counts per week, separated into baseline and outbreak cases.
        """
        if self.seed:
            base.set_seed(self.seed)
        simulated = surveillance.sim_pointSource(
            p=self.p,
            r=self.r,
            length=length,
            A=self.amplitude,
            alpha=self.alpha,
            beta=self.trend,
            phi=self.seasonal_move,
            frequency=self.frequency,
            state=robjects.NULL if state is None else robjects.IntVector(state),
            K=state_weight,
        )

        simulated_as_frame = r_list_to_frame(simulated, ["observed", "state"])
        return simulated_as_frame.pipe(add_date_time_index_to_frame).rename(
            columns={"observed": "n_cases", "state": "is_outbreak"}
        )
