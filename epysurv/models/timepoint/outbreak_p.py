from dataclasses import dataclass
from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import STSBasedAlgorithm

surveillance = importr('surveillance')


@dataclass
class OutbreakP(STSBasedAlgorithm):
    """
    Attributes
    ----------

    threshold
        The threshold value. Once the outbreak statistic is above this threshold an alarm is sounded.
    upperbound_statistic
        A string specifying the type of upperbound-statistic that is returned. With
        "cases" the number of cases that would have been necessary to produce
        an alarm (NNBA) or with "value" the outbreakP-statistic is computed.
    max_upperbound_cases
        Upperbound when numerically searching for NNBA. Default is 1e5.

    References
    ----------
    [1] Frisén, M., Andersson and Schiöler, L., (2009), Robust outbreak surveillance of epidemics in Sweden, Statistics in Medicine, 28(3):476-493.
    [2] Frisén, M. and Andersson, E., (2009) Semiparametric Surveillance of Monotonic Changes, Sequential Analysis 28(4):434-454.
    """
    threshold: int = 100
    upperbound_statistic: str = 'cases'
    max_upperbound_cases: int = 100_000

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(range=detection_range,
                         k=self.threshold,
                         ret=self.upperbound_statistic,
                         maxUpperboundCases=self.max_upperbound_cases)
        surv = surveillance.outbreakP(sts, control=control)
        return surv
