# Run this script via $ R < packages.R to install all R dependencies.
repos = getOption("repos")
repos["CRAN"] = "https://cran.r-project.org"
options(repos = repos)
install.packages("surveillance")
install.packages("gamlss")
install.packages("gridBase")
install.packages("MGLM")
install.packages('msm')
