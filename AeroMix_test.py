#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import AeroMix

#%% Loading sample input dictionary

input_dict = AeroMix.getAerosolType('urban', [0.4,0.5,0.6,0.7,0.8],80)

output = AeroMix.run(input_dict)

#%% Copying aerosol data to custom directory

data_dir = './'
AeroMix.CopyAerosolData(data_dir)
data_dir = data_dir+'aerosol_components_AeroMix'

# Creating new external aerosol in custom directory

ext_input = AeroMix.getSampleInputDict_ext()
ext_input['Output directory'] = data_dir
ext_input['Output filename'] = 'custom1'
ext_input['RH'] = 0

AeroMix.ext_aerosol(ext_input)

#%% Creating new core-shell aerosol in custom directory

cs_input = AeroMix.getSampleInputDict_cs()
cs_input['Component file directory'] = data_dir
cs_input['Output directory'] = data_dir
cs_input['Output filename'] = 'custom2'
cs_input['RH'] = 0

AeroMix.cs_aerosol(cs_input)
#%% Running AeroMix with new compoents

input_dict['Layer1 component concentration'][10] = 100
input_dict['Layer1 component concentration'][11] = 100000
input_dict['Layer1 relative humidity'] = 0
input_dict['Component file directory'] = data_dir

output = AeroMix.run(input_dict)
#%%
for filename in os.listdir(data_dir):
    os.remove(data_dir+'/'+filename)
os.rmdir(data_dir)

print('Test completed successfully')
