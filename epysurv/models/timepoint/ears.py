from dataclasses import dataclass
from typing import ClassVar

from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import STSBasedAlgorithm

surveillance = importr("surveillance")


@dataclass
class _EarsBase(STSBasedAlgorithm):
    """Base class for the Ears models."""

    alpha: float = 0.001
    baseline: int = 7
    min_sigma: float = 0

    method: ClassVar[str] = ""

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(
            range=detection_range,
            method=self.method,
            baseline=self.baseline,
            minSigma=self.min_sigma,
            alpha=self.alpha,
        )
        surv = surveillance.earsC(sts, control=control)
        return surv


class EarsC1(_EarsBase):
    """Computes a threshold for the number of counts based on values from the recent past.

    This is then compared to the observed number of counts. If the observation is above
    a specific quantile of the prediction interval, then an alarm is raised.
    This method is especially useful for data without many
    historic values, since it only needs counts from the recent past.

    Attributes
    ----------
    alpha
        An approximate (two-sided)(1 − α) prediction interval is calculated.
    baseline
        How many time points to use for calculating the baseline.
    min_sigma
        If minSigma is higher than 0, the quantity zAlpha * minSigma is then the alerting threshold if the baseline is zero.

    References
    ----------
    .. [1] Fricker, R.D., Hegler, B.L, and Dunfee, D.A. (2008). Comparing syndromic surveillance detection
        methods: EARS versus a CUSUM-based methodology, 27:3407-3429, Statistics in medicine.
    .. [2] Salmon, M., Schumacher, D. and Höhle, M. (2016): Monitoring count time series in R: Aberration
        detection in public health surveillance. Journal of Statistical Software, 70 (10), 1-35. doi: 10.18637/jss.v070.i10
    """

    method = "C1"


class EarsC2(_EarsBase):
    """Computes a threshold for the number of counts based on values from the recent past.

    This is then compared to the observed number of counts. If the observation is above
    a specific quantile of the prediction interval, then an alarm is raised.
    This method is especially useful for data without many
    historic values, since it only needs counts from the recent past.

    Attributes
    ----------
    alpha
        An approximate (two-sided)(1 − α) prediction interval is calculated.
    baseline
        How many time points to use for calculating the baseline.
    min_sigma
        If minSigma is higher than 0, zAlpha * minSigma is then the alerting threshold if the baseline is zero.

    References
    ----------
    .. [1] Fricker, R.D., Hegler, B.L, and Dunfee, D.A. (2008). Comparing syndromic surveillance detection
        methods: EARS versus a CUSUM-based methodology, 27:3407-3429, Statistics in medicine.
    .. [2] Salmon, M., Schumacher, D. and Höhle, M. (2016): Monitoring count time series in R: Aberration
        detection in public health surveillance. Journal of Statistical Software, 70 (10), 1-35. doi: 10.18637/jss.v070.i10
    """

    method = "C2"


@dataclass
class EarsC3(_EarsBase):
    """The EarsC3 model.

    Computes a threshold for the number of counts based on values from the recent past. This is then
    compared to the observed number of counts. If the observation is above a specific quantile of the
    prediction interval, then an alarm is raised. This method is especially useful for data without many
    historic values, since it only needs counts from the recent past.

    Attributes
    ----------
    alpha
        An approximate (two-sided)(1 − α) prediction interval is calculated.
    baseline
        How many time points to use for calculating the baseline.


    References
    ----------
    .. [1] Fricker, R.D., Hegler, B.L, and Dunfee, D.A. (2008). Comparing syndromic surveillance detection
        methods: EARS versus a CUSUM-based methodology, 27:3407-3429, Statistics in medicine.
    .. [2] Salmon, M., Schumacher, D. and Höhle, M. (2016): Monitoring count time series in R: Aberration
        detection in public health surveillance. Journal of Statistical Software, 70 (10), 1-35. doi: 10.18637/jss.v070.i10
    """

    alpha: float = 0.001
    baseline: int = 7

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(
            range=detection_range,
            method="C3",
            baseline=self.baseline,
            minSigma=self.min_sigma,
            alpha=self.alpha,
        )
        surv = surveillance.earsC(sts, control=control)
        return surv
