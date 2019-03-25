from dataclasses import dataclass

from rpy2 import robjects
from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import STSBasedAlgorithm

surveillance = importr('surveillance')


@dataclass
class Boda(STSBasedAlgorithm):
    """
    Attributes
    ----------
    trend
        Boolean indicating whether a linear trend term should be included in the model for the expectation the log-scale
    season
        Boolean to indicate whether a cyclic spline should be included.
    prior
        Either of "iid", "rw1" or "rw2".
    alpha
        The threshold for declaring an observed count as an aberration is the (1 − α) · 100% quantile of the predictive posterior.
    mc_munu
    mc_y
        Number of samples of y to generate for each pair of the mean and size parameter. A total of mc.munu × mc.y samples are generated.
    sampling_method
        Should one sample from the parameters joint distribution (joint) or from their respective marginal posterior distribution (marginals)
    quantile_method
        Either of "MC" or "MM". Indicates how to compute the quantile
        based on the posterior distribution (no matter the inference method):
        either by sampling mc.munu values from the posterior distribution of the
        parameters and then for each sampled parameters vector sampling mc.y response
        values so that one gets a vector of response values based on which
        one computes an empirical quantile (MC method, as explained in Manitz
        and Höhle 2013); or by sampling mc_munu from the posterior distribution
        of the parameters and then compute the quantile of the mixture distribution
        using bisectioning, which is faster.
    """
    trend: bool = False
    season: bool = False
    prior: str = 'iid'
    alpha: float = 0.05
    mc_munu: int = 100
    mc_y: int = 10
    sampling_method = 'joint'
    quantile_method: str = 'MM'

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(**{'range': detection_range,
                            'X': robjects.NULL,
                            'trend': self.trend,
                            'season': self.season,
                            'prior': self.prior,
                            'alpha': self.alpha,
                            'mc.munu': self.mc_munu,
                            'mc.y': self.mc_y,
                            'samplingMethod': self.sampling_method,
                            'quantileMethod': self.quantile_method})
        surv = surveillance.boda(sts, control=control)
        return surv
