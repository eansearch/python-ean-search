# EANSearch

A Python class for EAN and ISBN name lookup and validation using the API on https://www.ean-search.org

Compatible with Python 2.x **and** 3.x

```python
from eansearch import EANSearch

# get a token from https://www.ean-search.org/ean-database-api.html
apiToken = "secret"
ean = "5099750442227" # Thriller

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

eanList = eansearch.categorySearch(45, 'thriller');
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.barcodePrefixSearch('4007249146');
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

country = eansearch.issuingCountryLookup("5099750442227")
print(ean + " was issued in " + country)

barcode = eansearch.barcodeImage("5099750442227")
print("Barcode image for " + ean + " (base64 encoded): " + barcode)

//import base64
//print (base64.b64decode(barcode))

