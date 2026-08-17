# EANSearch

A Python class for EAN and ISBN name lookup and validation using the API on https://www.ean-search.org

Compatible with Python 2.x **and** 3.x

You can install the eansearch module directly with pip:
```sh
python -m pip install eansearch
```

Then use EANSearch in your own scripts like this:

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
print(ean, " is ", product["name"].encode("utf-8"), " from category ", product["categoryName"], "(Google ID", product["googleCategoryId"], ") issued in", product["issuingCountry"])

# search for ISBN-10, use barcodeLookup() for ISBN-13
isbn = "1119578884"
title = eansearch.isbnLookup(isbn)
print(isbn, " is ", title)

ean = "5099750442227" # Thriller
ok = eansearch.verifyChecksum(ean)
print(ean, " is ", "OK" if ok else "Not OK")

# search for product name "iPod", get the first page of the results, only English results
eanList = eansearch.productSearch("iPod")
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

# search for similar product names, get the first page of the results, in any language
eanList = eansearch.similarProductSearch("iPod with extra features", 0, 99)
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.categorySearch(45, "thriller")
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

eanList = eansearch.barcodePrefixSearch("4007249146")
for product in eanList:
	print(product["ean"], " is ", product["name"].encode("utf-8"))

# lookup the EAN for an ASIN
asin = "B00000J1V5"
ean = eansearch.findEanForAsin(asin)
print("ASIN ", asin, " is EAN ", ean)

# lookup the ASIN for an EAN
ean = "0722868396643"
asin = eansearch.findAsinForEan(ean)
print("EAN ", ean, " is ASIN ", asin)

# lookup the LCCN for and ISBN-13 / EAN
isbn13 = "9780815346333"
lccn = eansearch.findLccnForEan(isbn13)
print("ISBN-13 ", isbn13, " is LCCN ", lccn)

# lookup the EAN / ISBN-13 for and LCCN
lccn = "2020691629"
ean = eansearch.findEanForLccn(lccn)
print("LCCN ", lccn, " is EAN ", ean)

country = eansearch.issuingCountryLookup("5099750442227")
print(ean + " was issued in " + country)

barcode = eansearch.barcodeImage("5099750442227", 300, 200)
print("HTML: <img src=\"data:image/png;base64," + " encoded + "\">")

