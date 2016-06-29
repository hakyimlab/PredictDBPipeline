#!/usr/bin/env python

"""
Program to build the directory structure if needed and put data in
correct location.

Author: Scott Dickinson <spdickinson88@gmail.com>
"""

import argparse
import os
import shutil
import tarfile


class DirectoryFramework:

    def __init__(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = os.path.normpath(this_dir + "/../data/")
        self.jobs_dir = os.path.normpath(this_dir + "/../joblogs/")

        def data_path(child_dirs):
            return os.path.join(self.data_dir, child_dirs)

        self.input_dir_dict = {
            "snp_ann": data_path("input/annotations/snp_annotation/"),
            "gene_ann": data_path("input/annotations/gene_annotation/"),
            "expr": data_path("input/expression_phenotypes/"),
            "geno": data_path("input/genotypes/")
        }

        self.inter_dir_dict = {
            "snp_ann": data_path("intermediate/annotations/snp_annotation/"),
            "gene_ann": data_path("intermediate/annotations/gene_annotation/"),
            "expr": data_path("intermediate/expression_phenotypes/"),
            "geno": data_path("intermediate/genotypes/"),
            "models": data_path("intermediate/model_by_chr/")
        }

        self.output_dir_dict = {
            "betas": data_path("output/allBetas/"),
            "logs": data_path("output/allLogs/"),
            "meta": data_path("output/allMetaData/"),
            "results": data_path("output/allResults/"),
            "dbs": data_path("output/dbs/")
        }

    def build_directories(self):
        """Builds directory structure needed for pipeline"""
        if not os.path.exists(self.data_dir):
            print("Creating data directory structure...")
            for k in self.input_dir_dict:
                os.makedirs(self.input_dir_dict[k])
            for k in self.inter_dir_dict:
                os.makedirs(self.inter_dir_dict[k])
            for k in self.output_dir_dict:
                os.makedirs(self.output_dir_dict[k])
        else:
            print("data/ directory already exists")

        if not os.path.exists(self.jobs_dir):
            print("Creating joblogs directory...")
            os.makedirs(self.jobs_dir)
        else:
            print("joblogs/ directory already exists")

    def smart_move(self, fname, ftype):
        """Move a file to correct location and extract it if needed"""
        if fname.endswith("tar.gz"):
            tar = tarfile.open(fname, "r:gz")
            tar.extractall(path=self.input_dir_dict[ftype])
            tar.close()
        elif fname.endswith("tar"):
            tar = tarfile.open(fname, "r:")
            tar.extractall(path=self.input_dir_dict[ftype])
            tar.close()
        else:
            # Only make symbolic links to save space if not decompressing.
            os.symlink(fname, self.input_dir_dict[ftype] + '/' + fname)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gene_annotation', action='store',
                        dest='gene_ann', default=None)
    parser.add_argument('--snp_annotation', action='store',
                        dest='snp_ann', default=None)
    parser.add_argument('--genotype', action='store',
                        dest='geno', default=None)
    parser.add_argument('--expression', action='store',
                        dest='expr', default=None)
    parser.add_argument('--covariate', action='store',
                        dest='cov', default=None)

    args = parser.parse_args()

    gene_ann_src = args.gene_ann
    snp_ann_src = args.snp_ann
    geno_src = args.geno
    expr_src = args.expr
    cov_src = args.cov

    directory_framework = DirectoryFramework()
    directory_framework.build_directories()

    if gene_ann_src:
        directory_framework.smart_move(gene_ann_src, 'gene_ann')
    if snp_ann_src:
        directory_framework.smart_move(snp_ann_src, 'snp_ann')
    if geno_src:
        directory_framework.smart_move(geno_src, 'geno')
    if expr_src:
        directory_framework.smart_move(expr_src, 'expr')
    if cov_src:
        # Move covariate files to expression directory for ease of processing.
        directory_framework.smart_move(cov_src, 'expr')
    


if __name__ == "__main__":
    main()
