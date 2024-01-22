
"""
AeroMix v 1.0.1 | Python package for modeling aerosol optical properties.

Copyright © 2023  Sam P Raj and P R Sinha
"""


def getAerosolType(name, wavelength_array, mixed_layer_rh, max_no_comps=9):
    """
    Load AeroMix input dictionary for predefined aerosol types.

    Parameters
    ----------
    name : A string representing the type of aerosol. Predefined types are
        ('default','urban','continental clean','continental average',
         'continental polluted','desert',''desert',maritime clean',
         'maritime polluted','maritime tropical','antarctic','arctic').
    wavelength_array : An array specifying the wavelengths (in µm) at which
        the optical properties are to be calculated. Acceptable values are
        [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
         0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.2, 3.39, 3.5, 3.75, 4.0,
         4.5, 5.0, 5.5, 6.0, 6.2, 6.5, 7.2, 7.9, 8.2, 8.5, 8.7, 9.0, 9.2, 9.5,
         9.8, 10.0, 10.6, 11.0, 11.5, 12.5, 13.0, 14.0, 14.8, 15.0, 16.4, 17.2,
         18.0, 18.5, 20.0, 21.3, 22.5, 25.0, 27.9, 30.0, 35.0, 40.0].
    mixed_layer_rh : An integer representing the relative humidity percentage
        in the mixed layer. Acceptable values are (0,50,70,80,90,95,98,99)
    max_no_comps : Maximum number of components to constitute the mixture.
        Should be 9 or greater. The default is 9

    Returns
    -------
    A dictionary containing input parameters for running AeroMix.

    """
    def_input_dir = {'Wavelengths': wavelength_array,
                     'Maximum radius': 5,
                     'Maximum number of components': max_no_comps,
                     'Component file directory': 'def',
                     'Input unit': 0,
                     'Layer1 profile type': 0,
                     'Layer1 relative humidity': mixed_layer_rh,
                     'Layer1 profile params': [0, 2, 8],
                     'Layer1 component concentration': {k: 0 for k in range(
                         1, max_no_comps+1)},
                     'Layer2 profile type': 1,
                     'Layer2 relative humidity': 50,
                     'Layer2 profile params': [2, 2],
                     'Layer2 component concentration': {k: 0 for k in range(
                         1, max_no_comps+1)},
                     'Layer3 profile type': 0,
                     'Layer3 relative humidity': 50,
                     'Layer3 profile params': [2, 12, 8],
                     'Layer3 component concentration': {k: 0 for k in range(
                         1, max_no_comps+1)},
                     'Layer4 profile type': 1,
                     'Layer4 relative humidity': 0,
                     'Layer4 profile params': [12, 35, 1],
                     'Layer4 component concentration': {k: 0 for k in range(
                         1, max_no_comps+1)},
                     'Layer5 profile type': 0,
                     'Layer5 relative humidity': 0,
                     'Layer5 profile params': [35, 35, 8],
                     'Layer5 component concentration': {k: 0 for k in range(
                         1, max_no_comps+1)},
                     'Layer6 profile type': 0,
                     'Layer6 relative humidity': 0,
                     'Layer6 profile params': [35, 35, 8],
                     'Layer6 component concentration': {k: 0 for k in range(
                         1, max_no_comps+1)},
                     }
    def_input_dir['Layer2 component concentration'][7] = 1.8633
    def_input_dir['Layer3 component concentration'][1] = 0.0013
    def_input_dir['Layer3 component concentration'][2] = 438.0
    def_input_dir['Layer3 component concentration'][3] = 294.0
    def_input_dir['Layer3 component concentration'][6] = 2
    def_input_dir['Layer4 component concentration'][9] = 3

    if name == 'default':
        def_input_dir = def_input_dir
    elif name == 'antarctic':
        def_input_dir['Layer1 component concentration'][4] = 0.047
        def_input_dir['Layer1 component concentration'][7] = 3.993e-02
        def_input_dir['Layer1 component concentration'][9] = 42.9
        def_input_dir['Layer1 profile params'] = [0, 10, 8]
        def_input_dir['Layer2 profile params'] = [10, 10, 11]
        def_input_dir['Layer3 profile params'] = [10, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'arctic':
        def_input_dir['Layer1 component concentration'][1] = 0.01
        def_input_dir['Layer1 component concentration'][2] = 1300
        def_input_dir['Layer1 component concentration'][3] = 5300
        def_input_dir['Layer1 component concentration'][4] = 1.9
        def_input_dir['Layer1 profile type'] = 1
        def_input_dir['Layer1 profile params'] = [0, 2, 1]
        def_input_dir['Layer2 profile params'] = [2, 2, 11]
        def_input_dir['Layer3 profile params'] = [2, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'continental average':
        def_input_dir['Layer1 component concentration'][1] = 0.4
        def_input_dir['Layer1 component concentration'][2] = 7000
        def_input_dir['Layer1 component concentration'][3] = 8300
        def_input_dir['Layer1 profile params'] = [0, 2, 8]
        def_input_dir['Layer2 profile params'] = [2, 2, 11]
        def_input_dir['Layer3 profile params'] = [2, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'continental clean':
        def_input_dir['Layer1 component concentration'][1] = 0.15
        def_input_dir['Layer1 component concentration'][2] = 2600
        def_input_dir['Layer1 profile params'] = [0, 2, 8]
        def_input_dir['Layer2 profile params'] = [2, 2, 11]
        def_input_dir['Layer3 profile params'] = [2, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'continental polluted':
        def_input_dir['Layer1 component concentration'][1] = 0.6
        def_input_dir['Layer1 component concentration'][2] = 15700
        def_input_dir['Layer1 component concentration'][3] = 34300
        def_input_dir['Layer1 profile params'] = [0, 2, 8]
        def_input_dir['Layer2 profile params'] = [2, 2, 11]
        def_input_dir['Layer3 profile params'] = [2, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'desert':
        def_input_dir['Layer1 component concentration'][2] = 2000
        def_input_dir['Layer1 component concentration'][6] = 269.5
        def_input_dir['Layer1 component concentration'][7] = 30.5
        def_input_dir['Layer1 component concentration'][8] = 0.142
        def_input_dir['Layer1 profile params'] = [0, 6, 8]
        def_input_dir['Layer2 profile params'] = [6, 6, 11]
        def_input_dir['Layer3 profile params'] = [6, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'maritime clean':
        def_input_dir['Layer1 component concentration'][2] = 1500
        def_input_dir['Layer1 component concentration'][4] = 20
        def_input_dir['Layer1 component concentration'][5] = 3.2e-3
        def_input_dir['Layer1 profile params'] = [0, 2, 1]
        def_input_dir['Layer2 profile params'] = [2, 2, 11]
        def_input_dir['Layer3 profile params'] = [2, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'maritime polluted':
        def_input_dir['Layer1 component concentration'][2] = 3800
        def_input_dir['Layer1 component concentration'][3] = 5180
        def_input_dir['Layer1 component concentration'][4] = 20
        def_input_dir['Layer1 component concentration'][5] = 3.2e-3
        def_input_dir['Layer1 profile params'] = [0, 2, 1]
        def_input_dir['Layer2 profile params'] = [2, 2, 11]
        def_input_dir['Layer3 profile params'] = [2, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'maritime tropical':
        def_input_dir['Layer1 component concentration'][2] = 590
        def_input_dir['Layer1 component concentration'][4] = 10
        def_input_dir['Layer1 component concentration'][5] = 1.3e-3
        def_input_dir['Layer1 profile params'] = [0, 2, 1]
        def_input_dir['Layer2 profile params'] = [2, 2, 11]
        def_input_dir['Layer3 profile params'] = [2, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    elif name == 'urban':
        def_input_dir['Layer1 component concentration'][1] = 1.5
        def_input_dir['Layer1 component concentration'][2] = 28000
        def_input_dir['Layer1 component concentration'][3] = 130000
        def_input_dir['Layer1 profile params'] = [0, 2, 8]
        def_input_dir['Layer2 profile params'] = [2, 2, 11]
        def_input_dir['Layer3 profile params'] = [2, 12, 8]
        def_input_dir['Layer4 profile params'] = [12, 35, 1]
    return def_input_dir
