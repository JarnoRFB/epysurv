from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd


class BasePoissonModel(ABC):
    """An abstract class for a Poisson-based linear model for epidemic/endemic disease count simulation"""

    @abstractmethod
    def __init__(
        self,
        alpha: float,
        amplitude: float,
        beta: float,
        frequency: int,
        phi: int,
        seed: Optional[int],
    ) -> None:
        self.alpha = alpha
        self.amplitude = amplitude
        self.beta = beta
        self.frequency = frequency
        self.phi = phi
        self.seed = seed

    @abstractmethod
    def simulate(self, length: int, state_weight: float) -> pd.DataFrame:
        """An abstract method that starts the simulation based on the hyper parameter of the model."""
        pass
