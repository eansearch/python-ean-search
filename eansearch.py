"""
A Python class for EAN and ISBN name lookup and validation using the API on ean-search.org.

To use it, you need an API access token from https://www.ean-search.org/ean-database-api.html

Python 2.x or 3.x
"""

import sys
import time
import json
import socket
import threading

class EANSearch:

	def __init__(self, token):
		self._apiurl = "https://api.ean-search.org/api?token=" + token + "&format=json"
		self._timeout = 30
		self._ua = "python-eansearch/1.0"
		self._state = threading.local()
		self.MAX_API_TRIES = 3

	@property
	def _error(self):
		return getattr(self._state, "error", "")

	@_error.setter
	def _error(self, value):
		self._state.error = value

	@property
	def _remaining(self):
		return getattr(self._state, "remaining", -1)

	@_remaining.setter
	def _remaining(self, value):
		self._state.remaining = value

	def setTimeout(self, sec):
		"""Set HTTP timeout in seconds"""
		self._timeout = sec

	def error(self):
		"""Check if last API call produced an error"""
		return self._error

	def barcodeLookup(self, ean, lang=1):
		"""Lookup the product name for an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&ean=" + str(ean) + "&language=" + str(lang))
		product = self._first(contents)
		return None if product is None else product["name"]

	def barcodeSearch(self, ean, lang=1):
		"""Lookup the product info for an EAN barcode (or ISBN-13)"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&ean=" + str(ean) + "&language=" + str(lang))
		return self._first(contents)

	def isbnLookup(self, isbn):
		"""Lookup the book title for an ISBN-10 barcode (use barcodeLookup() for ISBN-13)"""
		contents = self._urlopen(self._apiurl + "&op=barcode-lookup&isbn=" + str(isbn))
		product = self._first(contents)
		return None if product is None else product["name"]

	def findEanForAsin(self, asin):
		"""Lookup the EAN barcode for an ASIN (Amazon Standard Identification Number)"""
		contents = self._urlopen(self._apiurl + "&op=ean-for-asin-lookup&asin=" + str(asin))
		product = self._first(contents)
		return None if product is None else product["ean"]

	def findAsinForEan(self, ean):
		"""Lookup the ASIN (Amazon Standard Identification Number) for an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=asin-for-ean-lookup&ean=" + str(ean))
		product = self._first(contents)
		return None if product is None else product["asin"]

	def findEanForLccn(self, lccn):
		"""Lookup the EAN barcode for an LCCN (Library of Congress Control Number), there coulbe be multiple EANs for one LCCN, we just return the first one"""
		contents = self._urlopen(self._apiurl + "&op=ean-for-lccn-lookup&lccn=" + str(lccn))
		product = self._first(contents)
		return None if product is None else product["ean"]

	def findLccnForEan(self, ean):
		"""Lookup the LCCN (Library of Congress Control Number) for an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=lccn-for-ean-lookup&ean=" + str(ean))
		product = self._first(contents)
		return None if product is None else product["lccn"]

	def verifyChecksum(self, ean):
		"""verify checksum of an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=verify-checksum&ean=" + str(ean))
		product = self._first(contents)
		if product is None:
			return None
		return str(product["valid"]).lower() in ("1", "true")

	def productSearch(self, name, page=0, lang=1):
		"""search for a product name (exact search)"""
		name = self._quote(name)
		contents = self._urlopen(self._apiurl + "&op=product-search&name=" + name + "&page=" + str(page) + "&language=" + str(lang))
		return self._productlist(contents)

	def similarProductSearch(self, name, page=0, lang=1):
		"""search for a product name (find similar names)"""
		name = self._quote(name)
		contents = self._urlopen(self._apiurl + "&op=similar-product-search&name=" + name + "&page=" + str(page) + "&language=" + str(lang))
		return self._productlist(contents)

	def categorySearch(self, category, name, page=0, lang=1):
		"""search for a product name (exact match)"""
		name = self._quote(name)
		contents = self._urlopen(self._apiurl + "&op=category-search&category=" + str(category) + "&name=" + name + "&page=" + str(page) + "&language=" + str(lang))
		return self._productlist(contents)

	def barcodePrefixSearch(self, prefix, page=0, lang=1):
		"""search for a prefix of EAN barcodes"""
		contents = self._urlopen(self._apiurl + "&op=barcode-prefix-search&prefix=" + str(prefix) + "&page=" + str(page) + "&language=" + str(lang))
		return self._productlist(contents)

	def issuingCountryLookup(self, ean):
		"""get issuing country of an EAN barcode"""
		contents = self._urlopen(self._apiurl + "&op=issuing-country&ean=" + str(ean))
		product = self._first(contents)
		return None if product is None else product["issuingCountry"]

	def barcodeImage(self, ean, width=102, height=50):
		"""get barcodeimage for EAN"""
		contents = self._urlopen(self._apiurl + "&op=barcode-image&ean=" + str(ean) + "&width=" + str(width) + "&height=" + str(height))
		product = self._first(contents)
		return None if product is None else product["barcode"]

	def creditsRemaining(self):
		"""get number of requests remaining this month"""
		if (self._remaining < 0):
			self._urlopen(self._apiurl + "&op=account-status")
		return self._remaining

	def _first(self, contents):
		"""return the first result object, or None on error / empty / unexpected response"""
		data = json.loads(contents)
		if not isinstance(data, list) or not data or not isinstance(data[0], dict) or "error" in data[0]:
			return None
		return data[0]

	def _productlist(self, contents):
		"""return the product list, or [] on error / unexpected response"""
		data = json.loads(contents)
		if not isinstance(data, dict):
			return []
		return data.get("productlist") or []

	def _setRemaining(self, value):
		if value is None:
			return
		try:
			self._remaining = int(value)
		except ValueError:
			pass

	def _errorResult(self, msg):
		self._error = msg
		return json.dumps([{"error": msg}])

	def _quote(self, param):
		if (sys.version_info >= (3,)):
			import urllib.parse
			return urllib.parse.quote_plus(param)
		import urllib
		if isinstance(param, unicode):
			param = param.encode("utf-8")
		return urllib.quote_plus(param)

	def _urlopen(self, url, tries = 1):
		self._error = ""	# clear last error
		if (sys.version_info >= (3,)):
			from urllib.request import urlopen, Request
			from urllib.error import HTTPError, URLError
			request = Request(url, headers={'User-Agent': self._ua})
		else:
			from urllib2 import urlopen, Request, HTTPError, URLError
			request = Request(url, headers={'User-Agent': self._ua})
		try:
			connection = urlopen(request, timeout=self._timeout)
			try:
				if (sys.version_info >= (3,)):
					self._setRemaining(connection.getheader('X-Credits-Remaining'))
				else:
					self._setRemaining(connection.info().getheader('X-Credits-Remaining'))
				return connection.read().decode("utf-8")
			finally:
				connection.close()
		except HTTPError as e:
			if e.code == 429 and tries < self.MAX_API_TRIES:
				time.sleep(1)
				return self._urlopen(url, tries+1)
			return self._errorResult("Server error " + str(e.code))
		except URLError as e:
			return self._errorResult("Connection error " + str(e.reason))
		except socket.timeout:
			return self._errorResult("Timeout")
