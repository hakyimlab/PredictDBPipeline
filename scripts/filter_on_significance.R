library(qvalue)
library(RSQLite)
library(dplyr)
"%&%" <- function(a, b) paste(a, b, sep = "")

filter_on_qval <- function() {
  DB_DIR <- "../data/output/dbs/"
  driver <- dbDriver("SQLite")

  for (db_file in list.files(DB_DIR)) {
    print("Processing " %&% db_file)
    # Rename file and set correct paths
    file.rename(DB_DIR %&% db_file, DB_DIR %&% sub(".db", "_all.db", db_file))
    old_path <- DB_DIR %&% sub(".db", "_all.db", db_file)
    new_path <- DB_DIR %&% db_file

    # Open connections
    old_conn <- dbConnect(drv = driver, dbname = old_path)
    new_conn <- dbConnect(drv = driver, dbname = new_path)

    # Copy over construction and sample_info tables
    construction_df <- dbReadTable(old_conn, "construction", NULL)
    dbWriteTable(new_conn, "construction", construction_df)
    dbGetQuery(new_conn, "CREATE INDEX construction_chr ON construction (chr)")
    sample_info_df <- dbReadTable(old_conn, "sample_info", NULL)
    dbWriteTable(new_conn, "sample_info", sample_info_df)
    # Free up some memory.
    rm(construction_df)
    rm(sample_info_df)

    # Read in extra table, calculate q-values, and filter rows.
    extra_df <- dbReadTable(old_conn, "extra", NULL)
    qobj <- qvalue(extra_df$pval, fdr.level = 0.05)
    extra_df$qval <- qobj$qvalues
    extra_df$significant <- qobj$significant
    extra_filtered <- extra_df %>% rename(pred.perf.pval = pval) %>% filter(significant == TRUE) %>% select(-significant)
    sig_genes <- extra_filtered$gene
    dbWriteTable(new_conn, "extra", extra_filtered)
    dbGetQuery(new_conn, "CREATE INDEX extra_gene ON extra (gene)")

    rm(extra_filtered)

    # Read in weights table, drop all rows pertaining to insignificant genes.
    weights_df <- dbReadTable(old_conn, "weights", NULL)
    weights_filtered <- weights_df %>% filter(gene %in% sig_genes)
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
