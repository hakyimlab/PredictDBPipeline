# Reads an expression file in as a dataframe, transposes it, and
# saves it as an RDS object.  If a covariate file is present (as 3rd
# input argument), then it will be used to produce new expression data
# by making a linear model expression ~ covariate, and then pulling the
# residuals as the new expression data.
#
# The input expression file is expected to be tab-delimted, with people
# as columns and genes as row.

argv <- commandArgs(trailingOnly = TRUE)
expressionfile <- argv[1]
RDSout <- argv[2]
# Presence of covariate file suggests to correct for PEER factors, etc.
covariatefile <- ifelse(length(argv) == 3, argv[3], NA)

expression <- read.table(expressionfile, stringsAsFactors = FALSE,
    header = TRUE, row.names = 1)
# Transpose expression.
expression <- t(expression)

if (!is.na(covariatefile)) {
  # Correct expression data for covariates.
  covariate <- read.table(covariatefile, stringsAsFactors = FALSE,
    header = TRUE, row.names = 1)
  covariate <- t(covariate)

  for (i in 1:length(colnames(expression))) {
    fit <- lm(expression[,i] ~ covariate)
    expression[,i] <- fit$residuals
  }
}

saveRDS(expression, RDSout)
