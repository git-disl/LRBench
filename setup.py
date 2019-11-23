from setuptools import setup

import os
import sys

with open('README.md') as f:
  long_description = f.read()


setup(
  name = 'LRBench',
  packages = ['LRBench', 'LRBench.lr', 'LRBench.database', 'LRBench.framework', 'LRBench.monitor'],
  version = '0.0.0.1',      
  description = 'A learning rate recommending and benchmarking tool.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Yanzhao Wu',
  author_email = 'yanzhaowumail@gmail.com',
  url = 'https://github.com/git-disl/LRBench',
  download_url = 'https://github.com/git-disl/LRBench/archive/master.zip',
  keywords = ['LEARNING RATE', 'TRAINING', 'DEEP LEARNING'],
  install_requires=[
          'numpy',
          'matplotlib',
          'psycopg2'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
