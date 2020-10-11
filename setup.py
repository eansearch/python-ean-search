import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='eansearch',
      description='A Python class for EAN and ISBN name lookup and validation using the API on ean-search.org',
      long_description=long_description,
      long_description_content_type="text/markdown",
      version='1.0.6',
      url='https://github.com/eansearch/python-ean-search',
      author='Jan Willamowius',
      author_email='info@relaxedcommunications.com',
      keywords = 'barcode barcodes ean ean13 ean-13 upc gtin isbn13 isbn-13 search lookup find valid validation',
      packages=setuptools.find_packages(),
      py_modules=['eansearch'],
      classifiers=[
          'License :: OSI Approved',
          'License :: OSI Approved :: MIT License',
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Other Audience',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Topic :: Office/Business :: Financial :: Point-Of-Sale',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      python_requires='>=2.0',
)

