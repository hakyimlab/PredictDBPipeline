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

  set.seed(1209)
  groupid <- sample(1:n_k_folds, length(exp_samples), replace = TRUE)

  resultsarray <- array(0, c(length(exp_genes), 9))
  dimnames(resultsarray)[[1]] <- exp_genes
  resultscol <- c("gene","alpha","cvm","lambda.iteration","lambda.min","n.snps","R2","pval","genename")
  dimnames(resultsarray)[[2]] <- resultscol
  workingbest <- out_dir %&% "working_TW_" %&% tis %&% "_exp_" %&% n_k_folds %&% "-foldCV_elasticNet_alpha" %&% alpha %&% "_" %&% snpset %&% "_chr" %&% chrom %&% ".txt"
  write(resultscol,file=workingbest,ncolumns=9,sep="\t")

  weightcol = c("gene","rsid","ref","alt","beta","alpha")
  workingweight <- out_dir %&% "TW_" %&% tis %&% "_elasticNet_alpha" %&% alpha %&% "_" %&% snpset %&% "_weights_chr" %&% chrom %&% ".txt"
  write(weightcol,file=workingweight,ncol=6,sep="\t")

  for (i in 1:length(exp_genes)) {
    cat(i,"/",length(exp_genes),"\n")
    gene <- exp_genes[i]
    cisgenos <- get_cisgenos(gene, gene_annot, snp_annot)
    if (is.null(dim(cisgenos))) {
      bestbetas <- data.frame() ###effectively skips genes with <2 cis-SNPs
    } else {
      minorsnps <- subset(colMeans(cisgenos), colMeans(cisgenos,na.rm=TRUE)>0) ###pull snps with at least 1 minor allele###
      minorsnps <- names(minorsnps)

      cisgenos <- cisgenos[,minorsnps]
      if (is.null(dim(cisgenos)) | dim(cisgenos)[2] == 0){###effectively skips genes with <2 cis-SNPs
        bestbetas <- data.frame() ###effectively skips genes with <2 cis-SNPs
      } else {
            
        exppheno <- expression[,gene] ### pull expression data for gene
        exppheno <- scale(exppheno, center=T, scale=T)  ###need to scale for fastLmPure to work properly
        exppheno[is.na(exppheno)] <- 0
        rownames(exppheno) <- rownames(expression)

        ##run Cross-Validation over alphalist
        fit <- cv.glmnet(cisgenos,exppheno,nfolds=n_k_folds,alpha=alpha,keep=T,foldid=groupid,parallel=F) ##parallel=T is slower on tarbell, not sure why
            
        fit.df <- data.frame(fit$cvm,fit$lambda,1:length(fit$cvm)) ##pull info to find best lambda
        best.lam <- fit.df[which.min(fit.df[,1]),] # needs to be min or max depending on cv measure (MSE min, AUC max, ...)
        cvm.best = best.lam[,1]
        lambda.best = best.lam[,2]
        nrow.best = best.lam[,3] ##position of best lambda in cv.glmnet output
            
        ret <- as.data.frame(fit$glmnet.fit$beta[,nrow.best]) # get betas from best lambda
        ret[ret == 0.0] <- NA
        bestbetas = as.vector(ret[which(!is.na(ret)),]) # vector of non-zero betas
        names(bestbetas) = rownames(ret)[which(!is.na(ret))]
            
        pred.mat <- fit$fit.preval[,nrow.best] # pull out predictions at best lambda
            
        }
    }
    if (length(bestbetas) > 0) {
      res <- summary(lm(exppheno~pred.mat))
      genename <- as.character(gene_annot[gene, 3])
      rsq <- res$r.squared
      pval <- res$coef[2,4]
        
      resultsarray[gene,] <- c(gene, alpha, cvm.best, nrow.best, lambda.best, length(bestbetas), rsq, pval, genename)
        
      ### output best shrunken betas for PrediXcan
      bestbetalist <- names(bestbetas)
      bestbetainfo <- snp_annot[bestbetalist,]
      betatable <- as.matrix(cbind(bestbetainfo,bestbetas))
      ##output "gene","rsid","refAllele","effectAllele","beta"
      # To change rsid to the chr_pos_ref_alt_build label, change "rsid" below to "varID".  Want to do eventually.
      betafile<-cbind(gene,betatable[,"rsid"],betatable[,"refAllele"],betatable[,"effectAllele"],betatable[,"bestbetas"], alpha) 
      write(t(betafile),file=workingweight,ncolumns=6,append=T,sep="\t") # t() necessary for correct output from write() function
      write(resultsarray[gene,],file=workingbest,ncolumns=9,append=T,sep="\t")
    } else {
      genename <- as.character(gene_annot[gene,3])
      resultsarray[gene,1] <- gene
      resultsarray[gene,2:8] <- c(alpha,NA,NA,NA,0,NA,NA)
      resultsarray[gene,9] <- genename
    }
  }
  write.table(resultsarray,file=out_dir %&% "TW_" %&% tis %&% "_exp_" %&% n_k_folds %&% "-foldCV_elasticNet_alpha" %&% alpha %&% "_" %&% snpset %&% "_chr" %&% chrom %&% ".txt",quote=F,row.names=F,sep="\t")
}

get_cisgenos <- function(gene, gene_annot, snp_annot) {
  # Pulls the genotype for all snps within 1 megabase of the gene.
  geneinfo <- gene_annot[gene,]
  start <- geneinfo$start - 1e6
  end <- geneinfo$end + 1e6
  # Pull cis-SNP info
  cissnps <- subset(snp_annot, snp_annot$pos >= start & snp_annot$pos <= end)
  # Pull cis-SNP genotypes
  cisgenos <- genotype[,intersect(colnames(genotype), cissnps$varID)]
  return(cisgenos)
}
