## GTEx Elastic-Net Model Pipeline

This directory can be used for creating models for PredictDB with GTEx
data.

These models can be used to predict gene expression in 44 different
tissues, based on individual genotype.  To train the models, we used
version 6p of the GTEx data and applied 10-fold cross validation
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

(See our wiki)[https://github.com/hakyimlab/PredictDBPipeline/wiki] for
a tutorial with example files and a detailed description of these
scripts.
