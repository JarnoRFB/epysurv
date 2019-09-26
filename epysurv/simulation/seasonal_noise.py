import rpy2.robjects.packages as rpackages
import pandas as pd

from rpy2 import robjects

surveillance = rpackages.importr("surveillance")


def simulate_outbreaks(
    length, A=1, alpha=1, beta=0, phi=0, frequency=1, state=robjects.NULL, K=0
):
    """Generation of a cyclic model of a Poisson distribution as background data for a simulated timevector.

    The mean of the Poisson distribution is modelled as:
    :math:`\\mu = \\exp{(A\\sin{(frequency \\cdot (t + \\phi))} + \\alpha + \\beta * t + L * state)}`

    Attributes
    ----------
    A
        amplitude (range of sinus), default = 1.
    alpha
        parameter to move along the y-axis (negative values not allowed) with alpha >
        = A, default = 1.
    beta
        regression coefficient, default = 0.
    phi
        factor to create seasonal moves (moves the curve along the x-axis), default = 0.
    length
        number of weeks to model.
    frequency
        factor to determine the oscillation-frequency, default = 1.
    state
        if a state chain is entered the outbreaks will be additional weighted by K
    K
        additional weight for an outbreak which influences the distribution parameter mu, default = 0.

    Returns
    -------
    pandas.DataFrame
    """
    simulated = surveillance.sim_seasonalNoise(
        A=A,
        alpha=alpha,
        beta=beta,
        phi=phi,
        length=length,
        frequency=frequency,
        state=state,
        K=K,
    )
    simulated = dict(zip(simulated.names, list(simulated)))
    print(simulated)
    return pd.DataFrame(
        {
            "t": list(simulated["t"]),
            "mu": list(simulated["mu"]),
            "seasonal_background": list(simulated["seasonalBackground"]),
        }
    )
