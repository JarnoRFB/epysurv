from abc import ABC, abstractmethod

import pandas as pd


class BaseSimulation(ABC):
    """An abstract class for a Poisson-based linear model for epidemic/endemic disease count simulation."""

    @abstractmethod
    def simulate(self, length: int, state_weight: float) -> pd.DataFrame:
        """An abstract method that starts the simulation based on the hyper parameter of the model."""
        pass
