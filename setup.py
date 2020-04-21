#!/usr/bin/env python
__usage__ = "setup.py command [--options]"
__description__ = "standard install script"
__author__ = "pgjlandry@gmail.com"

#-------------------------------------------------

from setuptools import (setup, find_packages)
import glob

setup(
    name = 'eos-inf',
    version = '0.0',
    url = 'https://github.com/landryp/eos-inf',
    author = __author__,
    author_email = 'philippe.landry@ligo.org',
    description = __description__,
    license = '',
    scripts = glob.glob('bin/*'),
    packages = find_packages(),
    data_files = [],
    requires = [],
)
