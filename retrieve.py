#! /usr/bin/env python

import argparse

import requests

from convert_coordinate import convert_coordinate
from converters import rsid_to_coordinate


def get_pheno_annot(
        chrom, pos, ref_allele, alt_allele, ref_genome,
        n_top_pheno=10, pval_threshold=0.05,
        gwas_name='UKB-TOPMed', gwas_build='hg38'):

    if ref_genome != gwas_build:
        pos = convert_coordinate(
                chrom, pos,
                build_in=ref_genome,
                build_out=gwas_build)[1]
    snp = f'{chrom}:{pos}-{ref_allele}-{alt_allele}'
    url = f'https://pheweb.org/{gwas_name}/api/variant/{snp}'
    info = requests.get(url).json()

    if info is None:
        phenos_top_str = ''
    else:
        # retrieve phenotype names
        phenos = [
                pheno['phenostring']
                for pheno in info['phenos']]
        # retrieve phenotype pvalues
        pvals = [
                pheno['pval']
                for pheno in info['phenos']]
        # sort by pvalues and filter by significance
        phenos_signi = [
                pheno for pval, pheno
                in sorted(zip(pvals, phenos))
                if pval < pval_threshold]
        # select the top phenotypes
        phenos_top = phenos_signi[:n_top_pheno]
        # convert to camel case, remove punctuations, concat
        phenos_top_str = '|'.join([''.join(filter(
                str.isalnum, pheno.title().replace(' ', '')))
                for pheno in phenos_top])
    return phenos_top_str


def get_pheno_annot_from_rsid(rsid, ref_genome):
    chrom, pos, ref_allele, alt_allele = rsid_to_coordinate(
            rsid=rsid,
            ref_genome=ref_genome)
    return get_pheno_annot(
        chrom=chrom,
        pos=pos,
        ref_allele=ref_allele,
        alt_allele=alt_allele,
        ref_genome=ref_genome)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--chrom',
            type=int,
            help=(
                'Chromosome of the SNP. '
                'Example: 19. '))
    parser.add_argument(
            '--pos',
            type=int,
            help=(
                'Position of the SNP on the chromosome. '
                'Example: 44908684. '))
    parser.add_argument(
            '--ref-allele',
            help=(
                'Reference allele of the SNP. '
                'Example: T. '))
    parser.add_argument(
            '--alt-allele',
            help=(
                'Alternative allele of the SNP. '
                'Example: C. '))
    parser.add_argument(
            '--ref-genome',
            help=(
                'Build of the reference genome. '
                'Example: hg38. '))
    parser.add_argument(
            '--rsid',
            help=(
                'rsid of the SNP. '
                'Example: rs429358. '))
    args = vars(parser.parse_args())

    if args['rsid'] is None:
        pheno_annot = get_pheno_annot(
                chrom=args['chrom'],
                pos=args['pos'],
                ref_allele=args['ref_allele'],
                alt_allele=args['alt_allele'],
                ref_genome=args['ref_genome'])
    else:
        pheno_annot = get_pheno_annot_from_rsid(
                rsid=args['rsid'],
                ref_genome='hg38')
    print(pheno_annot)


if __name__ == '__main__':
    main()
