argv <- commandArgs(trailingOnly = TRUE)

"%&%" <- function(a,b) paste(a, b, sep = "")

data_dir <- "../data/intermediate/"
tis <- argv[1]
# Use chromosome 22 for speed.  Sample size will be same for all chromosomes.
chrom <- '22'

expression_RDS <- data_dir %&% "expression_phenotypes/" %&% tis %&% "_Analysis.expr.RDS"
geno_file <- data_dir %&% "genotypes/" %&% tis %&% "_chr" %&% chrom %&% "_Analysis.snps.biallelic.txt"
out_dir <- data_dir %&% "../output/allMetaData/"
snpset <- "1KG_snps"
alpha <- 0.5
n_k_folds <- 10
rsid_label <- "RS_ID_dbSNP142_CHG37p13"

expression <- readRDS(expression_RDS)
genotype <- read.table(geno_file, header = TRUE, row.names = 'Id', stringsAsFactors = FALSE)
n_samples <- length(intersect(colnames(genotype), rownames(expression)))

meta_df <- data.frame(n_samples, n_k_folds, snpset, rsid_label, alpha)
colnames(meta_df) <- c('n_samples', 'n_folds_cv', 'snpset', 'rsid_db_snp_label', 'alpha')
write.table(meta_df, file = out_dir %&% tis %&% '.allMetaData.txt', quote = FALSE, row.names = FALSE, sep = "\t")
