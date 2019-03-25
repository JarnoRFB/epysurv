#!/bin/bash
export R_HOME=$PREFIX/lib/R
R < packages.R --no-save
$PYTHON setup.py install