"""
A Python class for EAN and ISBN name lookup and validation using the API on ean-search.org.

To use it, you need an API access token from https://www.ean-search.org/ean-database-api.html

Python 2.x or 3.x
"""

import sys
import json

class EANSearch:

	def __init__(self, token):
		self._apiurl = "https://api.ean-search.org/api?token=" + token + "&format=json"


	def barcodeLookup(self, ean, lang=1):
		"""Lookup the product name for an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&ean=" + str(ean) + "&language=" + str(lang))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		else:
			return data[0]["name"]

	def barcodeSearch(self, ean, lang=1):
		"""Lookup the product info for an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&ean=" + str(ean) + "&language=" + str(lang))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		else:
			return data[0]

	def isbnLookup(self, isbn):
		"""Lookup the book title for an ISBN-10 or ISBN-13 barcode"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&isbn=" + str(isbn))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		else:
			return data[0]["name"]

	def verifyChecksum(self, ean):
		"""verify checksum of an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=verify-checksum&ean=" + str(ean))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		else:
			return data[0]["valid"]

	def productSearch(self, name, page=0, lang=99):
		"""search for a product name"""
		contents = self._urlopen(self._apiurl + "&op=product-search&name=" + name + "&page=" + str(page) + "&language=" + str(lang))
		data = json.loads(contents)
		return data["productlist"]

	def categorySearch(self, category, name='', page=0, lang=99):
		"""search for a product name"""
		contents = self._urlopen(self._apiurl + "&op=category-search&category=" + str(category) + "&name=" + name + "&page=" + str(page) + "&language=" + str(lang))
		data = json.loads(contents)
		return data["productlist"]

	def barcodePrefixSearch(self, prefix, page=0, lang=1):
		"""search for a prefix of EAN barcodes"""
		contents = self._urlopen(self._apiurl + "&op=barcode-prefix-search&prefix=" + str(prefix) + "&page=" + str(page) + "&language=" + str(lang))
		data = json.loads(contents)
		return data["productlist"]

	def _urlopen(self, url):
         if (sys.version_info >= (3,)):
             import urllib.request
             return urllib.request.urlopen(url, timeout=180).read().decode("utf-8")
         else:
             import urllib2
             return urllib2.urlopen(url, timeout=180).read().decode("utf-8")

	def issuingCountryLookup(self, ean):
		"""get issuing country of an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=issuing-country&ean=" + str(ean))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		else:
			return data[0]["issuingCountry"]

	def barcodeImage(self, ean):
		"""get barcodeimage for EAN"""
		contents = self._urlopen(self._apiurl + "&op=barcode-image&ean=" + str(ean))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		else:
			return data[0]["barcode"]

