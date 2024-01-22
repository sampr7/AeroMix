
"""
AeroMix v 1.0.1 | Python package for modeling aerosol optical properties.

Copyright © 2023  Sam P Raj and P R Sinha
"""

import os
import shutil


def CopyAerosolData(dir_loc):
    """
    Copy default database to desired location.

    Parameters
    ----------
    dir_loc : The target location where the database will be copied.

    Returns
    -------
    Database directory copied to target location.

    """
    def_comp_dir = (os.path.join(
        os.path.dirname(__file__), 'aerosol_components'))
    shutil.copytree(def_comp_dir, dir_loc+'aerosol_components_AeroMix',
                    symlinks=False, ignore=None,
                    ignore_dangling_symlinks=False, dirs_exist_ok=True)
