Outbreak Detection
==================
Surveillance algorithms usually work on regular spaced aggregated time series of case counts.
Let :math:`\mathbf{x} = (x_1, \dots x_T)` be such a time series with entries at regularly spaced,
discrete timepoints :math:`t`.
An entry :math:`x_t` of that time series is defined as the number of observed case
counts in that time period.

Time Point Classification
-------------------------

Based on this we can view the problem as a *sequential supervised learning problem*
:cite:`Dietterich2002`, in which
the sequence of counts is paired with a sequence of outbreak labels :math:`(\mathbf{x}, \mathbf{y})`, with
:math:`\mathbf{x} = (x_1, \dotsc, x_T), x_i \in \mathbb{N}_0\) and \(y_i \in \mathbb{B}`. For each
timepoint :math:`t` a boolean label is assigned, corresponding to whether there were outbreak cases
present in the aggregation
time interval. We call this problem *time point classification*. This is the standard
formulation of common surveillance algorithms.


.. _time-series-classification-formalization:

Time Series Classification
--------------------------

The time point formulation can be extended into a time series formulation by dividing the time series :math:`\mathbf{x}`
into smaller time series and assigning the label of the last time point to the whole time series. Thus
a data set :math:`\{(\mathbf{x}_j, y_j)\}_{j=1}^T` is obtained. This formulation is especially useful for incorporating
reporting delay. That means that the information at time point :math:`t = j` can be quite different
depending on whether :math:`j` is relatively recent, e.g. :math:`j = T` or already some time in the past. This
is due to the fact that information arrives sometimes slowly in epidemiological surveillance systems.
We call this problem formulation *time series classification*.

Models
------
As of now all models included in ``epysurv`` work on univariate time series of
counts. Extensions to multivariate time series and incorporation of spatial
data exist in the ``R surveillance package``, but their inclusion is only
planned for later releases.

The currently included models can be viewed as semi-supervised
techniques from a machine learning or anomaly detection perspective :cite:`Chandola2009a`.
All models fit historic data, assuming that they represent the normal state of the system.
Having fitted the data, an estimate for the case counts of the current week is computed.
This estimate is compared to the number of cases reported in the current
If the observed case count exceeds the expected number by some threshold,
an alarm is raised. Most models in fact compute a predictive distribution for the
estimated number of case counts and raise an alarm if the actual number exceeds a
certain quantile of this distribution.

Window-based Approaches 
^^^^^^^^^^^^^^^^^^^^^^^
The simplest form of outbreak detection algorithms are window-based
approaches. For them the expectation for the current week is computed
from a moving window of fixed size. For example the ``EarsC1``
algorithm, computes its predictive distribution based the mean and
standard deviation of the last seven timepoints, using a normal distribution.

Because of the short time interval considered, these approaches are naturally
insensitive against seasonality and trend. However, recent outbreaks can
contaminate the data, reducing the sensitivity of the algorithms.

This category includes the Ears-family :cite:`Hutwagner2003`,
CDC :cite:`Stroup1989a` and the RKI :cite:`Salmon2014` algorithm.

GLM-based Approaches 
^^^^^^^^^^^^^^^^^^^^
Approaches based on Generalized Linear Models (GLMs) form a popular
group of outbreak detection algorithms. They compute a predictive distribution for
the current week based on fitting a GLM to previous data. An alarm is raised
if the current observation is unlikely under the predictive distribution
controlled by some $\alpha$ value.
Often Poisson or Negative Binomial models are used to do justice to
the count nature of the data. Moreover, terms to accommodate seasonality
and trend are often incorporated as well. GLM-based approaches included
the classical Farrington algorithm :cite:`Farrington1996` and its more
recent extension :cite:`Noufaily2012`.

Cusum-based Approaches
^^^^^^^^^^^^^^^^^^^^^^
Both window-based and GLM approaches have the downside that they
only incorporate evidence from the current week. Larger outbreaks
that build up slowly could therefore easily be missed. Cusum-based approaches
are inspired by models from statistical process control~\cite{Oakland2007}
and incorporate evidence from previous timepoints. Instead of computing a predictive
distribution, evidence that observed case counts do originate from an epidemic is accumulated
until a certain threshold is exceeded and an alarm is raised. Then the sum
is reset.

Cusum-based approaches include the Cusum :cite:`Rossi1999`,
generalized likelihood ratio methods based on Poisson:cite:`Hohle2006`
or negative binomial distributions~\cite{Hohle2008} and
the OutbreakP method :cite:`Frisen2009`.

.. bibliography:: refs.bib
