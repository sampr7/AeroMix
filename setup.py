#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
      name='AeroMix',
      version='1.0.0',
      description='Python package for modeling aerosol optical properties',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/sampr7/AeroMix',
      author='Sam P Raj',
      author_email='sampr7@gmail.com',
      licence='GNU General Public License v3 (GPLv3)',
      packages=['AeroMix'],
      package_dir={'AeroMix': 'AeroMix'},
      classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',],
    keywords=['aerosol model mixing state AOD SSA g'],
    install_requires=['numpy','scipy','PyMieScatt'],
    package_data={'AeroMix':['aerosol_components/*']},
    zip_safe=False)
