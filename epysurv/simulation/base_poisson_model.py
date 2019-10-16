from abc import abstractmethod, ABCMeta
from typing import Optional, Sequence


class BasePoissonModel(metaclass=ABCMeta):
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
    def simulate(self, length: int, state: Optional[Sequence[int]]) -> "pd.DataFrame":
        """An abstract method that starts the simulation based on the hyper parameter of the model."""
        pass
