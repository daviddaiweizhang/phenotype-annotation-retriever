#! /usr/bin/env python

import sys

import requests
from pyliftover import LiftOver


def convert_coordinate(
        chrom, pos, build_in, build_out):
    lo = LiftOver(build_in, build_out)
    output = lo.convert_coordinate(f'chr{chrom}', pos)
    pos_converted = output[0][1]
    return chrom, pos_converted


def get_pheno_annot(
        chrom, pos, ref, alt, snp_build,
        n_top_pheno=10, pval_threshold=0.05,
        gwas_name='UKB-TOPMed', gwas_build='hg38'):

    if snp_build != gwas_build:
        pos = convert_coordinate(
                chrom, pos,
                build_in=snp_build, build_out=gwas_build)[1]
    snp = f'{chrom}:{pos}-{ref}-{alt}'
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
    chrom = int(sys.argv[1])  # e.g. 3
    pos = int(sys.argv[2])  # e.g. 152567908
    ref = sys.argv[3]  # e.g. 'C'
    alt = sys.argv[4]  # e.g. 'A'
    snp_build = sys.argv[5]  # e.g. 'hg19'
    pheno_annot = get_pheno_annot(
            chrom=chrom, pos=pos,
            ref=ref, alt=alt, snp_build=snp_build)
    print(pheno_annot)


if __name__ == '__main__':
    main()
