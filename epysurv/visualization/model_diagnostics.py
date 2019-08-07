import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotnine as gg
import seaborn as sns


def plot_confusion_matrix(
    confusion_matrix: np.ndarray, class_names: list, ax: matplotlib.axes.Axes = None
) -> matplotlib.axes.Axes:
    """Plots a confusion matrix, as returned by sklearn.metrics.confusion_matrix, as a heatmap.

    Based on https://gist.github.com/shaypal5/94c53d765083101efc0240d776a23823

    Arguments
    ---------
    confusion_matrix
        The numpy.ndarray object returned from a call to sklearn.metrics.confusion_matrix.
        Similarly constructed ndarrays can also be used.
    class_names
        An ordered list of class names, in the order they index the given confusion matrix.
    figsize:
        A 2-long tuple, the first value determining the horizontal size of the ouputted figure,
        the second determining the vertical size. Defaults to (10,7).

    Returns
    -------

        The resulting confusion matrix figure
    """
    df_cm = pd.DataFrame(confusion_matrix, index=class_names, columns=class_names)
    if ax is None:
        fig, ax = plt.subplots()
    heatmap = sns.heatmap(df_cm, annot=True, cmap="Blues", ax=ax)
    heatmap.set(ylabel="True label", xlabel="Predicted label")

    return ax


def plot_prediction(train_data, test_data, prediction, ax: matplotlib.axes.Axes = None) -> matplotlib.axes.Axes:
    """Plots case counts as step line, with outbreaks and alarms indicated by triangles."""
    whole_data = pd.concat((train_data, test_data), sort=False)
    fontsize = 20
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
    ax.step(x=whole_data.index, y=whole_data.n_cases, where="mid", color="blue", label="_nolegend_")
    alarms = prediction.query("alarm == 1")
    ax.plot(alarms.index, [0] * len(alarms), "g^", label="alarm", markersize=12)
    outbreaks = test_data.query("outbreak")
    ax.plot(outbreaks.index, outbreaks.n_outbreak_cases, "rv", label="outbreak", markersize=12)
    ax.set_xlabel("time", fontsize=fontsize)
    ax.set_ylabel("cases", fontsize=fontsize)
    ax.legend(fontsize="xx-large")

    return ax


def ghozzi_score_plot(prediction_result: pd.DataFrame, filename: str):
    """Plots case counts and detector predictions with ghozzi weighting.

    Parameters
    ----------
    prediction_result
        DataFrame containing 'alarm', 'county', 'pathogen', 'n_cases', 'n_outbreak_cases', 'outbreak'.
    filename
        File name to write the plot to.
    """
    # Outbreaks that were recognized.
    prediction_result["weighted_true_positives"] = (
        prediction_result.alarm * prediction_result.outbreak * prediction_result.n_outbreak_cases
    )

    # Outbreaks that were missed.
    prediction_result["weighted_false_negatives"] = (
        (1 - prediction_result.alarm) * prediction_result.outbreak * prediction_result.n_outbreak_cases
    )
    # Alarms that were falsely raised.
    prediction_result["weighted_false_positives"] = (
        prediction_result.alarm
        * (prediction_result.outbreak != prediction_result.alarm)
        * np.mean(prediction_result.query("outbreak").n_outbreak_cases)
    )

    melted_prediction_result = (
        prediction_result.reset_index()
        .rename(columns={"index": "date"})
        .melt(
            id_vars=["date", "county", "pathogen", "n_cases", "n_outbreak_cases", "outbreak", "alarm"],
            var_name="prediction",
            value_name="weighting",
        )
    )

    case_color = "grey"
    n_cols = 4
    n_filter_combinations = len(prediction_result[["county", "pathogen"]].drop_duplicates())

    chart = (
        gg.ggplot(melted_prediction_result, gg.aes(x="date"))
        + gg.geom_bar(
            prediction_result, gg.aes(x="prediction_result.index", y="n_cases"), fill=case_color, stat="identity"
        )
        + gg.geom_line(gg.aes(y=0), color=case_color)
        + gg.geom_bar(gg.aes(y="weighting", fill="prediction"), stat="identity")
        + gg.facet_wrap(["county", "pathogen"], ncol=n_cols)
        + gg.scale_x_date(date_breaks="4 month", date_labels="%Y-%m")
        + gg.ylab("# cases")
        + gg.scale_fill_manual(name="weighting", values=["red", "orange", "green"])
        + gg.theme(panel_grid_minor=gg.element_blank())
        + gg.theme_light()
    )
    chart.save(filename, width=5 * n_cols, height=4 * n_filter_combinations / n_cols, unit="cm", limitsize=False)
