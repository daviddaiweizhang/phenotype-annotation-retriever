#! /bin/bash
set -e

output_correct=$( mktemp )
output_hg38=$( mktemp )
output_hg19=$( mktemp )
output_rsid=$( mktemp )

echo 'Testing phenotype annotation retriever...'

echo 'Dementias|Hyperlipidemia|DisordersOfLipoidMetabolism|DeliriumDementiaAndAmnesticAndOtherCognitiveDisorders|Hypercholesterolemia|AlzheimerSDisease|CoronaryAtherosclerosis|VascularDementia|IschemicHeartDisease|MyocardialInfarction' > $output_correct
./retrieve.py --chrom=19 --pos=44908684 --ref-allele=T --alt-allele=C --ref-genome=hg38 > $output_hg38
./retrieve.py --chrom=19 --pos=45411941 --ref-allele=T --alt-allele=C --ref-genome=hg19 > $output_hg19
./retrieve.py --rsid=rs429358 > $output_rsid
cmp $output_correct $output_hg38
cmp $output_correct $output_hg19
cmp $output_correct $output_rsid

echo 'Passed!'
