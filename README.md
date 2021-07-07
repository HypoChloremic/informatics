# informatics
Informatic processing, for doing e.g. meta-searches on genes

## Uniprot

Performs searches in the uniprot database

### Basic search
#### Command line 
```bash
>> python uniprot/search.py --genes APOE MYL2 DCN

[outputs the vals in string format]
```

#### In python

```python
from uniprot.search import Uniprot

uni = Uniprot()
uni.gene_search(["MYL2", "APOE"])
d = uni.extract_function()
``` 
