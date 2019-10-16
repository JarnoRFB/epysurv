import random
from typing import Set

import numpy as np
import pandas as pd
from scipy import stats


def get_outbreak_begins(n: int, outbreak_length: int, n_outbreaks: int) -> Set[int]:
    possible_outbreaks_starts = set(range(outbreak_length, n - outbreak_length - 1))
    outbreaks_starts = set()

    for _ in range(n_outbreaks):
        start = random.choice(tuple(possible_outbreaks_starts))
        outbreaks_starts.add(start)
        for i in range(start - outbreak_length, start + outbreak_length * 2):
            try:
                possible_outbreaks_starts.remove(i)
            except KeyError:
                continue
    return outbreaks_starts


def simulate_outbreaks(
    n: int = 104,
    outbreak_length: int = 5,
    n_outbreaks: int = 3,
    mu: float = 1,
    outbreak_mu: float = 10,
) -> pd.DataFrame:
    """Simulate outbreaks based on Poisson distribution.

    Parameters
    ----------
    n
        Number of weeks.
    outbreak_length
        Number of weeks each outbreak is long.
    n_outbreaks
        Number of outbreaks.
    mu
        Mean for the baseline.
    outbreak_mu
        Mean for the outbreaks.

    Returns
    -------
        Simulated case counts per week, separated into baseline and outbreak cases.
    """
    baseline = stats.poisson.rvs(mu=mu, size=n)
    n_outbreak_cases = np.zeros_like(baseline)
    n_cases = baseline.copy()

    outbreaks_starts = get_outbreak_begins(n, outbreak_length, n_outbreaks)

    for start in outbreaks_starts:
        outbreak_cases = stats.poisson.rvs(mu=outbreak_mu, size=outbreak_length)
        outbreak_cases += (
            outbreak_cases == 0
        )  # Ensure that there is a least on case during the outbreak.
        n_cases[start : start + outbreak_length] += outbreak_cases
        n_outbreak_cases[start : start + outbreak_length] = outbreak_cases

    data = pd.DataFrame(
        {
            "n_cases": n_cases,
            "n_outbreak_cases": n_outbreak_cases,
            "outbreak": n_outbreak_cases > 0,
            "baseline": baseline,
        },
        index=pd.date_range(start="2020", periods=baseline.size, freq="W-MON"),
    )

    data.index.name = "date"
    return data
