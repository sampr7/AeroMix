#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 02:21:00 2023

@author: sam
"""

import aeromix

input_dict = aeromix.getAerosolType('desert', [0.3,0.5], 80)


output = aeromix.run(input_dict)

# print(output)

# input_dict = {'Name':'SSamBC_4',
#               'Output directory':'def',
#               'Output filename':'custom11',
#               'RH':50,
#               'Component file directory':'def',
#               'Core':'SSam',
#               'Shell':'BC',
#               'Method':'mass',
#               'CSR':0.9,
#               'Mass of core':5,
#               'Mass of shell':2
#               }
              
# input_dict = AeroMix.getSampleInputDict_cs()
# AeroMix.cs_aerosol(input_dict)
