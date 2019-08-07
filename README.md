[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JarnoRFB/epysurv/master?filepath=demo.ipynb)
[![Documentation Status](https://readthedocs.org/projects/epysurv/badge/?version=latest)](https://epysurv.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/JarnoRFB/epysurv.svg?token=dmY4GfBz2Rs5oxYeuMhW&branch=master)](https://travis-ci.com/JarnoRFB/epysurv)
[![codecov](https://codecov.io/gh/JarnoRFB/epysurv/branch/master/graph/badge.svg)](https://codecov.io/gh/JarnoRFB/epysurv)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/JarnoRFB/epysurv.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/JarnoRFB/epysurv/context:python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
# epysurv
`epysurv` is a Pythonic wrapper around the [R surveillance package](https://cran.r-project.org/web/packages/surveillance/index.html) 
that strives to implement a `scikit-learn` like API for epidemiological surveillance in Python. 

## In a nutshell

```python
from epysurv import data as epidata
from epysurv.models.timepoint import FarringtonFlexible
train, test = epidata.salmonella()
train.head()
#             n_cases  n_outbreak_cases  outbreak
# 2004-01-05        0                 0     False
# 2004-01-12        0                 0     False
# 2004-01-19        2                 0     False
# 2004-01-26        2                 0     False
# 2004-02-02        1                 0     False    
model = FarringtonFlexible()
model.fit(train)
model.predict(test)
#             n_cases  n_outbreak_cases  outbreak  alarm
# 2011-01-03        1                 0     False    0.0
# 2011-01-10        0                 0     False    0.0
# 2011-01-17        3                 0     False    0.0
# 2011-01-24        3                 0     False    0.0
# 2011-01-31        3                 0     False    0.0
```

## Installation
As `epysurv` requires both Python and R it can only be conveniently installed trough [`conda`](https://docs.conda.io/en/latest/):

    conda install -c conda-forge epysurv 

## Documentation
You can read the [documetation](https://epysurv.readthedocs.io/en/latest/?badge=latest) or try 
an interactive demo on [binder](https://mybinder.org/v2/gh/JarnoRFB/epysurv/master?filepath=demo.ipynb).
    
## Related Projects
* https://github.com/lvphj/epydemiology
* https://github.com/cmrivers/epipy
