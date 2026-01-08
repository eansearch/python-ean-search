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

isbn = "1119578884"
title = eansearch.isbnLookup(isbn)
print(isbn, " is ", title)

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

country = eansearch.issuingCountryLookup("5099750442227")
print(ean + " was issued in " + country)

barcode = eansearch.barcodeImage("5099750442227", 300, 200)
print("HTML: <img src=\"data:image/png;base64," + " encoded + "\">")

