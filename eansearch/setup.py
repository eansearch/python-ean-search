import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='eansearch',
      description='A Python class for EAN and ISBN name lookup and validation using the API on ean-search.org',
      long_description=long_description,
      version='1.0.1',
      url='https://github.com/eansearch/python-ean-search',
      author='Jan Willamowius',
      author_email='info@relaxedcommunications.com',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      ],
      package_dir={'': 'eansearch'},
      packages=['eansearch'],
)

