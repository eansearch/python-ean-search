#!/usr/bin/env python

from eansearch import EANSearch

# API token for ean-search.org account
# https://www.ean-search.org/ean-database-api.html
apiToken = "secret"
ean = "5099750442227" # Thriller
#ean = "5099750442228" # error

eansearch = EANSearch(apiToken)

name = eansearch.barcodeLookup(ean)
print(ean, " is ", name)

# more detailed result, preferrably in English (1)
product = eansearch.barcodeSearch(ean, 1)
print(ean, " is ", product["name"].encode("utf-8"), " from category ", product["categoryName"], " issued in ", product["issuingCountry"])

ok = eansearch.verifyChecksum(ean)
print(ean, " is ", "OK" if ok else "Not OK")

eanList = eansearch.productSearch('iPod');
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.barcodePrefixSearch('4007249146');
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

