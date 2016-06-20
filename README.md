## GTEx Elastic-Net Model Pipeline

This directory can be used for creating models for PredictDB with GTEx data.

These models can be used to predict gene expression in 44 different tissues, based on individual
genotype.  To train the models, we used version 6 of the GTEx data and applied 10-fold cross
validation elastic-net within SNPs that are located within 1mb of the gene as features.

The pipeline takes 4 different sets of inputs (all in the data/inputs/ directory, possibly in the
form of symbolic links), does some preprocessing, stores the results in the data/intermediate/
directory.  Once this is all done, we can apply our machine learning technique, output the
results in the data/output/ directory.  There's also a script to turn this data into SQLite
databases, to be used by PrediXcan.

### Overview

At the most granular level, we are using the GTEx data to predict the expression level of a gene
in a specific tissue, based on the SNPs located within 1 megabase of that gene.  We then do this
for thousands of genes in a single tissue, and then repeat for each of the 40-some tissues studied
by GTEx.

For each gene/tissue pair, we fit an Elastic Net linear model based on the GTEx data, using the
dosages of the nearby SNPs as features, with parameters alpha=0.5 and lambda chosen by
cross-validation.  Once we have the weights from the fitted-model, we can store them in a SQLite
database for the tissue.  This database can be used by others in conjunction with the software PrediXcan,
which allows researchers to predict gene expression in a specific tissue, given genotype data.

To accomplish this for a single gene/tissue pair, we need the following data:

- The start and position of the gene
- All snps located within 1000 base pairs of that gene.
- Expression level data for the gene in the specific tissue for the GTEx individuals
- Genotypes for all these individuals on the snp set.

As we are doing this process many, many times, this pipeline falls into the category of "embarassingly
parallelizable."  For ease of programming though, we implemented some poor man's parallelization by
splitting these processes into jobs split by chromosome and tissue, and submitting them to a computing
cluster.  Each of these jobs will handle all genes on a given chromosome for a specific tissue.

### Inputs

This pipeline takes 4 different sets of input data:

- A gene annotation file
    - In `.gtf` format.  Must have gene_id (ensemble ID) and gene_name attributes.
- A SNP annotation file
    - A tab delimited file, with a header row, containing the fields:
    chromosome, position, VariantID, RefAllele, AlternativeAllele, original RSID number,
    more recent RSID number, Num_alt_per_sit.
    - At a minimum, there must be a header row, with chromosome in the first column,
    position in the second, VariantID in the third (form: chr_pos_refAll_altAll_build),
    ref Allele in the fourth, alt Allele in the fifth, and rsid in the seventh.  
- The GTEx genotype files by tissue
    - A tab delimited file, with a header row, first column being the variantID of the SNP,
    and all remaining columns being individual ids.  The values indicate the dosage for the
    second allele listed in the variantID.
    - (IMPORTANT) File name convention: `{tissue_name}_Analysis.snps.txt`
