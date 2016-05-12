data/intermediate/annotations/gene_annotation/gencode.v19.genes.no-exons.patched_contigs.parsed.txt: data/input/annotations/gene_annotation/gencode.v19.genes.no-exons.patched_contigs.gtf scripts/parse_gtf.py
	scripts/parse_gtf.py $< $@

data/intermediate/annotations/gene_annotation/gencode.v19.genes.no-exons.patched_contigs.parsed.RDS: data/intermediate/annotations/gene_annotation/gencode.v19.genes.no-exons.patched_contigs.parsed.txt scripts/geno_annot_to_RDS.R
	Rscript scripts/geno_annot_to_RDS.R $< $@

data/intermediate/annotations/snp_annotation/%.txt: data/input/annotations/snp_annotation/GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6.txt scripts/split_snp_annot_by_chr.py
	scripts/split_snp_annot_by_chr.py $<

data/intermediate/annotations/snp_annotation/%.RDS: data/intermediate/snp_annotation/%.txt scripts/snp_annot_to_RDS.R
	Rscript scripts/snp_annot_to_RDS.R

data/intermediate/genotypes/%.chr*.biallelic.txt: data/input/genotypes/%.txt scripts/split_genotype_by_chr.py
	scripts/split_genotype_by_chr.py $<

data/intermediate/expression_phenotypes/%.RDS: data/input/expression_phenotypes/%.txt scripts/expr_to_transposed_RDS.R
	Rscript scripts/expr_to_transposed_RDS.R $< $@

data/intermediate/model_by_chr/TW_%_exp_10-foldCV_elasticNet_alpha0.5_1KG_snps.txt: scripts/create_model.R \
scripts/GTex_Tissue_Wide_CV_elasticNet.R \
scripts/build_tissue_by_chr.pbs \
data/intermediate/annotations/gene_annotation/gencode.v19.genes.no-exons.patched_contigs.parsed.RDS \
data/intermediate/annotations/snp_annotation/GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6.chr$(filter [1-9]?[0-9],%).RDS \
data/intermediate/genotypes/%_Analysis.snps.biallelic.txt \
data/intermediate/expression_phenotypes/$(filter-out _chr[1-9]?[0-9],%)_Analysis.expr.RDS
	qsub -v tissue=$(filter-out _chr[1-9]?[0-9],%), chrom=$(filter [1-9]?[0-9],%)

