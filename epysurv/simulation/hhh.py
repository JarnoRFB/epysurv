import rpy2.robjects.packages as rpackages
import pandas as pd

from types import MappingProxyType
from rpy2.robjects import r
from rpy2 import robjects

surveillance = rpackages.importr("surveillance")
default_config = {
    "coefs": {
        "alpha": 1,
        "gamma": 0,
        "delta": 0,
        "lambda": 0,
        "phi": robjects.NULL,
        "psi": robjects.NULL,
        "period": 52,
    },
    "neighbourhood": robjects.NULL,
    "population": robjects.NULL,
    "start": robjects.NULL,
}
DEFAULTS = MappingProxyType(default_config)


def simulate_outbreaks(length, control: dict = DEFAULTS, model=robjects.NULL):
    """Simulates a multivariate time series of counts based on the Poisson/Negative Binomial model as
    described in Held et al. (2005).

    Attributes
    ----------
    control
        coef
            list with the following parameters of the model - if not specified, those parameters are omitted
            alpha
                vector of length m with intercepts for m units or geographic areas respectively
            gamma
                vector with parameters for the "sine" part of :math:`v_{i,t}`
            delta
                vector with parameters for the "cosine" part of :math:`v_{i,t}`
            lambda
                autoregressive parameter
            phi
                autoregressive parameter for adjacent units
            psi
                overdispersion parameter of the negative binomial model; NULL corresponds to a Poisson model
            period
                period of the seasonal component, defaults to 52 for weekly data
        neighbourhood
            neighbourhood matrix of size m×m with element 1 if two units are adjacent;
            the default NULL assumes that there are no neighbours
        population
            matrix with population proportions; the default NULL sets :math:`n_{i,t}=1`
        start
            if NULL, he means of the endemic part in the m units is used as initial values :math:`v_{i,0}`
    model
        Result of a model fit with algo.hhh (not implemented in epysurv), the estimated parameters are used to simulate data
    length
        number of times points to simulate

    Returns
    -------
    object
    """
    control = r.list(
        coefs=r.list(
            alpha=control["coefs"]["alpha"],
            gamma=control["coefs"]["gamma"],
            delta=control["coefs"]["delta"],
            lambda_=control["coefs"]["lambda"],
            phi=control["coefs"]["phi"],
            psi=control["coefs"]["psi"],
            period=control["coefs"]["period"],
        ),
        neighbourhood=control["neighbourhood"],
        population=control["population"],
        start=control["start"],
    )
    simulated = surveillance.simHHH(model=model, control=control, length=length)
    simulated = dict(zip(simulated.names, list(simulated)))
    return pd.DataFrame(
        {"mean": list(simulated["mean"]), "endemic": list(simulated["endemic"])}
    )
