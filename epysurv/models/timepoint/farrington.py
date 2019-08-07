from dataclasses import dataclass

from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import DisProgBasedAlgorithm, STSBasedAlgorithm

surveillance = importr("surveillance")


@dataclass
class Farrington(DisProgBasedAlgorithm):
    """
    The Farrington algorithm.

    For each time point uses a GLM to predict the number of counts according
    to the procedure by Farrington et al. (1996).
    This is then compared to the observed number of counts. If the observation is above a specific
    quantile of the prediction interval, then an alarm is raised.

    Attributes
    ----------
    years_back
        How many years back in time to include when forming the base counts.
    window_half_width
        Number of weeks to include before and after the current week in each year.
    reweight
        Boolean specifying whether to perform reweighting step.
    alpha
        An approximate (two-sided) (1 − α) prediction interval is calculated.
    trend
        Boolean indicating whether a trend should be included and kept in case the conditions
        in the Farrington et. al. paper are met (see the results). If false then no trend is fit.
    past_period_cutoff
        Periods considered for suppression of low case numbers.
    min_cases_in_past_periods
        The minimal number of cases in past periods such that an outbreak is considered.
    power_transform
        Power transformation to apply to the data if the threshold is to be computed with the method
        described in Farrington et al. (1996). Use either
        - "2/3" for skewness correction (Default)
        - "1/2" for variance stabilizing transformation
        - "none" for no transformation.

    References
    ----------
    [1] Farrington, C.P., Andrews, N.J, Beale A.D. and Catchpole, M.A. (1996): A statistical algorithm for
        the early detection of outbreaks of infectious disease. J. R. Statist. Soc. A, 159, 547-563.
    """

    years_back: int = 3
    window_half_width: int = 3
    reweight: bool = True
    alpha: float = 0.01
    trend: bool = True
    past_period_cutoff: int = 4
    min_cases_in_past_periods: int = 5
    power_transform: str = "2/3"

    def _call_surveillance_algo(self, disprog_obj, detection_range):
        control = r.list(
            range=detection_range,
            b=self.years_back,
            w=self.window_half_width,
            reweight=self.reweight,
            alpha=self.alpha,
            trend=self.trend,
            limit54=r.c(self.min_cases_in_past_periods, self.past_period_cutoff),
            powertrans=self.power_transform,
        )

        surv = surveillance.algo_farrington(disprog_obj, control=control)
        return surv


@dataclass
class FarringtonFlexible(STSBasedAlgorithm):
    """
    The extended Farrington algorithm.

    For each time point uses
    a Poisson GLM with overdispersion to predict an upper bound on the number of counts according
    to the procedure by Farrington et al. (1996) and by Noufaily et al. (2012). This bound is then
    compared to the observed number of counts. If the observation is above the bound, then an alarm is
    raised.

    Attributes
    ----------
    years_back
        How many years back in time to include when forming the base counts.
    window_half_width
        Number of weeks to include before and after the current week in each year.
    reweight
        Boolean specifying whether to perform reweighting step.
    weights_threshold
        Defines the threshold for reweighting past outbreaks using the Anscombe residuals (1 in the original method, 2.58 advised in the improved method).
    alpha
        An approximate (one-sided) (1 − α) · 100% prediction interval is calculated
        unlike the original method where it was a two-sided interval.
        The upper limit of this interval i.e. the (1 − α) · 100% quantile serves as an upperbound.
    trend
        Boolean indicating whether a trend should be included and kept in case
        the conditions in the Farrington et. al. paper are met (see the results).
        If false then NO trend is fit.
    trend_threshold
        Threshold for deciding whether to keep trend in the model (0.05 in the original method, 1 advised in the improved method).
    past_period_cutoff
        Periods considered for suppression of low case numbers.
    min_cases_in_past_periods
        The minimal number of cases in past periods such that an outbreak is considered.
        power_transform
        Power transformation to apply to the data if the threshold is to be computed with the method
        described in Farrington et al. (1996). Use either
        - "2/3" for skewness correction (Default)
        - "1/2" for variance stabilizing transformation
        - "none" for no transformation.
    past_weeks_not_included
        Number of past weeks to ignore in the calculation.
    threshold_method
        Method to be used to derive the upperbound. Options are
        - "delta" for the method described in Farrington et al. (1996)
        - "Noufaily" for the method described in Noufaily et al. (2012)
        - "muan" for the method extended from Noufaily et al. (2012)


    References
    ----------
    [1] Farrington, C.P., Andrews, N.J, Beale A.D. and Catchpole, M.A. (1996): A statistical algorithm for
        the early detection of outbreaks of infectious disease. J. R. Statist. Soc. A, 159, 547-563.
    [2] Noufaily, A., Enki, D.G., Farrington, C.P., Garthwaite, P., Andrews, N.J., Charlett, A. (2012): An
        improved algorithm for outbreak detection in multiple surveillance systems. Statistics in Medicine,
        32 (7), 1206-1222.
    [3] Salmon, M., Schumacher, D. and Höhle, M. (2016): Monitoring count time series in R: Aberration
        detection in public health surveillance. Journal of Statistical Software, 70 (10), 1-35. doi: 10.18637/jss.v070.i10
    """

    years_back: int = 3
    window_half_width: int = 3
    reweight: bool = True
    weights_threshold: float = 2.58
    alpha: float = 0.01
    trend: bool = True
    trend_threshold: float = 0.05
    past_period_cutoff: int = 4
    min_cases_in_past_periods: int = 5
    power_transform: str = "2/3"
    past_weeks_not_included: int = 26
    threshold_method: str = "delta"

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(
            range=detection_range,
            b=self.years_back,
            w=self.window_half_width,
            reweight=self.reweight,
            weightsThreshold=self.weights_threshold,
            alpha=self.alpha,
            trend=self.trend,
            trend_threshold=self.trend_threshold,
            limit54=r.c(self.min_cases_in_past_periods, self.past_period_cutoff),
            powertrans=self.power_transform,
            pastWeeksNotIncluded=self.past_weeks_not_included,
            thresholdMethod=self.threshold_method,
        )

        surv = surveillance.farringtonFlexible(sts, control=control)
        return surv
