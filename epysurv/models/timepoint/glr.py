"""Count data regression charts for the monitoring of surveillance time series.

Method as proposed by Höhle and Paul (2008).
The implementation is described in Salmon et al. (2016).
"""
from dataclasses import dataclass
from typing import Tuple, Union

from rpy2 import robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import STSBasedAlgorithm

surveillance = importr("surveillance")


@dataclass
class GLRNegativeBinomial(STSBasedAlgorithm):
    """
    Generalized likelihood ratio algorithm using negative binomial distribution.

    Attributes
    ----------
    alpha
        The (known) dispersion parameter of the negative binomial distribution,
        i.e. the parametrization of the negative binomial is such that the variance
        is mean + alpha ∗ mean2. Note: This parametrization is the inverse of
        the shape parametrization used in R – for example in dnbinom and glr.nb.
        Hence, if alpha=0 then the negative binomial distribution boils down to
        the Poisson distribution and a call of algo.glrnb is equivalent to a call to
        algo.glrpois. If alpha=NULL the parameter is calculated as part of the
        in-control estimation. However, the parameter is estimated only once from
        the first fit. Subsequent fittings are only for the parameters of the linear
        predictor with alpha fixed.
    glr_test_threshold
        Threshold in the GLR test, i.e. cγ.
    m
        Number of time instances back in time in the window-limited approach, i.e. the last value considered is max(1, n − m).
        To always look back until the first observation use -1.
    change
        A string specifying the type of the alternative. The two choices are "intercept" and "epi".
    direction
        Specifying the direction of testing in GLR scheme.
        - ("inc",) only increases in x are considered in the GLR-statistic
        - ("dec",) only decreases are regarded
        - ("inc", "dec") both increases and decreases are regarded.
    upperbound_statistic
        A string specifying the type of upperbound-statistic that is returned.
        With "cases" the number of cases that would have been necessary
        to produce an alarm or with "value" the GLR-statistic is computed.
    x_max
        Maximum value to try for x to see if this is the upperbound number of cases before sounding an alarm (Default: 1e4).
        This only applies only when ``upperbound_statistic == "cases"``.

    References
    ----------
    .. [1] Höhle, M. and Paul, M. (2008): Count data regression charts for the monitoring of surveillance time
        series. Computational Statistics and Data Analysis, 52 (9), 4357-4368.
    .. [2] Salmon, M., Schumacher, D. and Höhle, M. (2016): Monitoring count time series in R: Aberration
        detection in public health surveillance. Journal of Statistical Software, 70 (10), 1-35.
        doi: 10.18637/jss.v070.i10
    """

    alpha: float = 0
    glr_test_threshold: int = 5
    m: int = -1
    change: str = "intercept"
    direction: Union[Tuple[str, str], Tuple[str]] = ("inc", "dec")
    upperbound_statistic: str = "cases"
    x_max: float = 1e4

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(
            **{
                "range": detection_range,
                "c.ARL": self.glr_test_threshold,
                "m0": robjects.NULL,
                "alpha": self.alpha,
                # Mtilde is set to 1, since that is the only valid value for "epi" and "intercept"
                "Mtilde": 1,
                "M": self.m,
                "change": self.change,
                "theta": robjects.NULL,
                "dir": r.c(*self.direction),
                "ret": self.upperbound_statistic,
                "xMax": self.x_max,
            }
        )

        surv = surveillance.glrnb(sts, control=control)
        return surv


@dataclass
class GLRPoisson(STSBasedAlgorithm):
    """Generalized likelihood ratio algorithm using Poisson distribution.

    Attributes
    ----------
    glr_test_threshold
        Threshold in the GLR test, i.e. cγ.
    m
        Number of time instances back in time in the window-limited approach, i.e. the last value considered is max(1, n − m).
        To always look back until the first observation use -1.
    change
        A string specifying the type of the alternative. The two choices are "intercept" and "epi".
    direction
        Specifying the direction of testing in GLR scheme.
        - ("inc",) only increases in x are considered in the GLR-statistic
        - ("dec",) only decreases are regarded
        - ("inc", "dec") both increases and decreases are regarded.
    upperbound_statistic
        a string specifying the type of upperbound-statistic that is returned.
        With "cases" the number of cases that would have been necessary
        to produce an alarm or with "value" the GLR-statistic is computed.

    References
    ----------
    .. [1] Höhle, M. and Paul, M. (2008): Count data regression charts for the monitoring of surveillance time
        series. Computational Statistics and Data Analysis, 52 (9), 4357-4368.
    .. [2] Salmon, M., Schumacher, D. and Höhle, M. (2016): Monitoring count time series in R: Aberration
        detection in public health surveillance. Journal of Statistical Software, 70 (10), 1-35.
        doi: 10.18637/jss.v070.i10
    """

    glr_test_threshold: int = 5
    """threshold in the GLR test, i.e. cγ."""
    m: int = -1
    """number of time instances back in time in the window-limited approach, i.e. the last value considered is max 1, n − M. To always look back until the first observation use M=-1."""
    change: str = "intercept"
    """a string specifying the type of the alternative. Currently the two choices are intercept and epi. See the SFB Discussion Paper 500 for details"""
    direction: Union[Tuple[str, str], Tuple[str]] = ("inc", "dec")
    """Specifying the direction of testing in GLR scheme. With "inc" only increases in x are considered in the GLR-statistic, with "dec" decreases are regarded."""
    upperbound_statistic: str = "cases"
    """a string specifying the type of upperbound-statistic that is returned. With "cases" the number of cases that would have been necessary to produce an alarm or with "value" the GLR-statistic is computed (see below)"""

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(
            **{
                "range": detection_range,
                "c.ARL": self.glr_test_threshold,
                "m0": robjects.NULL,
                # Mtilde is set to 1, since that is the only valid value for "epi" and "intercept"
                "Mtilde": 1,
                "M": self.m,
                "change": self.change,
                # Role of theta: If NULL then the GLR scheme is used. If not NULL the prespecified value for κ or λ is used in a recursive LR scheme, which is faster."""
                "theta": robjects.NULL,
                "dir": r.c(*self.direction),
                "ret": self.upperbound_statistic,
            }
        )

        surv = surveillance.glrpois(sts, control=control)
        return surv
