from dataclasses import dataclass

from rpy2.robjects import r
from rpy2.robjects.packages import importr

from ._base import DisProgBasedAlgorithm

surveillance = importr("surveillance")


@dataclass
class HMM(DisProgBasedAlgorithm):
    """
    Hidden Markov model for outbreak detection.

    Attributes
    ----------
    n_observations
        number of observations back in time to use for fitting the HMM (including
        the current observation). Reasonable values are a multiple of observations per year,
        the default is -1, which means to use all possible values - for long
        series this might take very long time!
    n_hidden_states
        number of hidden states in the HMM – the typical choice is 2. The
        initial rates are set such that the noStates’th state is the one having the
        highest rate. In other words: this state is considered the outbreak state.
    trend
        The two choices are "intercept" and "epi".
    n_harmonics
        Number of harmonic waves to include in the linear predictor.
    equal_covariate_effects
        If set then all covariate effects parameters are equal for the states.

    References
    ----------
    [1] Y. Le Strat and F. Carrat, Monitoring Epidemiologic Surveillance Data using Hidden Markov Models (1999), Statistics in Medicine, 18, 3463–3478
    [2] I.L. MacDonald and W. Zucchini, Hidden Markov and Other Models for Discrete-valued Time
        Series, (1997), Chapman & Hall, Monographs on Statistics and applied Probability 70
    """

    n_observations: int = -1
    n_hidden_states: int = 2
    trend: bool = True
    n_harmonics: int = 1
    equal_covariate_effects: bool = False

    def _call_surveillance_algo(self, disprog_obj, detection_range):
        control = r.list(
            range=detection_range,
            Mtilde=self.n_observations,
            noStates=self.n_hidden_states,
            trend=self.trend,
            noHarmonics=self.n_harmonics,
            covEffectEqual=self.equal_covariate_effects,
        )
        surv = surveillance.algo_hmm(disprog_obj, control=control)
        return surv
