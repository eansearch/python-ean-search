"""
A Python class for EAN and ISBN name lookup and validation using the API on ean-search.org.

To use it, you need an API access token from https://www.ean-search.org/ean-database-api.html

Python 2.x or 3.x
"""

import sys
import json

class EANSearch:

	def __init__(self, token):
		self.token = token;

	def barcodeLookup(self, ean, lang=1):
		"""Lookup the product name for an EAN barcode"""
		contents = self._urlopen("https://api.ean-search.org/api?token=" + self.token \
			+ "&op=barcode-lookup&format=json&ean=" + ean + "&lang=" + str(lang)).read().decode("utf-8")
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		else:
			return data[0]["name"]

	def verifyChecksum(self, ean):
		"""verify checksum of an EAN barcode"""
		contents = self._urlopen("https://api.ean-search.org/api?token=" + self.token \
			+ "&op=verify-checksum&format=json&ean=" + ean).read().decode("utf-8")
		data = json.loads(contents)
		if "error" in data[0]:
			return None
		else:
			return data[0]["valid"]

	def productSearch(self, name, page=0):
		"""search for a product name"""
		contents = self._urlopen("https://api.ean-search.org/api?token=" + self.token \
			+ "&op=product-search&format=json&name=" + name + "&page=" + str(page)).read().decode("utf-8")
		data = json.loads(contents)
		return data["productlist"]

	def barcodePrefixSearch(self, prefix, page=0):
		"""search for a prefix of EAN barcodes"""
		contents = self._urlopen("https://api.ean-search.org/api?token=" + self.token \
			+ "&op=barcode-prefix-search&format=json&prefix=" + prefix + "&page=" + str(page)).read().decode("utf-8")
		data = json.loads(contents)
		return data["productlist"]

	def _urlopen(self, url):
         if (sys.version_info > (3, 0)):
             import urllib.request
             return urllib.request.urlopen(url)
         else:
             import urllib2
             return urllib2.urlopen(url)

