#! /usr/bin/env python

from pyliftover import LiftOver


def convert_coordinate(
        chrom, pos, build_in, build_out):
    lo = LiftOver(build_in, build_out)
    output = lo.convert_coordinate(f'chr{chrom}', pos)
    pos_converted = output[0][1]
    return chrom, pos_converted
