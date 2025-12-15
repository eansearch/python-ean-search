"""
A Python class for EAN and ISBN name lookup and validation using the API on ean-search.org.

To use it, you need an API access token from https://www.ean-search.org/ean-database-api.html

Python 2.x or 3.x
"""

import sys
import time
import json

class EANSearch:

	def __init__(self, token):
		self._apiurl = "https://api.ean-search.org/api?token=" + token + "&format=json"
		self._timeout = 180
		self.MAX_API_TRIES = 3

	def setTimeout(self, sec):
		"""Set HTTP timeout in seconds"""
		self._timeout = sec

	def barcodeLookup(self, ean, lang=1):
		"""Lookup the product name for an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&ean=" + str(ean) + "&language=" + str(lang))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		return data[0]["name"]

	def barcodeSearch(self, ean, lang=1):
		"""Lookup the product info for an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&ean=" + str(ean) + "&language=" + str(lang))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		return data[0]

	def isbnLookup(self, isbn):
		"""Lookup the book title for an ISBN-10 or ISBN-13 barcode"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&isbn=" + str(isbn))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		return data[0]["name"]

	def verifyChecksum(self, ean):
		"""verify checksum of an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=verify-checksum&ean=" + str(ean))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		return data[0]["valid"]

	def productSearch(self, name, page=0, lang=1):
		"""search for a product name (exact search)"""
		name = self._quote(name)
		contents = self._urlopen(self._apiurl + "&op=product-search&name=" + name + "&page=" + str(page) + "&language=" + str(lang))
		data = json.loads(contents)
		return data["productlist"]

	def similarProductSearch(self, name, page=0, lang=1):
		"""search for a product name (find similar names)"""
		name = self._quote(name)
		contents = self._urlopen(self._apiurl + "&op=similar-product-search&name=" + name + "&page=" + str(page) + "&language=" + str(lang))
		data = json.loads(contents)
		return data["productlist"]

	def categorySearch(self, category, name, page=0, lang=1):
		"""search for a product name (exact match)"""
		name = self._quote(name)
		contents = self._urlopen(self._apiurl + "&op=category-search&category=" + str(category) + "&name=" + name + "&page=" + str(page) + "&language=" + str(lang))
		data = json.loads(contents)
		return data["productlist"]

	def barcodePrefixSearch(self, prefix, page=0, lang=1):
		"""search for a prefix of EAN barcodes"""
		contents = self._urlopen(self._apiurl + "&op=barcode-prefix-search&prefix=" + str(prefix) + "&page=" + str(page) + "&language=" + str(lang))
		data = json.loads(contents)
		return data["productlist"]

	def issuingCountryLookup(self, ean):
		"""get issuing country of an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=issuing-country&ean=" + str(ean))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		return data[0]["issuingCountry"]

	def barcodeImage(self, ean, width=102, height=50):
		"""get barcodeimage for EAN"""
		contents = self._urlopen(self._apiurl + "&op=barcode-image&ean=" + str(ean) + "&width=" + str(width) + "&height=" + str(height))
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		return data[0]["barcode"]

	def _quote(self, param):
		if (sys.version_info >= (3,)):
			import urllib.parse
			return urllib.parse.quote_plus(param)
		import urllib2
		return urllib2.quote(param)

	def _urlopen(self, url, tries = 1):
		if (sys.version_info >= (3,)):
			import urllib.request
			import urllib.error
			try:
				connection = urllib.request.urlopen(url, timeout=self._timeout)
			except urllib.error.HTTPError as e:
				if e.code == 429 and tries < self.MAX_API_TRIES:
					time.sleep(1)
				return self._urlopen(url, tries+1)
		else:
			import urllib2
			try:
				connection = urllib2.urlopen(url, timeout=self._timeout)
			except urllib2.HTTPError as e:
				if e.code == 429 and tries < self.MAX_API_TRIES:
					time.sleep(1)
				return self._urlopen(url, tries+1)

		return connection.read().decode("utf-8")

