import pandas as pd


def load_predictions(filepath):
    predictions = pd.read_csv(
        filepath, index_col=0, parse_dates=True, infer_datetime_format=True
    ).assign(alarm=lambda df: df["alarm"].astype(bool))
    freq = pd.infer_freq(predictions.index)
    return predictions.asfreq(freq)


def load_simulations(filepath):
    simulations = pd.read_csv(
        filepath,
        index_col=0,
        parse_dates=True,
        infer_datetime_format=True,
        dtype={"n_cases": "int64"},
    )
    freq = pd.infer_freq(simulations.index)
    return simulations.asfreq(freq)


def drop_column_if_exists(df, column):
    if column in df.columns:
        df = df.drop(columns=column)
    return df
