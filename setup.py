import setuptools


long_description = open('README.md').read()
setuptools.setup(name='pubmed_extract',
      version='0.4',
      description='Python Distribution Utilities',
      long_description = 'README.md',
      author='Ashutosh Kumar',
      author_email='akashutosh09@gmail.com',
      url='https://skumarashutosh.github.io/',
      packages=['pubmed_extract'],
      install_requires=[]
     )

# import json
# import dotenv
# import os
# import sys
# import requests
# import xml
# import pandas as pd
# from tqdm import tqdm
# from tabulate import tabulate
# from bs4 import BeautifulSoup as bs
# #from pmids_extract_solr import pmids_solr_list
# from dotenv import load_dotenv