# Phenotype Annotation Retriever

This program provides the phenotypes associated with a given SNP.
The association information is retrieved from 
from the [Michigan Genomics Initiative PheWeb](http://pheweb.sph.umich.edu/).

## Prerequisites
To install the required Python modules, run
```
pip install -r requirements.txt
```

## Examples
To retrieve phenotype information,
the SNP can be defined by coordinate, e.g.
```
./retrieve.py --chrom=19 --pos=44908684 --ref-allele=T --alt-allele=C --ref-genome=hg38

# Output: Dementias|Hyperlipidemia|DisordersOfLipoidMetabolism|DeliriumDementiaAndAmnesticAndOtherCognitiveDisorders|Hypercholesterolemia|AlzheimerSDisease|CoronaryAtherosclerosis|VascularDementia|IschemicHeartDisease|MyocardialInfarction
```
or by rsid, e.g.
```
./retrieve.py --rsid=rs429358

# Output: Dementias|Hyperlipidemia|DisordersOfLipoidMetabolism|DeliriumDementiaAndAmnesticAndOtherCognitiveDisorders|Hypercholesterolemia|AlzheimerSDisease|CoronaryAtherosclerosis|VascularDementia|IschemicHeartDisease|MyocardialInfarction
```

## Acknoledgement

We would like to thank
[Peter VandeHaar](https://github.com/pjvandehaar)
for his help with PheWeb.
