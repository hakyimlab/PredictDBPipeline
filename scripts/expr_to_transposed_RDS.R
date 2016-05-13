
argv <- commandArgs(trailingOnly = TRUE)
expressionfile <- argv[1]
RDSout <- argv[2]
# Input file has header as people ids, first column is gene_id.  Want transposed.
expression <- read.table(expressionfile, stringsAsFactors = FALSE, header = TRUE, row.names = 1)
transposed_exp <- t(expression)
saveRDS(transposed_exp, RDSout)
