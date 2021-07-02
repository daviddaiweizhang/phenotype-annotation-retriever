#! /usr/bin/env python

import argparse

import requests
from pyliftover import LiftOver

from converters import rsid_to_coordinate


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
        phenos_top_str = ''
    else:
        phenos = [
                pheno['phenostring'].replace(' ', '-')
                for pheno in info['phenos']]
        pvals = [
                pheno['pval']
                for pheno in info['phenos']]

        phenos_signi = [
                pheno for pval, pheno
                in sorted(zip(pvals, phenos))
                if pval < pval_threshold]
        phenos_top = phenos_signi[:n_top_pheno]
        phenos_top_str = '|'.join(phenos_top)
    return phenos_top_str


def get_pheno_annot_from_rsid(rsid, reference_genome):
    chrom, pos, ref_allele, alt_allele = rsid_to_coordinate(
            rsid=rsid,
            reference_genome=reference_genome)
    print(chrom, pos, ref_allele, alt_allele)
    return get_pheno_annot(
        chrom=chrom,
        pos=pos,
        ref_allele=ref_allele,
        alt_allele=alt_allele,
        reference_genome=reference_genome)


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
            '--reference-genome',
            help=(
                'Build of the reference genome. '
                'Example: hg19. '))
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
                reference_genome=args['reference_genome'])
    else:
        pheno_annot = get_pheno_annot_from_rsid(
                rsid=args['rsid'],
                reference_genome='hg38')
    print(pheno_annot)


if __name__ == '__main__':
    main()
