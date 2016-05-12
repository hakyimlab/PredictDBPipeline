
argv <- commandArgs(trailingOnly = TRUE)
expressionfile <- argv[1]
RDSout <- argv[2]
expression <- read.table(expressionfile, stringsAsFactors = FALSE, header = TRUE)
transposed_exp <- t(expression)
saveRDS(transposed_exp, RDSout)
