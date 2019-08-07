from dataclasses import dataclass

from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import STSBasedAlgorithm

surveillance = importr("surveillance")


@dataclass
class Bayes(STSBasedAlgorithm):
    """
    Evaluation of timepoints with the Bayes subsystem.

    Attributes
    ----------
    years_back
        How many years back in time to include when forming the base counts.
    window_half_width
        Number of weeks to include before and after the current week in each year.
    include_recent_year
        is a boolean to decide if the year of timePoint also contributes w reference values.
    alpha
        The parameter alpha is the (1 − α)-quantile to use in order to calculate the upper threshold. As default b, w, actY are set for the Bayes 1 system with alpha=0.05.

    References
    ----------
    [1] Riebler, A. (2004), Empirischer Vergleich von statistischen Methoden zur Ausbruchserkennung bei
        Surveillance Daten, Bachelor’s thesis
    [2] Höhle, M., & Riebler, A. (2005). Höhle, Riebler: The R-Package “surveillance.” Sonderforschungsbereich (Vol. 386). Retrieved from https://epub.ub.uni-muenchen.de/1791/1/paper_422.pdf
    """

    years_back: int = 0
    window_half_width: int = 6
    include_recent_year: bool = True
    alpha: float = 0.05

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(
            range=detection_range,
            b=self.years_back,
            w=self.window_half_width,
            actY=self.include_recent_year,
            alpha=self.alpha,
        )

        surv = surveillance.bayes(sts, control=control)
        return surv
