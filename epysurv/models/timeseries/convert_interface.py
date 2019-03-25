"""Put a timeseries interface in front of all timepoint algorithms."""
# type: ignore
from .. import timepoint
from ._base import NonLearningTimeseriesClassificationMixin

__all__ = []
for name, obj in vars(timepoint).items():
    try:
        if issubclass(obj, timepoint._base.TimepointSurveillanceAlgorithm):
            globals()[name] = type(name, (NonLearningTimeseriesClassificationMixin, obj), {})
            __all__.append(name)
    except TypeError:
        continue

# print(__all__)

