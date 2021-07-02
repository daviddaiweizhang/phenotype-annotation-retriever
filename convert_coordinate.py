#! /usr/bin/env python

import argparse

from pyliftover import LiftOver


def convert_coordinate(
        chrom, pos, build_in, build_out):
    lo = LiftOver(build_in, build_out)
    output = lo.convert_coordinate(f'chr{chrom}', pos)
    pos_converted = output[0][1]
    return chrom, pos_converted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'chrom',
            type=int,
            help=(
                'Chromosome of the input coordinate. '
                'Example: 19. '))
    parser.add_argument(
            'pos',
            type=int,
            help=(
                'Position of the input coordinate.'
                'Example: 44908684. '))
    parser.add_argument(
            'build_in',
            help=(
                'Reference genome of the input coordinate. '
                'Example: hg38. '))
    parser.add_argument(
            'build_out',
            help=(
                'Reference genome of the output coordinate. '
                'Example: hg19. '))
    args = vars(parser.parse_args())
    chrom_out, pos_out = convert_coordinate(**args)
    print(chrom_out, pos_out, args['build_out'])


if __name__ == '__main__':
    main()
