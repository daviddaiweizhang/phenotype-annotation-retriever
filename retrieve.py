#! /usr/bin/env python

import argparse

import requests
from pyliftover import LiftOver


def convert_coordinate(
        chrom, pos, build_in, build_out):
    lo = LiftOver(build_in, build_out)
    output = lo.convert_coordinate(f'chr{chrom}', pos)
    pos_converted = output[0][1]
    return chrom, pos_converted


def get_pheno_annot(
        chrom, pos, ref_allele, alt_allele, reference_genome,
        n_top_pheno=10, pval_threshold=0.05,
        gwas_name='UKB-TOPMed', gwas_build='hg38'):

    if reference_genome != gwas_build:
        pos = convert_coordinate(
                chrom, pos,
                build_in=reference_genome,
                build_out=gwas_build)[1]
    snp = f'{chrom}:{pos}-{ref_allele}-{alt_allele}'
    url = f'https://pheweb.org/{gwas_name}/api/variant/{snp}'
    info = requests.get(url).json()

    if info is None:
        signi_pheno_list = []
    else:
        signi_pheno_list = [
            pheno['phenostring'].replace(' ', '-')
            for pheno in info['phenos']
            if pheno['pval'] < pval_threshold]
    strong_pheno_str = '|'.join(signi_pheno_list[:n_top_pheno])
    return strong_pheno_str


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
            'chrom',
            type=int,
            help=(
                'Chromosome of the SNP. '
                'Example: 3. '))
    parser.add_argument(
            'pos',
            type=int,
            help=(
                'Position of the SNP on the chromosome. '
                'Example: 152567908. '))
    parser.add_argument(
            'ref_allele',
            help=(
                'Reference allele of the SNP. '
                'Example: C. '))
    parser.add_argument(
            'alt_allele',
            help=(
                'Alternative allele of the SNP. '
                'Example: A. '))
    parser.add_argument(
            'reference_genome',
            help=(
                'Build of the reference genome. '
                'Example: hg19'))
    args = vars(parser.parse_args())

    pheno_annot = get_pheno_annot(**args)
    print(pheno_annot)


if __name__ == '__main__':
    main()
