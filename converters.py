#! /usr/bin/env python

import mysql.connector
import argparse


def rsid_to_coordinate(
        rsid,
        reference_genome,
        dbsnp='snp151'):

    # connect to server
    cnx = mysql.connector.connect(
            host='genome-mysql.cse.ucsc.edu',
            user='genome',
            database=reference_genome)
    # get a cursor
    cur = cnx.cursor()
    # search for SNP by rsid
    cols = 'chrom,chromStart,chromEnd,observed'
    cur.execute(f'select {cols} from {dbsnp} where name = "{rsid}"')
    # fetch matched entries
    matched = cur.fetchall()
    # close connection
    cnx.close()

    # delimit matched entries
    if len(matched) == 0:
        print('SNP not found.')
    else:
        if len(matched) > 1:
            print('Warning: multiple SNPs found.')
        chrom_str, start, end, alleles_str = matched[0]

        # get SNP chromosome
        chrom = int(chrom_str[3:])

        # get SNP position
        if end - start != 1:
            print('Warning: SNP length not equal to one.')
        pos = end

        # get SNP alleles
        alleles = alleles_str.split('/')
        if len(alleles) != 2:
            print('Warning: SNP is not bi-allelic.')
        ref_allele, alt_allele = alleles[:2]

    return chrom, pos, ref_allele, alt_allele


def coordinate_to_str(chrom, pos, ref_allele, alt_allele):
    return f'{chrom}_{pos}_{ref_allele}_{alt_allele}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'rsid',
            help=(
                'rsid of the SNP. '
                'Example: rs371194064. '))
    parser.add_argument(
            'reference_genome',
            help=(
                'Build of the reference genome. '
                'Examples: hg19, hg38. '))
    parser.add_argument(
            '--dbsnp',
            default='snp151',
            help=(
                'Build of dbSNP. '
                'Examples: snp151, snp150, snp147. '
                'Default: snp151. '))
    args = vars(parser.parse_args())
    coordinate = rsid_to_coordinate(**args)
    coordiante_str = coordinate_to_str(*coordinate)
    print(coordiante_str)


if __name__ == '__main__':
    main()
