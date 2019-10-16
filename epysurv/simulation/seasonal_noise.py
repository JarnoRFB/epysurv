import rpy2.robjects.packages as rpackages
import pandas as pd

from rpy2 import robjects
from typing import Sequence


from epysurv.simulation.utils import r_list_to_frame, add_date_time_index_to_frame


surveillance = rpackages.importr("surveillance")


def simulate_outbreaks(
    length: int,
    seed: int,
    amplitude: float = 1,
    alpha: float = 1,
    beta: float = 0,
    phi: int = 0,
    frequency: float = 1,
    state: Sequence[int] = None,
    state_weight: float = 0,
) -> pd.DataFrame:
    """Generation of a cyclic model of a Poisson distribution as background data for a simulated timevector.

    The mean of the Poisson distribution is modelled as:
    :math:`\\mu = \\exp{(A\\sin{(frequency \\cdot (t + \\phi))} + \\alpha + \\beta * t + L * state)}`

    Attributes
    ----------
    amplitude
        amplitude (range of sinus), default = 1.
    alpha
        parameter to move along the y-axis (negative values not allowed) with alpha >= amplitude, default = 1.
    beta
        regression coefficient, default = 0.
    phi
        factor to create seasonal moves (moves the curve along the x-axis), default = 0.
    length
        number of weeks to model.
    frequency
        factor to determine the oscillation-frequency, default = 1.
    seed
        a seed for the random number generation
    state
        if a state chain is entered the outbreaks will be additional weighted by state_weight
    state_weight
        additional weight for an outbreak which influences the distribution parameter mu, default = 0.

    Returns
    -------
    A DataFrame of an endemic time series that contains n weeks where n=``length``.
    The DataFrame is divided into timesteps where each step is equivalent to one calender week.
    It contains a ``mean`` column which is the mean case count according to the sinus based model.
    And finally, it contains a column ``n_cases`` that consists of the generates case counts
    based on the sinus model
    """
    if seed:
        robjects.r(f"set.seed({seed})")
    simulated = surveillance.sim_seasonalNoise(
        A=amplitude,
        alpha=alpha,
        beta=beta,
        phi=phi,
        length=length,
        frequency=frequency,
        state=robjects.NULL if state is None else robjects.IntVector(state),
        K=state_weight,
    )

    simulated = r_list_to_frame(simulated, ["mu", "seasonalBackground"])
    simulated = (
        simulated.pipe(add_date_time_index_to_frame)
        .rename(columns={"mu": "mean", "seasonalBackground": "n_cases"})
        .assign(n_outbreak_cases=0)
    )
    return simulated
