"%&%" <- function(a,b) paste(a, b, sep = "")
library(dplyr)

file_head <- "data/intermediate/annotations/snp_annotation/GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6.chr"

for (i in 1:22) {
  infile <- file_head %&% i %&% ".txt"
  outfile <- file_head %&% i %&% ".RDS"
  snp_annot <- read.table(infile, stringsAsFactors = FALSE, header = TRUE)
  snp_annot <- distinct(snp_annot)
  rownames(snp_annot) <- snp_annot$varID
  saveRDS(snp_annot, outfile)
  print(i %&% "/22")
}
