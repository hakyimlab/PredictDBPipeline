library(glmnet)
library(methods)
"%&%" <- function(a,b) paste(a, b, sep = "")

TW_CV_model <- function(expression_RDS, geno_file, gene_annot_RDS, snp_annot_RDS, n_k_folds, n_k_folds_rep, alpha, out_dir, tis, chrom, snpset) {
  expression <- readRDS(expression_RDS)
  genotype <- read.table(geno_file, header = TRUE, row.names = 'Id', stringsAsFactors = FALSE)
  # Transpose genotype for glmnet
  genotype <- t(genotype)
  gene_annot <- readRDS(gene_annot_RDS)
  gene_annot <- subset(gene_annot, gene_annot$chr == chrom)
  snp_annot <- readRDS(snp_annot_RDS)
  
  rownames(gene_annot) <- gene_annot$gene_id
  # Subset expression data to only include genes with gene_info
  expression <- expression[, intersect(colnames(expression), rownames(gene_annot))]
  exp_samples <- rownames(expression)
  exp_genes <- colnames(expression)
  n_samples <- length(exp_samples)
  n_genes <- length(exp_genes)
  seed <- sample(1:2016, 1)
  log_df <- data.frame(chrom, n_genes, seed, alpha)
  colnames(log_df) <- c('chr', 'n_genes', 'seed_for_cv', 'alpha')
  write.table(log_df, file = out_dir %&% tis %&% '_chr' %&% chrom %&% '_elasticNet_model_log.txt', quote = FALSE, row.names = FALSE, sep = "\t")
  set.seed(seed)
  groupid <- sample(1:n_k_folds, length(exp_samples), replace = TRUE)

  resultsarray <- array(0, c(length(exp_genes), 9))
  dimnames(resultsarray)[[1]] <- exp_genes
  resultscol <- c("gene", "alpha", "cvm", "lambda.iteration", "lambda.min", "n.snps", "R2", "pval", "genename")
  dimnames(resultsarray)[[2]] <- resultscol
  workingbest <- out_dir %&% "working_TW_" %&% tis %&% "_exp_" %&% n_k_folds %&% "-foldCV_elasticNet_alpha" %&% alpha %&% "_" %&% snpset %&% "_chr" %&% chrom %&% ".txt"
  write(resultscol, file = workingbest, ncolumns = 9, sep = "\t")

  weightcol <- c("gene","rsid","ref","alt","beta","alpha")
  workingweight <- out_dir %&% "TW_" %&% tis %&% "_elasticNet_alpha" %&% alpha %&% "_" %&% snpset %&% "_weights_chr" %&% chrom %&% ".txt"
  write(weightcol, file = workingweight, ncol = 6, sep = "\t")

  for (i in 1:length(exp_genes)) {
    cat(i, "/", length(exp_genes), "\n")
    gene <- exp_genes[i]
    # Reduce genotype data to only include SNPs within 1 megabase of gene in question.
    # Pulls the genotype for all snps within 1 megabase of the gene.
    geneinfo <- gene_annot[gene,]
    start <- geneinfo$start - 1e6
    end <- geneinfo$end + 1e6
    # Pull cis-SNP info
    cissnps <- subset(snp_annot, snp_annot$pos >= start & snp_annot$pos <= end)
    # Pull cis-SNP genotypes
    cisgenos <- genotype[,intersect(colnames(genotype), cissnps$varID)]
    if (is.null(dim(cisgenos))) {
      # Skip genes without any cis-SNPS
      bestbetas <- data.frame()
    } else {
      # Reduce cisgenos to only include SNPs with at least 1 minor allele in dataset
      minorsnps <- subset(colMeans(cisgenos), colMeans(cisgenos, na.rm = TRUE) > 0)
      minorsnps <- names(minorsnps)
      cisgenos <- cisgenos[,minorsnps]
      if (is.null(dim(cisgenos)) | dim(cisgenos)[2] == 0){
        # Skip genes with <2 cis-SNPs in dataset
        bestbetas <- data.frame()
      } else {
        # Pull expression data for gene
        exppheno <- expression[,gene]
        # Scale for fastLmPure to work properly
        exppheno <- scale(exppheno, center = TRUE, scale = TRUE) 
        exppheno[is.na(exppheno)] <- 0
        rownames(exppheno) <- rownames(expression)

        # Run Cross-Validation over alphalist
        # parallel = TRUE is slower on tarbell for some reason
        fit <- cv.glmnet(cisgenos, exppheno, nfolds = n_k_folds, alpha = alpha, keep = TRUE, foldid = groupid, parallel = FALSE)
        
        # Pull info from fit to find the best lambda   
        fit.df <- data.frame(fit$cvm, fit$lambda, 1:length(fit$cvm))
        # Needs to be min or max depending on cv measure (MSE min, AUC max, ...)
        best.lam <- fit.df[which.min(fit.df[,1]),]
        cvm.best <- best.lam[,1]
        lambda.best <- best.lam[,2]
        # Position of best lambda in cv.glmnet output
        nrow.best <- best.lam[,3]
        # Get the betas from the best lambda value
        ret <- as.data.frame(fit$glmnet.fit$beta[,nrow.best])
        ret[ret == 0.0] <- NA
        # Pull the non-zero betas from model
        bestbetas <- as.vector(ret[which(!is.na(ret)),])
        names(bestbetas) <- rownames(ret)[which(!is.na(ret))]
        # Pull out the predictions at the best lambda value.    
        pred.mat <- fit$fit.preval[,nrow.best]
        }
    }
    if (length(bestbetas) > 0) {
      res <- summary(lm(exppheno~pred.mat))
      genename <- as.character(gene_annot[gene, 3])
      rsq <- res$r.squared
      pval <- res$coef[2,4]  
      resultsarray[gene,] <- c(gene, alpha, cvm.best, nrow.best, lambda.best, length(bestbetas), rsq, pval, genename)  
      # Output best shrunken betas for PrediXcan
      bestbetalist <- names(bestbetas)
      bestbetainfo <- snp_annot[bestbetalist,]
      betatable <- as.matrix(cbind(bestbetainfo,bestbetas))
      # Output "gene", "rsid", "refAllele", "effectAllele", "beta"
      # For future: To change rsid to the chr_pos_ref_alt_build label, change "rsid" below to "varID".
      betafile<-cbind(gene,betatable[,"rsid"],betatable[,"refAllele"],betatable[,"effectAllele"],betatable[,"bestbetas"], alpha)
      # Transposing betafile necessary for correct output from write() function
      write(t(betafile), file = workingweight, ncolumns = 6, append = TRUE, sep = "\t")
      write(resultsarray[gene,], file = workingbest, ncolumns = 9, append = TRUE, sep = "\t")
    } else {
      genename <- as.character(gene_annot[gene,3])
      resultsarray[gene,1] <- gene
      resultsarray[gene,2:8] <- c(alpha,NA,NA,NA,0,NA,NA)
      resultsarray[gene,9] <- genename
    }
  }
  write.table(resultsarray,file=out_dir %&% "TW_" %&% tis %&% "_chr" %&% chrom %&% "_exp_" %&% n_k_folds %&% "-foldCV_elasticNet_alpha" %&% alpha %&% "_" %&% snpset %&% ".txt",quote=F,row.names=F,sep="\t")
}
