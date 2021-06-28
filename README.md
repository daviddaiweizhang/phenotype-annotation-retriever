# Phenotype Annotation Retriever

This program provides the phenotypes associated with a given SNP.
The association information is retrieved from 
from the [Michigan Genomics Initiative PheWeb](http://pheweb.sph.umich.edu/).
For example,
```
./retrieve.py 3 152567908 C A hg19
```
generates a list of diseases associated with the SNP
located on chromosome 3 at location 152567908 (hg19 build),
with reference allele C and alternative allele A.

## Prerequisites
To install the required Python modules, run
```
pip install -r requirements.txt
```

## Acknoledgement

We would like to thank
[Peter VandeHaar](https://github.com/pjvandehaar)
for his help with PheWeb.