- The GTEx gene expression files by tissue.
    - A tab delimited file, with a header row, first column being the ensembleID of the
    gene, and all remaining columns being individual ids.  The values indicate the expresion
    levels of the gene.
    - (IMPORTANT) File name convention: `{tissue_name}_Analysis.expr.txt'

### Preprocessed Data

After all preprocessing the inputs into the analysis script will look like the following:

- Gene Annotation:
    - an R dataframe saved as an RDS object with columns `chr`, `gene_id`, `gene_name`, `start`,
    `end`. The rownames of the dataframe are the `gene_id`.
    - File name convention: None specifically.  Right now this value is hard-coded as
    `gencode.v19.genes.no-exons.patched_contigs.parsed.RDS`
- SNP Annotation:
    - The snp annotation file is split up by chromosome (i.e. there are 22 files. There's an
    assumption of working with human genotypes, and we don't work with X or Y chromosome) and saved
    as an R dataframe (RDS Object) with columns `chr`, `pos`, `varID`, `refAllele`, `effectAllele`,
    and `rsid`.  All rows are true snps (i.e. single letter variants only).  The `varID` column is
    saved as the rownames.
    - File name convention: Whatever the original snp annotation file was, but with the extension
    removed and replaced with `.chr{chromosome_number}.RDS`.
- Genotype files:
    - Again split by chromosome, but saved as a tab-delimited text file.  Has a header row with
    fields `Id` for the variant ID of the snp and the rest are the individual ID labels.  Rows
    have been filtered so that only single letter variants are included.
    - File name convention: `{tissue_name}_chr{chromosome_number}_Analysis.snps.biallelic.txt`.
- Expression files:
    - An R dataframe saved as an RDS object.  colnames are the ensembleID and the rownames are
    the individual ids.  Note that this is transposed from the original input.
    - File name convention: `{tissue_name}_Analysis.expr.RDS`.

### Output

The output files to care about are the SQLite databases created for each tissue.

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
            - the number of expressed genes found in tissue for the chromosome
        - cv.seed
            - the random seed used to split the data for cross-validation.  Only useful if you want to fully reconstruct the model exactly.
    4. sample_info
        - n.samples
            - The number of samples (people) used to train the model.

### Directory Structure

If you are trying to adapt this pipeline for yourself, be aware that the scripts were written with the
following directory structure in mind:

```
|modelpipeline/
    |data/
        |input/
            |annotations/
                |gene_annotation/
                    > gene_annotation_file
                |snp_annotation/
                    > snp_annotation_file
            |expression_phenotypes/
                > tissue_1_expression_file
                > tissue_2_expression_file
                > ...
                > tissue_n_expression_file
            |genotypes/
                > tissue_1_genotype_file
                > tissue_2_genotype_file
                > ...
                > tissue_n_genotype_file
        |intermediate/
            |annotations/
                |gene_annotation/
                    > parsed_gene_annotation_file
                    > parsed_gene_annotation_file.RDS
                |snp_annotation/
                    > snp_annotation_chr1_file
                    > snp_annotation_chr2_file
                    > ...
                    > snp_annotation_chr22_file
                    > snp_annotation_chr1_file.RDS
                    > snp_annotation_chr2_file.RDS
                    > ...
                    > snp_annotation_chr22_file.RDS
            |expression_phenotypes/
                > tissue_1_expression_file.RDS
                > tissue_2_expression_file.RDS
                > ...
                > tissue_n_expression_file.RDS
            |genotypes/
                > tissue_1_chr1_genotype_file
                > tissue_1_chr2_genotype_file
                > ...
                > tissue_1_chr22_genotype_file
                > tissue_2_chr1_genotype_file
                > tissue_2_chr2_genotype_file
                > ...
                > tissue_n_chr22_genotype_file
            |model_by_chr/
                > tissue_1_chr1_log_file
                > tissue_1_chr1_betas
                > tissue_1_chr1_results
                > ...
                > tissue_n_chr22_log_file
                > tissue_n_chr22_betas
                > tissue_n_chr22_results
        |output/
            |allBetas/
                > tissue_1_allBetas
                > tissue_2_allBetas
                > ...
                > tissue_n_allBetas
            |allLogs/
                > tissue_1_allLogs
                > tissue_2_allLogs
                > ...
                > tissue_n_allLogs
            |allMetaData/
                > tissue_1_allMetaData
                > tissue_2_allMetaData
                > ...
                > tissue_n_allMetaData
            |allResults/
                > tissue_1_allResults
                > tissue_2_allResults
                > ...
                > tissue_n_allResults
            |dbs/
                > tissue_1.db
                > tissue_2.db
                > ...
                > tissue_n.db
    |joblogs/
        > output logs of all qsub jobs...
        > error logs of all qsub jobs...
    |scripts/
        > ...
    
```

### Running the scripts

**Step 0**: Make sure all of your data is in the correct format

**Step 1**: cd to the `modelpipeline` directory

**Step 2**: Put symbolic links to your data in the appropriate subdirectory in the `data/input/` directory:

> `ln -s {path to Gene_Annotation_File} data/input/annotations/gene_annotation/{Gene_Annotation_File}`
> `ln -s {path to SNP_Annotation_File} data/input/annotation/snp_annotation/{SNP_Annotation_File}`
> `ln -s {path to Expression_File} data/input/expression_phenotypes/{Expression_File}`
> `ln -s {path to Genotype_File} data/input/genotypes/{Genotype_File}`

**Step 3**: Enter a qsub interactive session with the `qsub -I` command

**Step 4**: 
