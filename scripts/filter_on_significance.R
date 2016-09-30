suppressMessages(library(qvalue))
suppressMessages(library(RSQLite))
suppressMessages(library(dplyr))
"%&%" <- function(a, b) paste(a, b, sep = "")

package_db <- function(db_in, db_out, gene_annot) {
  # Function to filter sqlite database.  Removes non-protein coding
  # genes, and removes models that don't meet significance at
  # FDR < 0.05.
  driver <- dbDriver("SQLite")
  in_conn <- dbConnect(drv = driver, dbname = db_in)
  out_conn <- dbConnect(drv = driver, dbname = db_out)
  # Copy over construction and sample_info tables and drop `n.genes` column.
  # n.genes refers to all genes, and really just want protein coding.
  construction_df <- dbReadTable(in_conn, "construction", NULL) %>%
    select(-n.genes)
  dbWriteTable(out_conn, "construction", construction_df)
  sample_info_df <- dbReadTable(in_conn, "sample_info", NULL)
  dbWriteTable(out_conn, "sample_info", sample_info_df)
  # Free up some memory.
  rm(construction_df)
  rm(sample_info_df)

  # Read in extra table, calculate q-values, and filter rows.
  extra_df <- dbReadTable(in_conn, "extra", NULL)
  # Include protein coding genes only.
  extra_df <- extra_df %>% filter(gene %in% gene_annot$gene_id)

  # Find qvalues
  qobj <- qvalue(extra_df$pval, fdr.level = 0.05)
  extra_df$pred.perf.qval <- qobj$qvalues
  extra_df$significant <- qobj$significant
  extra_filtered <- extra_df %>%
    rename(pred.perf.pval=pval,n.snps.in.model=n.snps,pred.perf.R2=R2) %>%
    filter(significant == TRUE) %>%
    select(-significant)
  sig_genes <- extra_filtered$gene
  dbWriteTable(out_conn, "extra", extra_filtered)
  dbGetQuery(out_conn, "CREATE INDEX extra_gene ON extra (gene)")

  rm(extra_filtered)
  # Read in weights table, drop all rows pertaining to insignificant genes.
  weights_df <- dbReadTable(in_conn, "weights", NULL)
  weights_filtered <- weights_df %>% filter(gene %in% sig_genes) %>%
    select(one_of(c("rsid", "gene", "weight", "ref_allele", "eff_allele")))
  dbWriteTable(out_conn, "weights", weights_filtered)
  dbGetQuery(out_conn, "CREATE INDEX weights_rsid ON weights (rsid)")
  dbGetQuery(out_conn, "CREATE INDEX weights_gene ON weights (gene)")
  dbGetQuery(out_conn, "CREATE INDEX weights_rsid_gene ON weights (rsid, gene)")
  
  dbDisconnect(in_conn)
  dbDisconnect(out_conn)
}

filter_on_qval <- function(db_in, db_out, gene_annot_RDS) {
  driver <- dbDriver("SQLite")

  # Read in gene annotation info, filter rows for protein coding only
  gene_annot <- readRDS(gene_annot_RDS)
  gene_annot <- gene_annot %>% filter(gene_type == 'protein_coding')
  for (db_file in list.files(DB_DIR)) {
    print("Processing " %&% db_file)
    # Rename file and set correct paths
    file.rename(DB_DIR %&% db_file, DB_DIR %&% sub(".db", "_all.db", db_file))
    old_path <- DB_DIR %&% sub(".db", "_all.db", db_file)
    new_path <- DB_DIR %&% db_file

    # Open connections
    old_conn <- dbConnect(drv = driver, dbname = old_path)
    new_conn <- dbConnect(drv = driver, dbname = new_path)

    # Copy over construction and sample_info tables and drop `n.genes` column.
    # n.genes refers to all genes, and really just want protein coding.
    construction_df <- dbReadTable(old_conn, "construction", NULL) %>% select(-n.genes)
    dbWriteTable(new_conn, "construction", construction_df)
    dbGetQuery(new_conn, "CREATE INDEX construction_chr ON construction (chr)")
    sample_info_df <- dbReadTable(old_conn, "sample_info", NULL)
    dbWriteTable(new_conn, "sample_info", sample_info_df)
    # Free up some memory.
    rm(construction_df)
    rm(sample_info_df)

    # Read in extra table, calculate q-values, and filter rows.
    extra_df <- dbReadTable(old_conn, "extra", NULL)
    # Include protein coding genes only.
    extra_df <- extra_df %>% filter(gene %in% gene_annot$gene_id)
    # Find qvalues
    qobj <- qvalue(extra_df$pval, fdr.level = 0.05)
    extra_df$pred.perf.qval <- qobj$qvalues
    extra_df$significant <- qobj$significant
    extra_filtered <- extra_df %>% rename(pred.perf.pval = pval, n.snps.in.model = n.snps, pred.perf.R2 = R2) %>% filter(significant == TRUE) %>% select(-significant)
    sig_genes <- extra_filtered$gene
    dbWriteTable(new_conn, "extra", extra_filtered)
    dbGetQuery(new_conn, "CREATE INDEX extra_gene ON extra (gene)")

    rm(extra_filtered)

    # Read in weights table, drop all rows pertaining to insignificant genes.
    weights_df <- dbReadTable(old_conn, "weights", NULL)
    weights_filtered <- weights_df %>% filter(gene %in% sig_genes) %>% select(one_of(c("rsid", "gene", "weight", "ref_allele", "eff_allele")))
    dbWriteTable(new_conn, "weights", weights_filtered)
    dbGetQuery(new_conn, "CREATE INDEX weights_rsid ON weights (rsid)")
    dbGetQuery(new_conn, "CREATE INDEX weights_gene ON weights (gene)")
    dbGetQuery(new_conn, "CREATE INDEX weights_rsid_gene ON weights (rsid, gene)")

    rm(weights_filtered)
    rm(weights_df)
    rm(sig_genes)
    
    dbDisconnect(old_conn)
    dbDisconnect(new_conn)
    gc()
  }
}
