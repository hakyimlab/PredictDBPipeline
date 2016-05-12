argv <- commandArgs(trailingOnly = TRUE)
source("GTex_Tissue_Wide_CV_elasticNet.R")

tis <- argv[1]
chrom <- argv[2]

data_dir <- "../data/intermediate/"

expression_RDS <- data_dir %&% "expression_phenotypes/" %&% tis %&% "_Analysis.expr.RDS"
geno_file <- data_dir %&% "genotypes/" %&% tis %&% "_chr" %&% chrom %&% "_Analysis.snps.biallelic.txt"
gene_annot_RDS <- data_dir %&% "annotations/gene_annotation/gencode.v19.no-exons.patched_contigs.parsed.RDS"
snp_annot_RDS <- data_dir %&% "annotations/snp_annotation/GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6.chr" %&% chrom %&% ".RDS"
n_k_folds <- 10
n_k_folds_rep <- 1
alpha <- 0.5
out_dir <- data_dir %&% "model_by_chr/" %&% tis %&% "/"
snpset <- "1KG_snps"

TW_CV_model(expression_RDS, geno_file, gene_annot_RDS, snp_annot_RDS,
    n_k_folds, n_k_folds_rep, alpha, out_dir, tis, chrom, snpset)
