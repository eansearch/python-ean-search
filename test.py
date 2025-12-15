#!/usr/bin/env python3

import os
from eansearch import EANSearch

# API token for ean-search.org account
# https://www.ean-search.org/ean-database-api.html
apiToken = os.environ['EAN_SEARCH_API_TOKEN']
ean = "5099750442227" # Thriller
#ean = "5099750442228" # error
#ean = "195949821844" # 12-digit UPC
#ean = "5-099750442227" # extra char

eansearch = EANSearch(apiToken)

name = eansearch.barcodeLookup(ean)
print(ean + " is " + name)

# more detailed result, preferably in English (1)
product = eansearch.barcodeSearch(ean, 1)
print(ean, "is", product["name"].encode("utf-8"), "from category", product["categoryName"], "(Google ID", product["googleCategoryId"], ") issued in", product["issuingCountry"])

isbn = "1119578884"
title = eansearch.isbnLookup(isbn)
print(isbn, " is ", title)

ok = eansearch.verifyChecksum(ean)
print(ean, " is ", "OK" if ok else "Not OK")

eanList = eansearch.productSearch('iPod')
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.similarProductSearch('iPod with extra features')
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.categorySearch(45, 'thriller')
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.barcodePrefixSearch('4007249146')
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

country = eansearch.issuingCountryLookup("5099750442227")
print(ean + " was issued in " + country)

barcode = eansearch.barcodeImage("5099750442227", 300, 200)
print("Barcode image for " + ean + " (base64 encoded): " + barcode)

#import base64
#print (base64.b64decode(barcode))

