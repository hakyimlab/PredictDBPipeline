import os

# Define parameters----------------------------------------------------/
# Change these variables when adapting for different analyses.

# List of Tissue Identifiers
STUDY_NAMES = [
    'Adipose_Subcutaneous',
    'Adipose_Visceral_Omentum',
    'Adrenal_Gland',
    'Artery_Aorta',
    'Artery_Coronary',
    'Artery_Tibial',
    'Brain_Anterior_cingulate_cortex_BA24',
    'Brain_Caudate_basal_ganglia',
    'Brain_Cerebellar_Hemisphere',
    'Brain_Cerebellum',
    'Brain_Cortex',
    'Brain_Frontal_Cortex_BA9',
    'Brain_Hippocampus',
    'Brain_Hypothalamus',
    'Brain_Nucleus_accumbens_basal_ganglia',
    'Brain_Putamen_basal_ganglia',
    'Breast_Mammary_Tissue',
    'Cells_EBV-transformed_lymphocytes',
    'Cells_Transformed_fibroblasts',
    'Colon_Sigmoid',
    'Colon_Transverse',
    'Esophagus_Gastroesophageal_Junction',
    'Esophagus_Mucosa',
    'Esophagus_Muscularis',
    'Heart_Atrial_Appendage',
    'Heart_Left_Ventricle',
    'Liver',
    'Lung',
    'Muscle_Skeletal',
    'Nerve_Tibial',
    'Ovary',
    'Pancreas',
    'Pituitary',
    'Prostate',
    'Skin_Not_Sun_Exposed_Suprapubic',
    'Skin_Sun_Exposed_Lower_leg',
    'Small_Intestine_Terminal_Ileum',
    'Spleen',
    'Stomach',
    'Testis',
    'Thyroid',
    'Uterus',
    'Vagina',
    'Whole_Blood'
]
# File names for gene and snp annotation:
GENE_ANNOTATION_FN = 'gencode.v19.genes.v6p.patched_contigs.gtf'
SNP_ANNOTATION_FN = 'GTEx_OMNI_genot_1KG_imputed_var_info4_maf01_CR95_CHR_POSb37_ID_REF_ALT_release_v6.txt'
# List of genotype/expression file names:
GENOTYPE_FNS = [
    'Adipose_Subcutaneous_Analysis.snps.txt',
    'Adipose_Visceral_Omentum_Analysis.snps.txt',
    'Adrenal_Gland_Analysis.snps.txt',
    'Artery_Aorta_Analysis.snps.txt',
    'Artery_Coronary_Analysis.snps.txt',
    'Artery_Tibial_Analysis.snps.txt',
    'Brain_Anterior_cingulate_cortex_BA24_Analysis.snps.txt',
    'Brain_Caudate_basal_ganglia_Analysis.snps.txt',
    'Brain_Cerebellar_Hemisphere_Analysis.snps.txt',
    'Brain_Cerebellum_Analysis.snps.txt',
    'Brain_Cortex_Analysis.snps.txt',
    'Brain_Frontal_Cortex_BA9_Analysis.snps.txt',
    'Brain_Hippocampus_Analysis.snps.txt',
    'Brain_Hypothalamus_Analysis.snps.txt',
    'Brain_Nucleus_accumbens_basal_ganglia_Analysis.snps.txt',
    'Brain_Putamen_basal_ganglia_Analysis.snps.txt',
    'Breast_Mammary_Tissue_Analysis.snps.txt',
    'Cells_EBV-transformed_lymphocytes_Analysis.snps.txt',
    'Cells_Transformed_fibroblasts_Analysis.snps.txt',
    'Colon_Sigmoid_Analysis.snps.txt',
    'Colon_Transverse_Analysis.snps.txt',
    'Esophagus_Gastroesophageal_Junction_Analysis.snps.txt',
    'Esophagus_Mucosa_Analysis.snps.txt',
    'Esophagus_Muscularis_Analysis.snps.txt',
    'Heart_Atrial_Appendage_Analysis.snps.txt',
    'Heart_Left_Ventricle_Analysis.snps.txt',
    'Liver_Analysis.snps.txt',
    'Lung_Analysis.snps.txt',
    'Muscle_Skeletal_Analysis.snps.txt',
    'Nerve_Tibial_Analysis.snps.txt',
    'Ovary_Analysis.snps.txt',
    'Pancreas_Analysis.snps.txt',
    'Pituitary_Analysis.snps.txt',
    'Prostate_Analysis.snps.txt',
    'Skin_Not_Sun_Exposed_Suprapubic_Analysis.snps.txt',
    'Skin_Sun_Exposed_Lower_leg_Analysis.snps.txt',
    'Small_Intestine_Terminal_Ileum_Analysis.snps.txt',
    'Spleen_Analysis.snps.txt',
    'Stomach_Analysis.snps.txt',
    'Testis_Analysis.snps.txt',
    'Thyroid_Analysis.snps.txt',
    'Uterus_Analysis.snps.txt',
    'Vagina_Analysis.snps.txt',
    'Whole_Blood_Analysis.snps.txt'
]
EXPRESSION_FNS = [
    'Adipose_Subcutaneous_Analysis.expr.txt',
    'Adipose_Visceral_Omentum_Analysis.expr.txt',
    'Adrenal_Gland_Analysis.expr.txt',
    'Artery_Aorta_Analysis.expr.txt',
    'Artery_Coronary_Analysis.expr.txt',
    'Artery_Tibial_Analysis.expr.txt',
    'Brain_Anterior_cingulate_cortex_BA24_Analysis.expr.txt',
    'Brain_Caudate_basal_ganglia_Analysis.expr.txt',
    'Brain_Cerebellar_Hemisphere_Analysis.expr.txt',
    'Brain_Cerebellum_Analysis.expr.txt',
    'Brain_Cortex_Analysis.expr.txt',
    'Brain_Frontal_Cortex_BA9_Analysis.expr.txt',
    'Brain_Hippocampus_Analysis.expr.txt',
    'Brain_Hypothalamus_Analysis.expr.txt',
    'Brain_Nucleus_accumbens_basal_ganglia_Analysis.expr.txt',
    'Brain_Putamen_basal_ganglia_Analysis.expr.txt',
    'Breast_Mammary_Tissue_Analysis.expr.txt',
    'Cells_EBV-transformed_lymphocytes_Analysis.expr.txt',
    'Cells_Transformed_fibroblasts_Analysis.expr.txt',
    'Colon_Sigmoid_Analysis.expr.txt',
    'Colon_Transverse_Analysis.expr.txt',
    'Esophagus_Gastroesophageal_Junction_Analysis.expr.txt',
    'Esophagus_Mucosa_Analysis.expr.txt',
    'Esophagus_Muscularis_Analysis.expr.txt',
    'Heart_Atrial_Appendage_Analysis.expr.txt',
    'Heart_Left_Ventricle_Analysis.expr.txt',
    'Liver_Analysis.expr.txt',
    'Lung_Analysis.expr.txt',
    'Muscle_Skeletal_Analysis.expr.txt',
    'Nerve_Tibial_Analysis.expr.txt',
    'Ovary_Analysis.expr.txt',
    'Pancreas_Analysis.expr.txt',
    'Pituitary_Analysis.expr.txt',
    'Prostate_Analysis.expr.txt',
    'Skin_Not_Sun_Exposed_Suprapubic_Analysis.expr.txt',
    'Skin_Sun_Exposed_Lower_leg_Analysis.expr.txt',
    'Small_Intestine_Terminal_Ileum_Analysis.expr.txt',
    'Spleen_Analysis.expr.txt',
    'Stomach_Analysis.expr.txt',
    'Testis_Analysis.expr.txt',
    'Thyroid_Analysis.expr.txt',
    'Uterus_Analysis.expr.txt',
    'Vagina_Analysis.expr.txt',
    'Whole_Blood_Analysis.expr.txt'
]
COVARIATE_FNS = [
    'Adipose_Subcutaneous_Analysis.covariates.txt',
    'Adipose_Visceral_Omentum_Analysis.covariates.txt',
    'Adrenal_Gland_Analysis.covariates.txt',
    'Artery_Aorta_Analysis.covariates.txt',
    'Artery_Coronary_Analysis.covariates.txt',
    'Artery_Tibial_Analysis.covariates.txt',
    'Brain_Anterior_cingulate_cortex_BA24_Analysis.covariates.txt',
    'Brain_Caudate_basal_ganglia_Analysis.covariates.txt',
    'Brain_Cerebellar_Hemisphere_Analysis.covariates.txt',
    'Brain_Cerebellum_Analysis.covariates.txt',
    'Brain_Cortex_Analysis.covariates.txt',
    'Brain_Frontal_Cortex_BA9_Analysis.covariates.txt',
    'Brain_Hippocampus_Analysis.covariates.txt',
    'Brain_Hypothalamus_Analysis.covariates.txt',
    'Brain_Nucleus_accumbens_basal_ganglia_Analysis.covariates.txt',
    'Brain_Putamen_basal_ganglia_Analysis.covariates.txt',
    'Breast_Mammary_Tissue_Analysis.covariates.txt',
    'Cells_EBV-transformed_lymphocytes_Analysis.covariates.txt',
    'Cells_Transformed_fibroblasts_Analysis.covariates.txt',
    'Colon_Sigmoid_Analysis.covariates.txt',
    'Colon_Transverse_Analysis.covariates.txt',
    'Esophagus_Gastroesophageal_Junction_Analysis.covariates.txt',
    'Esophagus_Mucosa_Analysis.covariates.txt',
    'Esophagus_Muscularis_Analysis.covariates.txt',
    'Heart_Atrial_Appendage_Analysis.covariates.txt',
    'Heart_Left_Ventricle_Analysis.covariates.txt',
    'Liver_Analysis.covariates.txt',
    'Lung_Analysis.covariates.txt',
    'Muscle_Skeletal_Analysis.covariates.txt',
    'Nerve_Tibial_Analysis.covariates.txt',
    'Ovary_Analysis.covariates.txt',
    'Pancreas_Analysis.covariates.txt',
    'Pituitary_Analysis.covariates.txt',
    'Prostate_Analysis.covariates.txt',
    'Skin_Not_Sun_Exposed_Suprapubic_Analysis.covariates.txt',
    'Skin_Sun_Exposed_Lower_leg_Analysis.covariates.txt',
    'Small_Intestine_Terminal_Ileum_Analysis.covariates.txt',
    'Spleen_Analysis.covariates.txt',
    'Stomach_Analysis.covariates.txt',
    'Testis_Analysis.covariates.txt',
    'Thyroid_Analysis.covariates.txt',
    'Uterus_Analysis.covariates.txt',
    'Vagina_Analysis.covariates.txt',
    'Whole_Blood_Analysis.covariates.txt'
]

