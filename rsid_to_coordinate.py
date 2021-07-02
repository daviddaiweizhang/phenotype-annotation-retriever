#! /usr/bin/env python

import argparse

import mysql.connector


def rsid_to_coordinate(
        rsid,
        ref_genome,
        dbsnp='snp151'):

    # connect to server
    cnx = mysql.connector.connect(
            host='genome-mysql.cse.ucsc.edu',
            user='genome',
            database=ref_genome)
    # get a cursor
    cur = cnx.cursor()
    # search for SNP by rsid
    cols = 'chrom,chromStart,chromEnd,observed,alleles,alleleFreqs'
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
        matched = matched[0]
        chrom_str, start, end, alleles_str = matched[:-2]
        allele_freqs_names, allele_freqs_vals = [
                e.decode('ascii').split(',')[:-1]
                for e in matched[-2:]]

        # get SNP chromosome
        chrom = int(chrom_str[3:])

        # get SNP position
        if end - start != 1:
            print('Warning: SNP length not equal to one.')
        pos = end

        # get SNP alleles
        alleles = alleles_str.split('/')
        # sort alleles by frequencies
        if len(allele_freqs_names) > 0:
            assert len(allele_freqs_names) == len(alleles)
            assert set(allele_freqs_names) == set(alleles)
            alleles_sorted = [e for _, e in sorted(
                zip(allele_freqs_vals, allele_freqs_names),
                reverse=True)]
        # get first two alleles
        if len(alleles_sorted) != 2:
            print('Warning: SNP is not bi-allelic.')
        ref_allele, alt_allele = alleles_sorted[:2]

    return chrom, pos, ref_allele, alt_allele


def coordinate_to_str(chrom, pos, ref_allele, alt_allele):
    return f'{chrom} {pos} {ref_allele} {alt_allele}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'rsid',
            help=(
                'rsid of the SNP. '
                'Example: rs429358. '))
    parser.add_argument(
            'ref_genome',
            help=(
                'Build of the ref genome. '
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
