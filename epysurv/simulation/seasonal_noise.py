from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np
import pandas as pd
import rpy2.robjects.packages as rpackages
from rpy2 import robjects
from scipy.stats import nbinom, poisson

from epysurv.simulation.base import BaseSimulation
from epysurv.simulation.utils import add_date_time_index_to_frame, r_list_to_frame

surveillance = rpackages.importr("surveillance")


@dataclass
class SeasonalNoisePoisson(BaseSimulation):
    r"""Simulation of an endemic time series based on a Poisson distribution.

    The mean of the Poisson distribution is modelled as:

        :math:`\mu(t) = \exp{(A\sin{(frequency \cdot \omega \cdot (t + \phi))}
        + \alpha + \beta \cdot t + K \cdot state)}`

    with :math:`\omega = \pi / 52`, :math:`A` being the amplitude, :math:`\beta` the trend parameter, :math:`t`
    the current week, and :math:`\theta` the seasonal move.

    Parameters
    ----------
    amplitude
        Amplitude of the sine. Determines the range of simulated cases.
    alpha
        Parameter to move simulation along the y-axis (negative values are not allowed) with `alpha` >= `amplitude`.
    frequency
        Factor in oscillation term. Is multiplied with the annual term :math:`\omega` and the current time point.
    seasonal_move
        A term added to each time point :math:`t` to move the curve along the x-axis.
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
    seasonal_move: int = 0
    seed: Optional[int] = None
    trend: float = 0.0

    def simulate(
        self,
        length: int,
        state_weight: Optional[float] = None,
        state: Optional[Sequence[int]] = None,
    ) -> pd.DataFrame:
        r"""
        Simulate outbreaks.

        Parameters
        ----------
        length
            Number of weeks to model. ``length`` is ignored if ``state`` is given. In this case the length of ``state``
            is used.
        state
            Use a state chain to define the status at this time point (outbreak or not). If not given, a Markov chain is
            generated automatically.
        state_weight
            Additional weight for an outbreak which influences the distribution parameter :math:`\mu`.

        Returns
        -------
            A ``DataFrame`` of an endemic time series where each row contains the case counts of this week.
            It also contains the mean case count value based on the underlying sinus model.
        """
        if self.seed:
            base = robjects.packages.importr("base")
            base.set_seed(self.seed)
        simulated = surveillance.sim_seasonalNoise(
            A=self.amplitude,
            alpha=self.alpha,
            beta=self.trend,
            phi=self.seasonal_move,
            length=length,
            frequency=self.frequency,
            state=robjects.NULL if state is None else robjects.IntVector(state),
            K=robjects.NULL if state_weight is None else state_weight,
        )

        simulated = r_list_to_frame(simulated, ["mu", "seasonalBackground"])
        simulated = simulated.pipe(add_date_time_index_to_frame).rename(
            columns={"mu": "mean", "seasonalBackground": "n_cases"}
        )
        return simulated


@dataclass
class SeasonalNoiseNegativeBinomial(BaseSimulation):
    r"""A time series simulation that generates case counts based on a negative binomial model.

    The model is described by a mean :math:`\mu`, variance :math:`\phi \cdot \mu`, and a linear predictor including
    trend and seasonality determined by Fourier terms. :math:`\mu` of the model depends on the current week and
    is defined as follows:

        :math:`\mu(t) = \exp \left\{ \theta + \beta t + \sum_{j=1}^{m} \left\{ \gamma_{1} \cos (\frac{2\pi j t}{52})
        + \gamma_{2} \sin (\frac{2\pi j t}{52}) \right\} \right\}`

    where :math:`t` is the current week, :math:`m` the seasonality length, :math:`\beta` equals to the trend parameter,
    :math:`\gamma` is a seasonality parameter, and :math:`\theta` is the baseline frequency of the cases.

    The simulation is then run using
    :math:`\mu` and the dispersion parameter :math:`\phi` to specify the
    negative binomial model we draw case counts from.

    Parameters
    ----------
    baseline_frequency
        Baseline frequency of cases.
    dispersion
        Regulates the overdispersion compared to the Poisson distribution (:math:`\phi \cdot \mu`).
    seasonality_cos
        Seasonality parameter to model :math:`\cos` of the Fourier term.
    seasonality_sin
        seasonality parameter to model :math:`\sin` of the Fourier term.
    seasonality_length
        Models the annual-wise seasonality. 0 equals to no seasonality, 1 to annual seasonality, 2 to
        biannual seasonality and so forth.
    seed
        A seed for the random number generation.
    trend
        Controls the influence of the current week on :math:`\mu`.

    References
    ----------
    .. [1] Noufaily, A., Enki, D.G., Farrington, C.P., Garthwaite, P., Andrews, N.J., Charlett, A. (2012): An
        improved algorithm for outbreak detection in multiple surveillance systems. Statistics in Medicine,
        32 (7), 1206-1222.
    """

    baseline_frequency: float = 1.5
    dispersion: float = 1.0
    seasonality_cos: float = 0.2
    seasonality_sin: float = -0.4
    seasonality_length: int = 1
    seed: Optional[int] = None
    trend: float = 0.003

    def _seasonality(self, week: int):
        """A Fourier-based seasonality term to model the season-depended case counts.

        Parameters
        ----------
        week
            The week to model the season-based case count.
        """
        years = np.arange(1, self.seasonality_length + 1)
        return np.sum(
            self.seasonality_cos * np.cos((2 * np.pi * years * week) / 52)
            + self.seasonality_sin * np.sin((2 * np.pi * years * week) / 52)
        )

    def simulate(self, length: int) -> pd.DataFrame:
        r"""Simulate outbreaks.

        Parameters
        ----------
        length
            Number of weeks to model.

        Returns
        -------
            A ``DataFrame`` of an endemic time series where each row contains the case counts ot this week.
        """
        if self.seed:
            np.random.seed(self.seed)
        mu_s = [
            np.exp(
                self.baseline_frequency + self.trend * week + self._seasonality(week)
            )
            for week in range(length)
        ]
        if self.dispersion == 1:
            cases = [poisson.rvs(mu, size=1)[0] for mu in mu_s]
        else:
            cases = []
            for mu in mu_s:
                r = np.float(mu / (self.dispersion - 1))
                p = r / (r + mu)
                cases.append(nbinom.rvs(r, p, size=1)[0])
        return (
            pd.DataFrame({"n_cases": cases})
            .pipe(add_date_time_index_to_frame)
            .assign(timestep=list(range(1, length + 1)))
        )
