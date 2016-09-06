argv <- commandArgs(trailingOnly = TRUE)
expressionfile <- argv[1]
RDSout <- argv[2]
# Input file has header as people ids, 1st col is gene_id.  Want transposed.
expression <- read.table(expressionfile, stringsAsFactors = FALSE,
    header = TRUE, row.names = 1)
expression <- t(expression)
# Presence of covariate file suggests to correct for PEER factors, etc.
if (length(argv) == 3) {
    covariatefile <- argv[3]
    covariate <- read.table(covariatefile, stringsAsFactors = FALSE,
    header = TRUE, row.names = 1)
    covariate <- t(covariate)

    for (i in 1:length(colnames(expression))) {
        fit <- lm(expression[,i] ~ covariate)
        expression[,i] <- fit$residuals
    }
}

saveRDS(expression, RDSout)
