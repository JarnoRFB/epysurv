import pandas as pd


def load_predictions(filepath):
    predictions = pd.read_csv(
        filepath, index_col=0, parse_dates=True, infer_datetime_format=True
    ).assign(alarm=lambda df: df["alarm"].astype(bool))
    freq = pd.infer_freq(predictions.index)
    return predictions.asfreq(freq)


def load_simulations(filepath):
    simulations = pd.read_csv(
        filepath, index_col=0, parse_dates=True, infer_datetime_format=True
    )
    freq = pd.infer_freq(simulations.index)
    return simulations.asfreq(freq)
