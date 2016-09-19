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
- Covariate data for the expression.
    - A tab delimited text file,

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
    1. Run
    ```
    ./parse_gtf.py ../data/input/annotations/gene_annotation/{gene_annot.gtf} \
        ../data/intermediate/annotations/gene_annotation/{gene_annot.parsed.txt}
    ```
        - This will create a new tab-delimited text file with only the necessary
        features for the model creation.
    2. Run
    ```
    Rscript geno_annot_to_RDS.R ../data/intermediate/annotations/gene_annotation/{gene_annot.parsed.txt} \
        ../data/intermediate/annotations/gene_annotation/{gene_annot.RDS}
    ```
        - This will create an RDS object out of the gene annotation file
        that can be read into R very quickly.
2. SNP annotation.
    1. Run
    ```
    ./split_snp_annot_by_chr.py ../data/input/annotations/snp_annotation/{snp_annot.txt} \
    ../data/intermediate/annotations/snp_annotation/{snp_annot}
    ```
        - This will split the snp annotation file into 22 files, separated
    by chromosome.  The first argument is the input file, and the second
    argument is the prefix for the output.  The files produced will
    append `.chrN.txt` to this prefix, where `N` is the chromosome
    number.
    2. Next, run
    ```
    ./snp_annot_to_RDS.R ../data/intermediate/annotations/snp_annotation/{snp_annot}.chr
    ```
        - This will turn each of the SNP annotation files into RDS objects to be
    used when we're selecting features for the model.
3. Genotype Files.
    1. For each genotype file, run
    ```
    ./split_genotype_by_chr.py ../data/input/genotypes/{genotype.txt} \
        ../data/intermediate/genotypes/{genotype}
    ```
        - This will split the genotype files up by chromosome.  The first
        argument is the input file, the second argument is the prefix
        for the outputs.  The script will append `.chrN.txt` to these
        files where `N` is the chromosome number.
4. Expression Files.
    1. If you have covariate files, as well as expression files, run
    ```
    Rscript expr_to_transposed_RDS.R ../data/input/expression_phenotypes/{expression_file}.txt \
        ../data/intermediate/expression_phenotypes/{expression_file}.RDS \
        ../data/input/expression_phenotypes/{covariate_file_name}
    ```
        - This will first transpose the expression data to have rows as
        people and genes as columns.  Then it performs the a linear regression
        between the covariates and the column vectors of the expression data.
        The residuals are then extracted from the linear model, and that
        is used as the new expression data.  The output file is an RDS
        object. Here the first argument is the input file, the second is
        the destination output file, and the third is the covariate file.
    2. If you do not have covariate data, run the same command as above,
    but do not include a third argument.
5. Creating meta data file.
    1. This will simply be a log of the sample size and the parameters
    you used for the model stored in a tab-delimited text file.  Run the
    `create_meta_data.py` script with the following arguments:
        - `--geno` the path to the input genotype file.  Used to
        calculate sample size.
        - `--expr` the path to the input expression file. Used to
        calculate sample size.
        - `--snpset` the SNP set for the study.  E.g. '1KG' for 1000
        Genomes and 'HapMap' for HapMap.
        - `--alpha` the mixing parameter glmnet will use to train the
        model.  Must be a number between 0.0 and 1.0.  Default value is
        0.5
        - `--n_k_folds` the number of folds to use in cross-validation.
        Default value is 10.
        - `--rsid_label` version of the rsid numbers.  This should be
        name of the 7th column in the snp annotation file.
        - `--window` how far to look upstream of the TSS and downstream
        of the TTS for consideration of ciseqtls.
        - `--out_prefix` the prefix for the output file.  Include the
        full path to `data/output/allMetaData/` and then what you'd like
        to label the analysis (e.g. Lung, Liver, etc.).  The script will
        append `.allMetaData.txt` for dependency reasons.

Since you may be rerunning these analyses many times, it would make sense
to run all of these commands in a single script.  See
`preprocess_input.py` for a way to do this with GTEx data.


#### Training Models

Right now, you will have to modify the scripts `build_all_models.py`,
`create_model.R` and `build_tissue_by_chr.pbs` to specify the parameters
and file names to use.

`build_all_models.py` is a script that will submit jobs to the computing
cluster.  For GTEx, we had 44 tissues to study, and we split up the
analysis by chromosome, which resulted in submitting 968 jobs.  The
common aspects of every job are specified in `build_tissue_by_chr.pbs`,
but controls for which tissue, chromosome, and window size are controlled
in `build_all_models.py`.  These arguments are then defined for the pbs
script when the job is submitted.

When editing the pbs script, be sure to edit the paths to the stdout,
stderr, and directory for where all the scripts are located.

The `pbs` job will call the R script `create_model.R`.  Many parameters
in this script are still hard coded, and will likely have to be changed
if you are adopting this for studies besides GTEx.

It is very important to note that the value given for 'tissue' will be
used in file names and group tissues together.

I'm working on refactoring this step in the process to make the api
more user friendly, but it will take some time and testing.

Once all of the jobs are finished, inspect the standard out and standard
error files to check for any funny business.  If successful, the stdout
files will just include an output of which gene in the expression file
it is analyzing.  If all goes well, the last line should be
`n_genes / n_genes`, where `n_genes` is the number of expressed genes on
that chromosome.

If you put all of the stdout and stderr files into a subdirectory within
the `joblogs/` and kept the stdout files to have the pattern
`_model_chrN.o` in the name, you can use the script `check_job_logs.py`
to make sure all the stdout files are ok.  Just supply the name of
the subdirectory to inspect within `joblogs`.

#### Putting everything together

Edit the script `assemble_tissue_models.py` so that the variable
`tissues` is a list which holds the tissue identifier for each model you
are building.

Also edit the script `generate_db_job.pbs` to make sure all the
stdout, stderr files and working directory for the script are correct.

Running the script `assemble_tissue_models.py` will then take all of the
files produced by the many cluster and concatenate all the separate
chromosome files together.  The step of this script submits another
cluster job to create the sqlite databases.

#### Filtering out non-significant results/protein-coding only

Once the databases are created, go to the scripts directory, enter an
interactive R session and run the following:

```
> source("filter_on_significance.R")
> filter_on_qval()
```

This will create databases with significant protein-coding models only.
Original databases with all models now have `_all.db` as a suffix.

And that's it! Your databases are now ready for use with PrediXcan and
MetaXcan.

