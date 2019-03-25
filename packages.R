# Run this script via $ R < packages.R to install all dependencies that cannot be installed trough conda.
repos = getOption("repos")
repos["CRAN"] = "cran.r-project.org"
options(repos = repos)
install.packages("surveillance")
install.packages("gamlss")
install.packages("gridBase")
install.packages("INLA", repos = c(getOption("repos"), INLA = "https://inla.r-inla-download.org/R/stable"), dep = TRUE)
install.packages("MGLM")
install.packages('msm')
