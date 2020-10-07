User  Guide
===========

Using ``epysurv`` models should be straightforward if you
are familiar with ``scikit-learn`` and ``pandas``.

Data Format
-----------

Let's first consider the models in the
:ref:`timepoint-model-api-doc`. 
Each model has a ``fit`` and a ``predict``
method that takes a ``pandas.DataFrame`` representing an
epidemiological count time series of the following form:

.. code-block:: python

                n_cases  n_outbreak_cases
    2004-01-05        0                 0
    2004-01-12        0                 0
    2004-01-19        2                 0
    2004-01-26        2                 0
    2004-02-02        1                 0


The data frame needs to have a regular ``DatetimeIndex`` and
two columns containing case counts. ``n_cases`` represents the
total number of cases observed and ``n_outbreak_cases`` the number
of cases are labeled as belonging to an outbreak. Therefore
``n_cases`` should always be bigger or equal to ``n_outbreak_cases``
as there can not be more outbreak cases as cases in total.
Note also that each row represents the number of cases
observed in the **period** between the row's timepoint and the
next timepoint. So in the above example the first row denotes
that there were zero cases observed from 2004-01-05 up to
2004-01-11 inclusive.

Fitting
-------

When passing the data frame to ``fit`` the outbreak cases are
subtracted from the total cases to obtain the *in control*
time series, i.e. the time series without outbreaks.

If you do not have any labeled outbreak data, but just the raw
counts, the ``n_cases`` column will be taken as is
under the assumption that your data is in fact
*in control* data. A warning is still issued in this case.

Prediction
----------
At prediction time only the total case counts are required.
The data frame passed to ``predict`` needs to consist
of observations that are spaced at the same regular time intervals
as the training data. All data points should lie strictly
in the future of the training data. The data frame returned
is the original data augmented by an ``alarm`` column that
indicated whether the model predicts an outbreak at that time
point or not.

.. code-block:: python

               n_cases  alarm
    2011-01-03        1    0.0
    2011-01-10        0    0.0
    2011-01-17        3    0.0
    2011-01-24        3    0.0
    2011-01-31        3    0.0


Using Time Series Classification Models
---------------------------------------
For each each model in the :ref:`timepoint-model-api-doc` there
is a corresponding model in the :ref:`timeseries-model-api-doc`.
These models basically perform the same task, but make a binary
prediction (alarm / no alarm) for an entire time series instead of
just a single time point. See :ref:`time-series-classification-formalization`
for a more detailed discussion. Therefore, bot ``fit`` and
``predict`` take iterables of data frames described above and labels:
``Iterable[Tuple[DataFrame, bool]]``. The label indicates whether
the last time point of the time series is to be considered an outbreak.
The ``predict`` method in this case only returns a time series of alarms.

Simulating Epidemiological Data
-------------------------------
Epysurv provides the methods to simulate endemic timeseries, using 
the ``SeasonalNoisePoisson`` and ``SeasonalNoiseNegativeBinomial`` and 
epidemic timeseries, using the ``PointSource`` class. All simulations 
can be tuned to simulate different seasonality, trends, and other 
characteristics during instantiation. Every simulation needs to implement 
the ``simulate`` method that at least takes a `length` parameter that 
determines how many observation should be simulated. Additionally, if the 
timeseries is supposed to be epidemic, we can define the ``state``, i.e., a sequence of 
equal length to the amount of simulations that encodes outbreaks. A ``1`` in the 
``state`` sequence indicates an outbreak and ``0`` otherwise. This is also shown in the
`quick tour <demo.ipynb>`_. Optionally, we can run a
Markov chain to randomly generate states where its transition probabilities can be adjusted.. 


