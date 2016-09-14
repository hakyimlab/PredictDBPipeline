## GTEx Elastic-Net Model Pipeline

This directory can be used for creating models for PredictDB with GTEx
data.

These models can be used to predict gene expression in 44 different
tissues, based on individual genotype.  To train the models, we used
version 6 of the GTEx data and applied 10-fold cross validation
elastic-net within SNPs that are located within 1mb of the gene as
features.

The pipeline takes 4 different sets of inputs (all in the data/inputs/
directory, possibly in the form of symbolic links), does some
preprocessing, stores the results in the data/intermediate/
directory.  Once this is all done, we can apply our machine learning
technique, output the results in the data/output/ directory.  There's
also a script to turn this data into SQLite databases, to be used by
PrediXcan.

With some modifications, this pipeline can be extended to analyze other
studies which have genotype and expression data.

### Overview

At the most granular level, we are using the GTEx data to predict the
expression level of a gene in a specific tissue, based on the SNPs
located within 1 megabase of that gene.  We then do this for thousands
of genes in a single tissue, and then repeat for each of the 40-some
tissues studied by GTEx.

For each gene/tissue pair, we fit an Elastic Net linear model based on
the GTEx data, using the allelic dosages of the nearby SNPs as
features, with parameters alpha=0.5 and lambda chosen by
cross-validation.  Once we have the weights from the fitted-model, we
can store them in a SQLite database for the tissue.  This database can
be used by others in conjunction with the software PrediXcan, which
allows researchers to predict gene expression in a specific tissue,
given genotype data, and the software MetaXcan, which takes the output
of GWAS summary statistics to infer associations between phenotype and
gene expression.

To accomplish this for a single gene/tissue pair, we need the following
data:

- The start and position of the gene
- All snps located within 1Mb base pairs of that gene (1Mb upstream of
    trascription start site and 1Mb downstream of transcription
    termination site).
- Expression quantification data for the gene in the specific tissue
    for the GTEx individuals
- Genotypes for all these individuals on the snp set.

For speed, we implemented some poor man's parallelization by splitting
these processes into jobs split by chromosome and tissue, and
submitting them to a computing cluster.  Each of these jobs will handle
all genes on a given chromosome for a specific tissue.

### Inputs

This pipeline takes 4 different sets of input data:

- A gene annotation file
    - In `gtf` format.  Must have gene_id (ensemble ID) and gene_name
    attributes.
- A SNP annotation file
    - A tab delimited file, with a header row, containing the fields:
    chromosome, position, VariantID, RefAllele, AlternativeAllele,
    original RSID number, more recent RSID number, Num_alt_per_site.
    - At a minimum, there must be a header row, with chromosome in the
    first column, position in the second, VariantID in the third (form:
    chr_pos_refAllele_altAllele_build), ref Allele in the fourth, alt
    Allele in the fifth, and rsid in the seventh.  
- The GTEx genotype files by tissue
    - A tab delimited file, with a header row, first column being the
    variantID of the SNP, and all remaining columns being individual
    ids. The values indicate the dosage for the second allele listed in
    the
    variantID.
- The GTEx gene expression files by tissue.
    - A tab delimited file, with a header row, first column being the
    ensembl ID of the gene, and all remaining columns being individual
    ids.  The values indicate the expresion levels of the gene.

### Preprocessed Data

After all preprocessing the inputs into the analysis script will look
like the following:

- Gene Annotation:
    - an R dataframe saved as an RDS object with columns `chr`,
    `gene_id`, `gene_name`, `start`, `end`. The rownames of the
    dataframe are the `gene_id`.
- SNP Annotation:
    - The snp annotation file is split up by chromosome (i.e. there are
    22 files. There's an assumption of working with human genotypes, and
    we don't work with X or Y chromosome) and saved
    as an R dataframe (RDS Object) with columns `chr`, `pos`, `varID`,
    `refAllele`, `effectAllele`, and `rsid`.  All rows are SNPs (no
    INDELS), and unambiguously stranded.  The `varID` column is saved as
    the rownames.
- Genotype files:
    - Again split by chromosome, but saved as a tab-delimited text file.
    Has a header row with fields `Id` for the variant ID of the snp and
    the rest are the individual ID labels.  Rows have been filtered so
    that only single letter variants are included.
- Expression files:
    - An R dataframe saved as an RDS object.  colnames are the ensembl
    ID and the rownames are the individual ids.  Note that this is
    transposed from the original input.

### Output

The output files to care about are the SQLite databases created for each
tissue.

Each database consists of four tables:
    1. weights
        - rsid
        - gene
        - weight
        - ref_allele
        - eff_allele
    2. extra
        - gene
        - genename
        - R2
        - n.snps
        - pred.perf.pval
        - qval
    3. construction
        - chr
        - n.genes
            - the number of expressed genes found in tissue for the 
            chromosome
        - cv.seed
            - the random seed used to split the data for
            cross-validation.  Only useful if you want to fully
            reconstruct the model exactly.
    4. sample_info
        - n.samples
            - The number of samples (people) used to train the model.

### Directory Structure

### Running the scripts

#### Setup

Once you have your data in the correct format and have cloned this
repository into a place in which can submit jobs to a computing cluster,
`cd` into the scripts directory and run the shell script
`make_dir_tree.sh`.  This will create all the directories required for
the pipeline.

Then, `mv`, `cp`, or symbolically link your correctly formatted data
into the appropriate directory.

- gene annotation (gtf) file goes in
`data/input/annotations/gene_annotation/`
- snp annotation file goes in
`data/input/annotations/snp_annotation/`
- genotype file(s) go in `data/input/genotypes/`
- expression file(s) go in `data/input/expression_phenotypes/`

#### Preprocess Data

Note: run all scripts from scripts directory.

1. Gene annotation. Use the script `parse_gtf.py` with first argument
the path to the annotation file, and second argument the file output.
    - Run
    > ./parse_gtf.py ../data/input/annotations/gene_annotation/{gene_annot_file} \
    ../data/intermediate/annotations/gene_annotation/{gene_annot_output}

2. SNP annotation.

3. Genotype Files.

4. Expression Files.

#### Training Models


