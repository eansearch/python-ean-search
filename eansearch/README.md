# EANSearch

A Python class for EAN and ISBN name lookup and validation using the API on https://www.ean-search.org

Compatible with Python 2.x **and** 3.x

```python
from eansearch import EANSearch

# get a token from https://www.ean-search.org/ean-database-api.html
apiToken = "secret"
ean = "5099750442227" # Thriller

lookup = EANSearch(apiToken)

name = lookup.barcodeLookup(ean)
print(ean, " is ", name)

ok = lookup.verifyChecksum(ean)
print(ean, " is ", "OK" if ok else "Not OK")

eanList = eansearch.productSearch('iPod');
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.barcodePrefixSearch('4007249146');
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

