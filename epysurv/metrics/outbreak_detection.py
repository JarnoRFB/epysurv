import numpy as np
import pandas as pd


def ghozzi_score(prediction_result: pd.DataFrame) -> float:
    """Evalutes the performance of an outbreak detection using the following formula:
    sum(p[t] * c[t] - (1 - p[t]) * c[t] - (p[t] != o[t]) * mean(c) for t in timeseries) / sum(c)
    p: alarm
    c: count of outbreak cases
    o: outbreak

    Parameters
    ----------
    prediction_result
        Dataframe containing the columns "alarm", "outbreak" and "outbreak_cases"

    Returns
    -------
    A maximum score of 1.
    """
    # Outbreaks that were correctly predicted.
    weighted_true_positives = np.sum(
        prediction_result.alarm * prediction_result.outbreak * prediction_result.n_outbreak_cases
    )
    # Outbreaks that were missed.
    weighted_false_negatives = np.sum(
        (1 - prediction_result.alarm) * prediction_result.outbreak * prediction_result.n_outbreak_cases
    )
    # Alarms that were falsely raised.
    weighted_false_positives = np.sum(
        prediction_result.alarm
        * (prediction_result.outbreak != prediction_result.alarm)
        * np.mean(prediction_result.query("outbreak").n_outbreak_cases)
    )
    absolute_score = weighted_true_positives - weighted_false_negatives - weighted_false_positives
    normalized_score = absolute_score / prediction_result.n_outbreak_cases.sum()
    return normalized_score


def ghozzi_case_score(prediction_result: pd.DataFrame) -> float:
    """Evalutes the performance of an outbreak detection using the following formula:
    sum(p[t] * c[t] - (1 - p[t]) * c[t] - (p[t] != o[t]) * e[t] for t in timeseries) / sum(c)
    p: alarm
    c: count of outbreak cases
    o: outbreak
    e: endemic cases

    Parameters
    ----------
    prediction_result
        Dataframe containing the columns "alarm", "outbreak" and "outbreak_cases"

    Returns
    -------
    A maximum score of 1.
    """
    # Outbreaks that were correctly predicted.
    weighted_true_positives = np.sum(
        prediction_result.alarm * prediction_result.outbreak * prediction_result.n_outbreak_cases
    )
    # Outbreaks that were missed.
    weighted_false_negatives = np.sum(
        (1 - prediction_result.alarm) * prediction_result.outbreak * prediction_result.n_outbreak_cases
    )
    # Alarms that were falsely raised.
    weighted_false_positives = np.sum(
        prediction_result.alarm * (prediction_result.outbreak != prediction_result.alarm) * prediction_result.n_cases
    )
    absolute_score = weighted_true_positives - weighted_false_negatives - weighted_false_positives
    normalized_score = absolute_score / prediction_result.n_outbreak_cases.sum()
    return normalized_score
