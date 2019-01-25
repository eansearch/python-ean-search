#!/usr/bin/env python

# Python 2.7
#from eansearch2 import EANSearch
# Python 3.x
from eansearch3 import EANSearch

# API token for ean-search.org account
# https://www.ean-search.org/ean-database-api.html
apiToken = "secret"
ean = "5099750442227" # Thriller
#ean = "5099750442228" # error

eansearch = EANSearch(apiToken)

name = eansearch.barcodeLookup(ean)
print(ean, " is ", name)

ok = eansearch.verifyChecksum(ean)
print(ean, " is ", "OK" if ok else "Not OK")

eanList = eansearch.productSearch('iPod');
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.barcodePrefixSearch('4007249146');
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

