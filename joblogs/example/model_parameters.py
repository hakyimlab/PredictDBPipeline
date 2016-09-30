import os

# Define parameters----------------------------------------------------/
# Change these variables when adapting for different analyses.

# List of identifiers for each database you'll make:
STUDY_NAMES = ['gEUVADIS']
# File names for gene and snp annotation:
GENE_ANNOTATION_FN = 'gencode.v12.genes.gtf'
SNP_ANNOTATION_FN = 'geuvadis.annot.txt'
# List of genotype/expression file names:
GENOTYPE_FNS = ['geuvadis.snps.txt']
EXPRESSION_FNS = ['geuvadis.expr.txt']
# File name of output for parse_gtf.py:
GENE_ANNOT_INTER1 = 'gencode.v12.genes.parsed.txt'
# File name of output for geno_annot_to_RDS.R:
GENE_ANNOT_INTER2 = 'gencode.v12.genes.parsed.RDS'
# File name prefix of outputs from split_snp_annot_by_chr.py:
SNP_ANN_INTER_PREFIX1 = 'geuvadis.annot'
# File name prefix for input files to snp_annot_to_RDS.R:
SNP_ANN_INTER_PREFIX2 = 'geuvadis.annot.chr'
# File name prefixes for output files from split_genotype_by_chr.py:
GENOTYPE_INTER_PREFIX = ['geuvadis.snps']
# File names for output files from expr_to_transposed_RDS.R:
EXPR_INTER = ['geuvadis.expr.RDS']

# Model metadata/parameters:
SNPSET = 'HapMap'
ALPHA = '0.5'
N_K_FOLDS = '10'
RSID_LABEL = 'RSID_dbSNP137'
WINDOW = '1e6'

# Define directories---------------------------------------------------/
INPUT_DIR = '../../data/input/'
INTER_DIR = '../../data/intermediate/'
OUTPUT_DIR = '../../data/output/'
GENE_ANN_DIR = 'annotations/gene_annotation/'
SNP_ANN_DIR = 'annotations/snp_annotation/'
GENOTYPE_DIR = 'genotypes/'
EXPRESSION_DIR = 'expression_phenotypes/'
MODEL_BY_CHR_DIR = INTER_DIR + 'model_by_chr/'
HOME_DIR = os.path.dirname(os.path.realpath(__file__))
ALL_BETAS_FILES = map(lambda x: OUTPUT_DIR + 'allBetas/' + x + '.allBetas.txt', STUDY_NAMES)
ALL_COVARIANCES_FILES = map(lambda x: OUTPUT_DIR + 'allCovariances/' + x + '_' + SNPSET + '_alpha' + ALPHA + '_window' + WINDOW + '.txt', STUDY_NAMES)
ALL_LOGS_FILES = map(lambda x: OUTPUT_DIR + 'allLogs/' + x + '.allLogs.txt', STUDY_NAMES)
ALL_META_DATA_FILES = map(lambda x: OUTPUT_DIR + 'allMetaData/' + x + '.allMetaData.txt', STUDY_NAMES)
ALL_RESULTS_FILES = map(lambda x: OUTPUT_DIR + 'allResults/' + x + '.allResults.txt', STUDY_NAMES)
DB_FILES = map(lambda x: OUTPUT_DIR + 'dbs/' + x + '_' + SNPSET + '_alpha' + ALPHA + '_window' + WINDOW + '.db', STUDY_NAMES)
