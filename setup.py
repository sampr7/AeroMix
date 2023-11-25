#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from setuptools import setup

setup(
      name='AeroMix',
      version='0.0.1',
      description='Python package for modeling aerosol optical properties',
      url='https://github.com/sampr7/AeroMix',
      author='Sam P Raj',
      author_email='sampr7@gmail.com',
      licence='GPL-3.0',
      py_modules=['run','getAerosolType','CopyAerosolData','ext_aerosol','cs_aerosol','getSampleInputDict_ext','getSampleInputDict_cs'],
      package_dir={'': 'aeromix'},
      classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
    'License :: OSI Approved :: GPL-3.0',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',],
    keywords=['aerosol model mixing state AOD SSA g'],
    install_requires=['numpy >=1.13','scipy >=1.5','PyMieScatt >=1.8.0'])