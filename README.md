[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JarnoRFB/epysurv/master?urlpath=lab/tree/demo.ipynb)
[![Build Status](https://travis-ci.com/JarnoRFB/epysurv.svg?token=dmY4GfBz2Rs5oxYeuMhW&branch=master)](https://travis-ci.com/JarnoRFB/epysurv)

# epysurv
`epysurv` is a Pythonic wrapper around the [R surveillance package](https://cran.r-project.org/web/packages/surveillance/index.html) 
that strives to implement a `scikit-learn` like API for epidemiological surveillance in Python. 

## In a nutshell

    from epysurv import data as epidata
    from epysurv.models.timepoint import FarringtonFlexible
    train, test = epidata.salmonella()
    model = FarringtonFlexible()
    model.fit(train)
    model.predict(test)


## Installation
As `epysurv` requires both Python and R it can only be conveniently installed trough `conda`:

    conda config --add channels conda-forge 
    conda config --add channels jarnorfb 
    conda install epysurv

## Documentation
Coming soon... For now see [`demo.ipynb`](demo.ipynb).
    
## Related Projects
* https://github.com/lvphj/epydemiology
* https://github.com/cmrivers/epipy