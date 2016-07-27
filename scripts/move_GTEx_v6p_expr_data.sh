#!/bin/bash
cd /group/im-lab/nas40t2/Data/dbGaP/GTEx/50852/gtex/exchange/GTEx_phs000424/exchange/subgroups/eqtl/v6p_fastQTL_FOR_QC_ONLY
for expr_file in $(ls *.bed)
do
    zcat $expr_file | cut -f1-3 --complement > /group/im-lab/nas40t2/scott/modelpipeline/data/input/expression_phenotypes/${expr_file/\.v6p\.FOR_QC_ONLY\.normalized\.expr\.bed/.expr.txt}
done
