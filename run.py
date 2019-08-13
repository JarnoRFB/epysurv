import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters

from epysurv.models import timepoint

register_matplotlib_converters()


def read_surv_data(filename):
    data = pd.read_csv(
        filename, index_col=0, parse_dates=True, infer_datetime_format=True
    )
    data.index.freq = pd.infer_freq(data.index)
    return data


def plot_prediction(train_data, prediction):
    prediction = pd.concat((train_data, prediction), sort=False)
    fontsize = 20
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.step(
        x=prediction.index,
        y=prediction.n_cases,
        where="mid",
        color="blue",
        label="_nolegend_",
    )
    outbreaks = prediction.query("alarm == 1")
    ax.plot(outbreaks.index, outbreaks.n_cases, "r^", label="alarm", markersize=12)
    ax.set_xlabel("time", fontsize=fontsize)
    ax.set_ylabel("cases", fontsize=fontsize)
    ax.legend(fontsize="xx-large")


data_train = read_surv_data("tests/data/salmonella_train.csv")
data_test = read_surv_data("tests/data/salmonella_test.csv")

algos = [
    timepoint.EarsC1,
    timepoint.EarsC2,
    timepoint.EarsC3,
    # timepoint.Farrington,
    # timepoint.FarringtonFlexible,
    # timepoint.Cusum,
    # timepoint.Bayes,
    # timepoint.RKI,
    # timepoint.GLRNegativeBinomial,
    # timepoint.GLRPoisson,
    # timepoint.OutbreakP,
    # timepoint.CDC,
    # timepoint.HMM,
    # timepoint.Boda
]

for Algo in algos:
    model = Algo()
    model.fit(data_train)
    pred = model.predict(data_test)
    pred.to_csv(f"tests/data/{model.__class__.__name__}_pred.csv")
    plot_prediction(data_train, pred)
    plt.title(model.__class__.__name__)
    plt.show()
