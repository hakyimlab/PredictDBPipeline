#!/usr/bin/env python
import argparse

HEADER_FIELDS = ['n_samples', 'n_folds_cv', 'snpset', 'rsid_db_snp_label',
                'alpha', 'window']

def get_sample_size(expression_file, genotype_file):
    '''Returns how many samples are common between the expression
    data and phenotype data'''

    def get_samples(fh):
        samples_list = fh.readline().strip().split()
        # First column has heading something like 'ID'
        # Only include fields after this.
        return set(samples_list[1:])

    with open(expression_file, 'r') as ef, open(genotype_file, 'r') as gf:
        ef_samples = get_samples(ef)
        gf_samples = get_samples(gf)
    return len(ef_samples & gf_samples)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--geno', required=True, help='genotype file for sample size')
    parser.add_argument('--expr', required=True, help='expression file for sample size')
    parser.add_argument('--snpset', required=True, help='SNP set used for analysis (e.g. 1KG, HapMap')
    parser.add_argument('--alpha', default='0.5', help='Alpha value for glmnet')
    parser.add_argument('--n_k_folds', default='10', help='Number of folds for cross-validation')
    parser.add_argument('--rsid_label', required=True, help='rsid version number')
    parser.add_argument('--window', required=True, help='Number of base pairs to look upstream of TSS and downstream of TTS for ciseqtls')
    parser.add_argument('--out_prefix', required=True, help='Prefix for output file')

    args = parser.parse_args()

    out_file = args.out_prefix + '.allMetaData.txt'
    n_samples = str(get_sample_size(args.expr, args.geno))
    meta_data = [n_samples, args.n_k_folds, args.snpset, args.rsid_label,
                args.alpha, args.window]
    with open(out_file, 'w') as out:
        out.write('\t'.join(HEADER_FIELDS) + '\n')
        out.write('\t'.join(meta_data) + '\n')
