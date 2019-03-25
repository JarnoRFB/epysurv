from dataclasses import dataclass
from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import DisProgBasedAlgorithm

surveillance = importr('surveillance')


@dataclass
class CDC(DisProgBasedAlgorithm):
    """
    Attributes
    ----------
    years_back
        How many years back in time to include when forming the base counts.
    window_half_width
        Number of weeks to include before and after the current week in each year.
    alpha
        An approximate (two-sided)(1 − α) prediction interval is calculated.
    References
    ----------
    [1] Stroup, D., G. Williamson, J. Herndon, and J. Karon (1989). Detection of aberrations in the occurence of
        notifiable diseases surveillance data. Statistics in Medicine 8, 323-329.
    [2] Farrington, C. and N. Andrews (2003). Monitoring the Health of Populations, Chapter Outbreak
        Detection: Application to Infectious Disease Surveillance, pp. 203-231. Oxford University Press.
    """
    years_back: int = 5
    window_half_width: int = 1
    alpha: float = 0.001

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(range=detection_range,
                         b=self.years_back,
                         m=self.window_half_width,
                         alpha=self.alpha)
        surv = surveillance.algo_cdc(sts, control=control)
        return surv
