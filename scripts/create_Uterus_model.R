argv <- commandArgs(trailingOnly = TRUE)
source("GTex_Tissue_Wide_CV_elasticNet.R")

chrom <- argv[1]

expression_RDS <- "expression/Uterus_Analysis.expr.t.RDS"
geno_file <- "genotype_by_chr/Uterus_Analysis.snps.chr" %&% chrom %&% "_SNPs_Only.txt"
gene_annot_RDS <- "annotation/gencode.v19.no-exons.patched_contigs.parsed.RDS"
snp_annot_RDS <- "snp_annot_by_chr/GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6.chr" %&% chrom %&% ".RDS"
n_k_folds <- 10
n_k_folds_rep <- 1
alpha <- 0.5
out_dir <- "output/"
tis <- "Uterus"
snpset <- "1KG_snps"

TW_CV_model(expression_RDS, geno_file, gene_annot_RDS, snp_annot_RDS,
    n_k_folds, n_k_folds_rep, alpha, out_dir, tis, chrom, snpset)
