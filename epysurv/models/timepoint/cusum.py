from dataclasses import dataclass
from typing import *

from rpy2 import robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import STSBasedAlgorithm

surveillance = importr("surveillance")


@dataclass
class Cusum(STSBasedAlgorithm):
    """
    Attributes
    ----------
    reference_value
    decision_boundary
    expected_numbers_method
        How to determine the expected number of cases – the following arguments are possible: {"glm", "mean"}.

        ``mean``
            Use the mean of all data points passed to ``fit``.
        ``glm``
            Fit a glm to the data ponts passed to ``fit``.
    transform
        One of the following transformations (warning: Anscombe and NegBin transformations are experimental)
        - standard standardized variables z1 (based on asymptotic normality) - This is the default.
        - rossi standardized variables z3 as proposed by Rossi
        - anscombe anscombe residuals – experimental
        - anscombe2nd anscombe residuals as in Pierce and Schafer (1986) based on 2nd order approximation of E(X) – experimental
        - pearsonNegBin compute Pearson residuals for NegBin – experimental
        - anscombeNegBin anscombe residuals for NegBin – experimental
        - ``"none"`` no transformation
    negbin_alpha
        Parameter of the negative binomial distribution, such that the variance is m + α ∗ m2.
    References
    ----------
    [1] G. Rossi, L. Lampugnani and M. Marchi (1999), An approximate CUSUM procedure for surveillance of health events, Statistics in Medicine, 18, 2111–2122
    [2] D. A. Pierce and D. W. Schafer (1986), Residuals in Generalized Linear Models, Journal of the
        American Statistical Association, 81, 977–986
    """

    reference_value: float = 1.04
    decision_boundary: float = 2.26
    expected_numbers_method: str = "mean"
    transform: str = "standard"
    negbin_alpha: float = 0.1

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(
            range=detection_range,
            k=self.reference_value,
            h=self.decision_boundary,
            m=robjects.NULL if self.expected_numbers_method == "mean" else self.expected_numbers_method,
            trans=self.transform,
            alpha=self.negbin_alpha,
        )
        surv = surveillance.cusum(sts, control=control)
        return surv
