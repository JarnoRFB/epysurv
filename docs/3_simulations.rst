Simulations 
==================
While infection counts are often available in at least an aggregated fashion, details on outbreaks are less often available outside of health authorities. For example, Germany's federal health authority - the `Robert Koch Institute <https://www.rki.de/DE/Content/Infekt/SurvStat/survstat_node.html>`_ - shares aggregated infection counts but no systematic information on outbreak events. Additionally, details on outbreaks are often not known like the onset of an outbreak :cite:`Yuan2019`.Hence, simulating infection counts and outbreak is a valid alternative to using real data. Epysurv includes a module that allows you to simulate simple, univariate endemic and epidemic timeseries, i.e., with and without outbreak to test and develop outbreak detection algorithms.

Endemic Timeseries
------------------
An endemic timeseries is an timeseries of case counts (as defined in :ref:`outbreak-detection-formalization`.) that occurs naturally and varies between diseases, time, space, sex, age, and other dimensions. The important distinction is that there is no influence in the observed case counts due to an outbreak event.

A simulation is usually a time-dependent, linear model that produces realistic case counts and can be set to mimic different types of disease dynamics. To achieve realism in epidemiological simulations, you would usually incorporate different effects into that model such as seasonality and trend e.g., a repetition of a certain pattern after one year with increasing case numbers over time. Finally, some distribution is used to make the outcome of the model non-deterministic. Since case counts are positive integers, a Poisson or negative binomial distribution is used on top of the linear model to introduce some randomness in the observed case counts. These kinds of algorithms are referred to as ``seasonal_noise``. 

Epidemic Timeseries
-------------------
Once we have created a model to simulate an endemic timeseries, we can introduce outbreak events by randomly increasing the case count at certain timepoints :math:`t`. A common approach is to have a chain of switching states (usually produces by a Markov chain) that use sensible transition probabilities to move into or leave the state of an outbreak.  Alternatively, one can assign certain timepoints to be in an outbreak to make such timeseries more comparable or tests edge cases of outbreak detection algorithms.

In practice, the model for the simulation of endemic timeseries is extended by a term that is dependent on the current outbreak state. If there is not outbreak, the term is ignored otherwise a fixed term is added to the endemic case counts.