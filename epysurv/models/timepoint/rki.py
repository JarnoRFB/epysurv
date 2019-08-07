from dataclasses import dataclass

from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import STSBasedAlgorithm

surveillance = importr("surveillance")


@dataclass
class RKI(STSBasedAlgorithm):
    """The old algorithm from the Robert Koch Institute.

    Attributes
    ----------
    years_back
        How many years back in time to include when forming the base counts.
    window_half_width
        Number of weeks to include before and after the current week in each year.
    include_recent_year
        Is a boolean to decide if the year of timePoint also contributes w reference values.
    """

    years_back: int = 0
    window_half_width: int = 6
    include_recent_year: bool = True

    def _call_surveillance_algo(self, sts, detection_range):
        control = r.list(
            range=detection_range, b=self.years_back, w=self.window_half_width, actY=self.include_recent_year
        )

        surv = surveillance.rki(sts, control=control)
        return surv
