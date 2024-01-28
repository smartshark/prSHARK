#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

if not sys.version_info[0] == 3:
    print('only python3 supported!')
    sys.exit(1)

setup(
    name='prSHARK',
    version='1.0.2',
    author='Alexander Trautsch',
    author_email='alexander.trautsch@cs.uni-goettingen.de',
    description='Collect data from pull request systems',
    install_requires=['mongoengine', 'pymongo', 'requests>=2.10.0', 'oauthlib>=3.0.0',
                      'cryptography>=1.3.4', 'python-dateutil', 'validate_email',
                      'pycoshark>=1.4.1', 'mock', 'deepdiff', 'pytz'],
    url='https://github.com/smartshark/prSHARK',
    download_url='https://github.com/smartshark/prSHARK/zipball/master',
    packages=find_packages(),
    test_suite='tests',
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache2.0 License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