# Model metadata/parameters. Keep all as strings:
SNPSET = '1KG'
ALPHA = '0.5'
N_K_FOLDS = '10'
RSID_LABEL = 'RS_ID_dbSNP142_CHG37p13'
WINDOW = '1e6'
SEEDS = [
    [371,783,1179,1127,338,1555,1427,363,741,588,1299,2013,1184,1559,1447,1315,843,123,215,1968,610,832],
    [454,424,1595,606,696,1095,285,472,1578,1553,1920,1438,1912,1720,494,413,653,138,819,1870,679,353],
    [1675,405,378,1780,616,266,1692,278,1231,1358,485,1032,932,1007,1683,524,1872,1749,1985,278,1935,1071],
    [1810,467,1744,1420,1494,958,1932,1772,882,1050,855,2003,672,1182,809,659,1180,1859,1193,886,881,627],
    [145,1330,1774,876,1427,1785,36,592,1620,1800,832,1985,165,843,353,129,235,853,1032,1213,595,247],
    [770,1060,1937,182,614,1758,756,1606,1115,100,919,488,423,374,1113,66,1483,637,886,695,374,298],
    [1888,1966,1531,496,1206,31,1657,1642,767,1453,380,1717,775,1166,454,54,1946,184,125,1942,826,91],
    [730,957,857,1988,99,268,1321,1792,1562,1189,1687,656,572,1105,470,1708,24,81,1035,430,1277,442],
    [532,850,428,162,1222,103,1897,687,920,848,1554,1010,1516,450,84,1740,383,1324,244,1433,1289,172],
    [1161,80,1027,1662,325,1329,750,1751,1945,104,658,1052,188,1508,1763,84,1611,1822,1905,123,403,1826],
    [962,1014,1612,518,397,1940,1387,813,1594,562,690,968,668,1961,273,235,1473,914,1655,1592,19,228],
    [189,1515,45,879,1544,890,111,1779,678,1093,105,1143,527,150,48,1043,1329,1024,217,1347,1768,382],
    [808,1390,1216,1351,614,1542,1392,535,568,1509,985,1413,1714,1108,566,1691,481,610,988,1830,488,817],
    [1715,1260,1303,1808,1506,1619,1516,144,997,717,882,1848,659,1916,1578,219,1723,1894,750,764,1237,1590],
    [326,88,662,35,374,1792,2000,583,580,1714,1056,1060,1948,316,1326,725,1810,220,294,1282,194,1237],
    [366,1795,2005,755,995,144,822,1273,1322,1751,1908,1793,356,127,1881,1199,1437,1917,957,186,721,238],
    [1664,1705,1785,1922,1736,731,1610,1425,608,651,1348,1941,1150,871,822,1665,1685,435,696,1805,361,1336],
    [441,1687,809,1353,249,639,1024,576,1325,951,1599,990,98,91,1909,438,512,1494,1026,1335,1542,1323],
    [1038,423,887,1172,520,1214,1226,1626,1106,722,74,738,727,1561,1486,532,665,185,1147,1516,208,1350],
    [1687,1245,1696,1960,1425,1958,1285,1054,1567,581,1587,1984,9,1378,709,855,303,1480,630,1825,936,1308],
    [379,1340,326,751,210,524,1354,2014,1685,1969,1815,1045,88,1128,1276,456,696,39,36,73,514,370],
    [79,465,348,1720,1476,1140,1458,417,242,1851,1951,416,1947,1019,1035,508,781,1734,506,960,424,968],
    [1017,1528,270,340,645,1354,1828,448,1208,598,463,384,1756,1540,444,1490,1513,923,1534,1335,1420,1863],
    [825,826,618,137,619,1120,268,835,1173,429,1809,1836,1033,1404,578,617,832,1231,1158,1011,1211,1779],
    [444,395,11,497,368,184,1617,1309,1295,1575,1900,696,1266,1277,515,20,958,1815,769,595,459,1134],
    [1055,1309,1246,1563,808,187,1943,347,1650,1075,528,1461,1267,464,358,1520,1851,387,1002,180,123,962],
    [645,419,1485,468,911,1258,1676,1993,1727,454,189,62,53,705,1424,427,1666,1131,948,136,1500,622],
    [671,1116,1959,471,1706,1520,1034,1089,1874,570,1306,1640,47,1552,1941,213,1893,53,271,1701,442,1248],
    [1539,1607,504,1132,677,1309,1586,1858,180,1697,1204,438,1390,1446,1693,1526,1211,1302,745,961,1750,171],
    [1231,1904,1839,1408,264,1746,875,1823,1645,550,1191,340,1832,291,664,328,188,1687,1201,1594,249,600],
    [95,435,1200,1622,2008,841,1986,855,440,1507,659,702,1234,1335,383,1488,1374,294,284,289,896,1378],
    [201,676,1513,266,1023,322,1575,1923,318,30,145,52,1278,1576,1966,1367,819,1605,956,785,1480,1397],
    [867,1008,464,1829,259,574,1450,597,1902,120,890,398,1276,825,1297,2005,1648,1809,286,1088,1780,1353],
    [1667,136,1902,1442,1321,768,785,11,1936,1069,301,1230,1425,1906,437,1733,52,613,1864,1347,1689,2004],
    [721,1286,1065,873,298,397,426,1174,1630,1187,1928,1734,948,1652,132,1699,1110,1714,1471,503,359,985],
    [856,1807,1713,1239,1025,1556,1015,562,1586,911,1093,1782,371,1270,1133,160,596,1396,58,170,458,738],
    [1851,1357,821,1631,147,744,1413,79,1798,599,991,375,1278,1230,1243,994,526,87,1158,304,964,300],
    [1260,1697,1326,31,261,1402,1414,877,1273,1531,1307,1244,330,1738,1011,196,909,176,1447,293,1421,715],
    [115,601,398,987,2,1629,671,1471,1849,124,1876,1169,1159,1204,839,1401,1414,170,194,1358,1631,1622],
    [1685,1577,1852,1787,273,1425,490,525,1962,1266,1877,755,177,228,13,1830,808,1650,1450,661,1613,272],
    [1419,200,1028,25,885,307,781,847,1133,1479,419,1634,990,1252,524,1216,68,390,1518,1291,1122,214],
    [1679,1654,819,664,1993,517,1673,1641,1373,1331,987,1314,1836,880,1043,115,1777,348,1812,1098,339,1034],
    [1319,1719,2010,419,1196,1362,1782,257,183,1940,1646,1724,1163,661,186,1657,1680,1298,820,783,1584,1527],
    [1558,1668,69,1483,971,1561,1616,179,1618,363,1222,211,714,678,232,1810,1042,429,1870,1987,1639,1133]
]
# Leave everything below here as is------------------------------------/

# Names for intermediate files-----------------------------------------/
# File name of output for parse_gtf.py:
GENE_ANNOT_INTER1 = GENE_ANNOTATION_FN[:-3] + 'parsed.txt'
# File name of output for geno_annot_to_RDS.R:
GENE_ANNOT_INTER2 = GENE_ANNOT_INTER1[:-3] + 'RDS'
# File name prefix of outputs from split_snp_annot_by_chr.py:
SNP_ANN_INTER_PREFIX1 = SNP_ANNOTATION_FN[:-4]
# File name prefix for input files to snp_annot_to_RDS.R:
SNP_ANN_INTER_PREFIX2 = SNP_ANN_INTER_PREFIX1 + '.chr'
# File name prefixes for output files from split_genotype_by_chr.py:
GENOTYPE_INTER_PREFIX = map(lambda x: x[:-4], GENOTYPE_FNS)
# File names for output files from expr_to_transposed_RDS.R:
EXPR_INTER = map(lambda x: x[:-3] + "RDS", EXPRESSION_FNS)

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
FILTERED_DB_FILES = map(lambda x: x[:-3] + '_filtered.db', DB_FILES)
