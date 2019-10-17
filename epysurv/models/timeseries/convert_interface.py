"""Put a timeseries interface in front of all timepoint algorithms."""
from ..timepoint import (
    CDC,
    HMM,
    RKI,
    Bayes,
    Boda,
    Cusum,
    EarsC1,
    EarsC2,
    Farrington,
    FarringtonFlexible,
    GLRNegativeBinomial,
    GLRPoisson,
    OutbreakP,
)
from ._base import NonLearningTimeseriesClassificationMixin


class Bayes(NonLearningTimeseriesClassificationMixin, Bayes):
    pass


class Boda(NonLearningTimeseriesClassificationMixin, Boda):
    pass


class CDC(NonLearningTimeseriesClassificationMixin, CDC):
    pass


class Cusum(NonLearningTimeseriesClassificationMixin, Cusum):
    pass


class EarsC1(NonLearningTimeseriesClassificationMixin, EarsC1):
    pass


class EarsC2(NonLearningTimeseriesClassificationMixin, EarsC2):
    pass


class Farrington(NonLearningTimeseriesClassificationMixin, Farrington):
    pass


class FarringtonFlexible(NonLearningTimeseriesClassificationMixin, FarringtonFlexible):
    pass


class GLRNegativeBinomial(
    NonLearningTimeseriesClassificationMixin, GLRNegativeBinomial
):
    pass


class GLRPoisson(NonLearningTimeseriesClassificationMixin, GLRPoisson):
    pass


class HMM(NonLearningTimeseriesClassificationMixin, HMM):
    pass


class OutbreakP(NonLearningTimeseriesClassificationMixin, OutbreakP):
    pass


class RKI(NonLearningTimeseriesClassificationMixin, RKI):
    pass
