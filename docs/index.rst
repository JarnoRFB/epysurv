epysurv: Epidemiological Surveillance in Python
===============================================
``epysurv`` is a pythonic wrapper around the `R surveillance package <https://cran.r-project.org/web/packages/surveillance/index.html>`_.
It's main goal is to predict disease outbreaks, right
now focusing on univariate count time series.
``epsurv`` operates on pandas ``DataFrame``\s and strives to implement a `scikit-learn <https://scikit-learn.org/stable/>`_ like API.

``epysurv`` supports two problem formalizations of outbreak detection: time point classification and time series classification.

This documentation mainly explains the usage of ``epysurv`` and the ideas behind the problem formalizations. For more
details about the algorithms have a look at the `vignette <https://cran.r-project.org/web/packages/surveillance/surveillance.pdf>`_
of the R surveillance package or the literature references in the model docstrings.

This package was originally developed at the Robert Koch Institute in the `Signale Project <https://rki.de/signale-project>`_ .

.. toctree::
   :maxdepth: 2
   :caption: Contents
   :glob:

   1_quickstart.rst
   2_outbreak_detection.rst
   3_simulations.rst
   4_user_guide.rst
   api_doc/modules.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
