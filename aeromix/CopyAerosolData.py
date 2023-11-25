#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeroMix v 0.0.1 | Python package for modeling aerosol optical properties
Copyright © 2023  Sam P Raj
"""

import os
import sys
import shutil

def CopyAerosolData(dir_loc):
    def_comp_dir = (os.path.join(os.path.dirname(__file__), 'aerosol_components'))
    shutil.copytree(def_comp_dir,dir_loc+'aerosol_components_AeroMix',symlinks=False,ignore=None,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)
    
