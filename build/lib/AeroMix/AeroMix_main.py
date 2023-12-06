#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeroMix v 1.0.0 | Python package for modeling aerosol optical properties
Copyright © 2023  Sam P Raj

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import copy
import math
import sys
from math import exp as exp
import numpy as np
from numpy import log as ln
from numpy import log10 as log
from scipy.integrate import trapezoid as trap


comp_names = {1:'IS',2:'WS',
              3:'BC',4:'SSam',
              5:'SScm',6:'MDnm',
              7:'MDam',8:'MDcm',
              9:'SUSO',10:'custom'}
#Create radius array
xrmin = 0.01
xrmax = 10
deltar = 0.015
xr = np.zeros(220)
xr[0] = xrmin
ix = 1
xranf = log(xrmin)
while xr[ix-1] < xrmax:
    xrl = xranf+deltar*(ix-1)
    xr[ix] = 10**(xrl)
    ix = ix+1
"""
Function to a create lookup dictionary for aerosol component data
"""    
def _ReadOpticalData(var,RH):
    OptdataFiles = dict(zip(np.arange(1,var['Maximum number of components']+1),np.zeros(var['Maximum number of components'])))
    RH = str(RH) if RH>0 else '00'
    def_comp_dir = (os.path.join(os.path.dirname(__file__), 'aerosol_components'))
        
    comp_dir = def_comp_dir if var['Component file directory']=='def' else var['Component file directory']
    if comp_dir[-1] != '/' and sys.platform != 'Windows':
        comp_dir = comp_dir+'/'
    elif comp_dir[-1] != '\\' and sys.platform == 'Windows':
        comp_dir = comp_dir+'\\'    
    if not os.path.exists(comp_dir):
        print("Error: Component file directory "+comp_dir+" not found\nExiting program")
        raise SystemExit
    for i in OptdataFiles.keys():
        if i<10 and i not in [1,3,6,7,8]:
            filename = comp_dir+comp_names[i]+RH
        elif i<10 and i in [1,3,6,7,8]:
            filename = comp_dir+comp_names[i]+'00'            
        elif i>=10:
            filename = comp_dir+comp_names[10]+str(i-9)+'_'+RH
        OptdataFiles[i]=filename
    return OptdataFiles

"""
Function to read size and mass of aerosols from optdata file
"""    
def _ReadSizeMassData(file,comp_no):
    global min_rad,max_rad,sigma,rho,Rmod,var_name
    for line in file:
        if "minimum radius" in line:
            var_name,min_rad = line.split(':')
        if "maximum radius" in line:
            var_name,max_rad = line.split(':')
        if "sigma" in line:
            var_name,sigma = line.split(':')
        if "rho[g/cm**3]" in line:
            var_name,rho = line.split(':')
        if "Rmod" and "wet" in line:
            var_name,Rmod = line.split(':')
        if "Rmod [um]:" in line:
            var_name,Rmod = line.split(':')
    result = {'Rmin':float(min_rad),'Rmax':float(max_rad),
              'sigma':float(sigma),'rho':float(rho),'Rmod':float(Rmod)}
    return result

def _vlogn(sig,ro,n,r):
    a = (n/(math.sqrt(2*math.pi)*log(sig)))
    b = log(ro)
    c = -2*(log(sig))**2
    rlogn = a*exp((log(r)-b)**2/c)
    vlogn = (4/3)*math.pi*(r**3)*rlogn
    return vlogn

def _CalculateMass(var,RH):
    mass_data = {}
    for i in range(1,var['Maximum number of components']+1):
        OptdataFiles = _ReadOpticalData(var,RH)
        if os.path.exists(OptdataFiles[i]):
            OptDataFile = open(OptdataFiles[i],'r')
            mass_data[i] = _ReadSizeMassData(OptDataFile, i)
    masscalc = dict(zip(np.arange(1,var['Maximum number of components']+1),np.zeros(var['Maximum number of components'])))
    volcalc = dict(zip(np.arange(1,var['Maximum number of components']+1),np.zeros(var['Maximum number of components'])))
    for i in list(mass_data.keys()):
        rmin = mass_data[i]['Rmin']
        rmax = mass_data[i]['Rmax']
        sigma = mass_data[i]['sigma']
        rho = mass_data[i]['rho']
        rm = mass_data[i]['Rmod']
        n = 1
        
        rad_array = xr[1:np.argmax(xr)+1]
        if rmax>rad_array[-1] or rmax not in rad_array:
            rad_array = np.append(rad_array,rmax)
        if rmin<rad_array[0] or rmin not in rad_array:
            rad_array = np.append(rad_array,rmin)
        if var['Maximum radius'] not in rad_array:
            rad_array = np.append(rad_array,var['Maximum radius'])
        rad_array = np.sort(rad_array)
        
        if i == 6:
            dv = [_vlogn(sigma,rm,n,r)*10**6 for r in rad_array]
            vol_array = np.zeros(len(rad_array))
            for idx in range(len(rad_array)):
                if rad_array[idx] <= var['Maximum radius']:
                    vol_array[idx] = dv[idx]/(rad_array[idx]*ln(10))
                else:
                    vol_array[idx] = 0
            volcalc[i] = trap(vol_array,rad_array)*0.9754
            masscalc[i] = volcalc[i]*rho*10**-6
        elif i ==7 or i == 8:
            dv = [_vlogn(sigma,rm,n,r)*10**6 for r in rad_array]
            vol_array = np.zeros(len(rad_array))
            for idx in range(len(rad_array)):
                if rad_array[idx] <= var['Maximum radius']:
                    vol_array[idx] = dv[idx]/(rad_array[idx]*ln(10))
                else:
                    vol_array[idx] = 0
            volcalc[i] = trap(vol_array,rad_array)*0.9273
            masscalc[i] = volcalc[i]*rho*10**-6
        else:
            dv = [_vlogn(sigma,rm,n,r)*10**6 for r in rad_array]
            vol_array = np.zeros(len(rad_array))
            for idx in range(len(rad_array)):
                if rad_array[idx] <= var['Maximum radius']:
                    vol_array[idx] = dv[idx]/(rad_array[idx]*ln(10))
                else:
                    vol_array[idx] = 0
            volcalc[i] = trap(vol_array,rad_array)
            masscalc[i] = volcalc[i]*rho*10**-6
    return volcalc,masscalc,mass_data
"""
Function to convert mass concentration to number concentration if Input unit = 1
"""
def _numdenscalc(var,conc_dict,mean_mass):
    NumDens = dict(zip(np.arange(1,var['Maximum number of components']+1),np.zeros(var['Maximum number of components'])))
    if var['Input unit'] == 1:
        input_mass = conc_dict
        for i in list(mean_mass.keys()):
            if mean_mass[i] != 0:    
                NumDens[i] = input_mass[i]/mean_mass[i]
            else:
                NumDens[i] = 0
    elif var['Input unit'] == 0:
        NumDens = conc_dict
    return NumDens
"""
Function to retrive spectral optical data of aerosol components
"""
def _storeoptdata(var,NumDens,RH):
    OptdataFiles = _ReadOpticalData(var,RH)
    optdata = {}
    empty_optdata = {}
    for i in [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.2, 3.39, 3.5, 3.75, 4.0, 4.5, 5.0, 5.5, 6.0, 6.2, 6.5, 7.2, 7.9, 8.2, 8.5, 8.7, 9.0, 9.2, 9.5, 9.8, 10.0, 10.6, 11.0, 11.5, 12.5, 13.0, 14.0, 14.8, 15.0, 16.4, 17.2, 18.0, 18.5, 20.0, 21.3, 22.5, 25.0, 27.9, 30.0, 35.0, 40.0]:
        empty_optdata[i] = np.zeros(8)
    for i in NumDens.keys():
        optdata[i] = {}
        if NumDens[i] != 0:
            OptdataFileLoc = OptdataFiles[i]
            OptDataFile = open(OptdataFileLoc,'r')
            for line in OptDataFile:
                if "," in line:
                    wavelength,extc,scac,absc,ssa,g,extn,real,img = line.split(",")
                    optdata[i][float(wavelength)] = [float(extc),float(scac),
                                                       float(absc),float(ssa),
                                                       float(g),float(extn),
                                                       float(real),float(img)]
        else:
            optdata[i] = empty_optdata
    return optdata

"""
Function to calculate mie params
"""
def _mieparamcalc(optdata,NumDens,wavelength_i,param_index_no):
    if sum(NumDens.values()) != 0:
        result = 0
        for i in NumDens.keys():
            result = result+(NumDens[i]*optdata[i][wavelength_i][param_index_no])
    else:
        result = np.nan
    return result
"""
Function to calculate SSA and g
"""
def _ssaandgcalc(optdata,NumDens,wavelength_i,ext_i,sca_i,ssa_i,g_i):
    if sum(NumDens.values()) != 0:
        #ssa
        ssa_num = 0
        ssa_denom = 0
        for i in NumDens.keys():
            ssa_num = ssa_num+(NumDens[i]*optdata[i][wavelength_i][ext_i]*optdata[i][wavelength_i][ssa_i])
            ssa_denom = ssa_denom+(NumDens[i]*optdata[i][wavelength_i][ext_i])
        ssa = ssa_num/ssa_denom
        #g
        g_num = 0
        g_denom = 0
        for i in NumDens.keys():
            g_num = g_num+(NumDens[i]*optdata[i][wavelength_i][sca_i]*optdata[i][wavelength_i][g_i])
            g_denom = g_denom+(NumDens[i]*optdata[i][wavelength_i][sca_i])
        g = g_num/g_denom
    else:
        ssa = np.nan
        g = np.nan
    return ssa,g
"""
Function to calculate AOD
"""
def _AODcalc(extcalc,profile_type,profile_params,wavelength_i):
    #exponential profile
    if profile_type == 0:
        AOD = (extcalc[wavelength_i]*profile_params[2]*(
                        math.exp(-profile_params[0]/profile_params[2])-
                        math.exp(-profile_params[1]/profile_params[2])))
    #Homogenous layer
    elif profile_type == 1:
        AOD = (extcalc[wavelength_i]*(profile_params[1]-profile_params[0])*profile_params[2])
    #Cubic function profile
    elif profile_type == 2:
        AOD = extcalc[wavelength_i]*(((profile_params[2]/4)*(
            (profile_params[1]**4)-(profile_params[0]**4)))+((profile_params[3]/3)*(
                (profile_params[1]**3)-(profile_params[0]**3)))+((profile_params[4]/2)*(
                    (profile_params[1]**2)-(profile_params[0]**2)))+((profile_params[5])*(
                        (profile_params[1])-(profile_params[0]))))
    return AOD                     

def _layerparams(var,RH,Concentration,Max_components,wavelengths,profile_type,profile_params):
    mean_vol,mean_mass,mass_data = _CalculateMass(var,RH)
    NumDens = _numdenscalc(var,Concentration,mean_mass)
    TotalNumDens = sum(NumDens.values())
    mass_calc = dict(zip(np.arange(1,var['Maximum number of components']+1),np.zeros(var['Maximum number of components'])))
    vol_calc = dict(zip(np.arange(1,var['Maximum number of components']+1),np.zeros(var['Maximum number of components'])))
    no_mix_ratio = {}
    mass_mix_ratio = {}
    vol_mix_ratio = {}
    for i in range(1,var['Maximum number of components']+1):
        mass_calc[i] = mean_mass[i]*NumDens[i]
        vol_calc[i] = mean_vol[i]*NumDens[i]
    if TotalNumDens != 0:
        for i in list(mass_calc.keys()):
            no_mix_ratio[i] = NumDens[i]/sum(NumDens.values())
            mass_mix_ratio[i] = mass_calc[i]/sum(mass_calc.values())
            vol_mix_ratio[i] = vol_calc[i]/sum(vol_calc.values())
    else:
        for i in list(mass_calc.keys()):
            no_mix_ratio[i] = 0
            mass_mix_ratio[i] = 0
            vol_mix_ratio[i] = 0
    optdata = _storeoptdata(var,NumDens,RH)
    extcalc = {}                # Calculation of ext. coeff.
    for i in wavelengths:
        extcalc[i] = _mieparamcalc(optdata,NumDens,i,0)
    scacalc = {}                # Calculation of sca. coeff.
    for i in wavelengths:
        scacalc[i] = _mieparamcalc(optdata,NumDens,i,1)
    abscalc = {}                # Calculation of abs. coeff.
    for i in wavelengths:
        abscalc[i] = _mieparamcalc(optdata,NumDens,i,2)
    ssacalc = {}
    gcalc = {}
    for i in wavelengths:
        ssacalc[i],gcalc[i] = _ssaandgcalc(optdata, NumDens, i, 0, 1, 3, 4)
    AOD = {}
    for i in wavelengths:
        AOD[i] = _AODcalc(extcalc,profile_type,profile_params,i)
    return NumDens,mass_calc,vol_calc,no_mix_ratio,mass_mix_ratio,vol_mix_ratio,extcalc,scacalc,abscalc,ssacalc,gcalc,AOD
               
        
def run(input_dict):
    var = copy.deepcopy(input_dict)
    #Validation of input
    for i in var['Wavelengths']:
        if i not in [0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,
                     0.7,0.75,0.8,0.9,1.0,1.25,1.5,1.75,2.0,
                     2.5,3.0,3.2,3.39,3.5,3.75,4.0,4.5,5.0,
                     5.5,6.0,6.2,6.5,7.2,7.9,8.2,8.5,8.7,9.0,
                     9.2,9.5,9.8,10.0,10.6,11.0,11.5,12.5,13.0,
                     14.0,14.8,15.0,16.4,17.2,18.0,18.5,20.0,
                     21.3,22.5,25.0,27.9,30.0,35.0,40.0]:
            print("Error: Invalid wavelength selection\nExiting program")
            raise SystemExit
    if var['Layer1 relative humidity'] not in [0,50,70,80,90,95,98,99]:
        print("Error: Invalid relative humidity value\nExiting program")
        raise SystemExit
    if var['Layer2 relative humidity'] not in [0,50,70,80,90,95,98,99]:
        print("Error: Invalid relative humidity value\nExiting program")
        raise SystemExit
    if var['Layer3 relative humidity'] not in [0,50,70,80,90,95,98,99]:
        print("Error: Invalid relative humidity value\nExiting program")
        raise SystemExit
    if var['Layer4 relative humidity'] not in [0,50,70,80,90,95,98,99]:
        print("Error: Invalid relative humidity value\nExiting program")
        raise SystemExit
    if var['Layer5 relative humidity'] not in [0,50,70,80,90,95,98,99]:
        print("Error: Invalid relative humidity value\nExiting program")
        raise SystemExit
    if var['Layer6 relative humidity'] not in [0,50,70,80,90,95,98,99]:
        print("Error: Invalid relative humidity value\nExiting program")
        raise SystemExit
    if len(var['Layer1 component concentration'].keys()) != var['Maximum number of components'] or len(var['Layer2 component concentration'].keys()) != var['Maximum number of components'] or len(var['Layer3 component concentration'].keys()) != var['Maximum number of components'] or len(var['Layer4 component concentration'].keys()) != var['Maximum number of components'] or len(var['Layer5 component concentration'].keys()) != var['Maximum number of components'] or len(var['Layer6 component concentration'].keys()) != var['Maximum number of components']: 
        print("Error: Number of components specified and maximum number of components are not matching")
        raise SystemExit
    if var['Input unit'] != 1 and var['Input unit'] != 0:
        print("Error: Invalid input unit\nExiting program")
        raise SystemExit
    #Layer1
    NumDens1,mass_calc1,vol_calc1,no_mix_ratio1,mass_mix_ratio1,vol_mix_ratio1,extcalc1,scacalc1,abscalc1,ssacalc1,gcalc1,AOD1=_layerparams(
        var,var['Layer1 relative humidity'],var['Layer1 component concentration'],var['Maximum number of components'],
        var['Wavelengths'],var['Layer1 profile type'],var['Layer1 profile params'])
    #Layer2
    NumDens2,mass_calc2,vol_calc2,no_mix_ratio2,mass_mix_ratio2,vol_mix_ratio2,extcalc2,scacalc2,abscalc2,ssacalc2,gcalc2,AOD2=_layerparams(
        var,var['Layer2 relative humidity'],var['Layer2 component concentration'],var['Maximum number of components'],
        var['Wavelengths'],var['Layer2 profile type'],var['Layer2 profile params'])
    #Layer3
    NumDens3,mass_calc3,vol_calc3,no_mix_ratio3,mass_mix_ratio3,vol_mix_ratio3,extcalc3,scacalc3,abscalc3,ssacalc3,gcalc3,AOD3=_layerparams(
        var,var['Layer3 relative humidity'],var['Layer3 component concentration'],var['Maximum number of components'],
        var['Wavelengths'],var['Layer3 profile type'],var['Layer3 profile params'])
    #Layer4
    NumDens4,mass_calc4,vol_calc4,no_mix_ratio4,mass_mix_ratio4,vol_mix_ratio4,extcalc4,scacalc4,abscalc4,ssacalc4,gcalc4,AOD4=_layerparams(
        var,var['Layer4 relative humidity'],var['Layer4 component concentration'],var['Maximum number of components'],
        var['Wavelengths'],var['Layer4 profile type'],var['Layer4 profile params'])
    #Layer5
    NumDens5,mass_calc5,vol_calc5,no_mix_ratio5,mass_mix_ratio5,vol_mix_ratio5,extcalc5,scacalc5,abscalc5,ssacalc5,gcalc5,AOD5=_layerparams(
        var,var['Layer5 relative humidity'],var['Layer5 component concentration'],var['Maximum number of components'],
        var['Wavelengths'],var['Layer5 profile type'],var['Layer5 profile params'])
    #Layer6
    NumDens6,mass_calc6,vol_calc6,no_mix_ratio6,mass_mix_ratio6,vol_mix_ratio6,extcalc6,scacalc6,abscalc6,ssacalc6,gcalc6,AOD6=_layerparams(
        var,var['Layer6 relative humidity'],var['Layer6 component concentration'],var['Maximum number of components'],
        var['Wavelengths'],var['Layer6 profile type'],var['Layer6 profile params'])
    TotalAOD = {}
    for i in var['Wavelengths']:
        TotalAOD[i] = np.nansum([AOD1[i],AOD2[i],AOD3[i],AOD4[i],AOD5[i],AOD6[i]])
    layer1_params = {'Layer':1, 'Relative humidity':var['Layer1 relative humidity'], 'Number concentration (1/cm³)':NumDens1,'Mass concentration (ug/m³)':mass_calc1,'Volume concentration (um³/m³)':vol_calc1,
                     'Number mixing ratio':no_mix_ratio1,'Mass mixing ratio':mass_mix_ratio1,'Volume mixing ratio':vol_mix_ratio1,'Extinction coefficient (1/km)':extcalc1,
                     'Scattering coefficient (1/km)':scacalc1,'Absorption coefficient (1/km)':abscalc1,'SSA':ssacalc1,'g':gcalc1,'AOD':AOD1}
    layer2_params = {'Layer':2, 'Relative humidity':var['Layer2 relative humidity'], 'Number concentration (1/cm³)':NumDens2,'Mass concentration (ug/m³)':mass_calc2,'Volume concentration (um³/m³)':vol_calc2,
                     'Number mixing ratio':no_mix_ratio2,'Mass mixing ratio':mass_mix_ratio2,'Volume mixing ratio':vol_mix_ratio2,'Extinction coefficient (1/km)':extcalc2,
                     'Scattering coefficient (1/km)':scacalc2,'Absorption coefficient (1/km)':abscalc2,'SSA':ssacalc2,'g':gcalc2,'AOD':AOD2}
    layer3_params = {'Layer':3, 'Relative humidity':var['Layer3 relative humidity'], 'Number concentration (1/cm³)':NumDens3,'Mass concentration (ug/m³)':mass_calc3,'Volume concentration (um³/m³)':vol_calc3,
                     'Number mixing ratio':no_mix_ratio3,'Mass mixing ratio':mass_mix_ratio3,'Volume mixing ratio':vol_mix_ratio3,'Extinction coefficient (1/km)':extcalc3,
                     'Scattering coefficient (1/km)':scacalc3,'Absorption coefficient (1/km)':abscalc3,'SSA':ssacalc3,'g':gcalc3,'AOD':AOD3}
    layer4_params = {'Layer':4, 'Relative humidity':var['Layer4 relative humidity'], 'Number concentration (1/cm³)':NumDens4,'Mass concentration (ug/m³)':mass_calc4,'Volume concentration (um³/m³)':vol_calc4,
                     'Number mixing ratio':no_mix_ratio4,'Mass mixing ratio':mass_mix_ratio4,'Volume mixing ratio':vol_mix_ratio4,'Extinction coefficient (1/km)':extcalc4,
                     'Scattering coefficient (1/km)':scacalc4,'Absorption coefficient (1/km)':abscalc4,'SSA':ssacalc4,'g':gcalc4,'AOD':AOD4}
    layer5_params = {'Layer':5, 'Relative humidity':var['Layer5 relative humidity'], 'Number concentration (1/cm³)':NumDens5,'Mass concentration (ug/m³)':mass_calc5,'Volume concentration (um³/m³)':vol_calc5,
                     'Number mixing ratio':no_mix_ratio5,'Mass mixing ratio':mass_mix_ratio5,'Volume mixing ratio':vol_mix_ratio5,'Extinction coefficient (1/km)':extcalc5,
                     'Scattering coefficient (1/km)':scacalc5,'Absorption coefficient (1/km)':abscalc5,'SSA':ssacalc5,'g':gcalc5,'AOD':AOD5}
    layer6_params = {'Layer':6, 'Relative humidity':var['Layer6 relative humidity'], 'Number concentration (1/cm³)':NumDens6,'Mass concentration (ug/m³)':mass_calc6,'Volume concentration (um³/m³)':vol_calc6,
                     'Number mixing ratio':no_mix_ratio6,'Mass mixing ratio':mass_mix_ratio6,'Volume mixing ratio':vol_mix_ratio6,'Extinction coefficient (1/km)':extcalc6,
                     'Scattering coefficient (1/km)':scacalc6,'Absorption coefficient (1/km)':abscalc6,'SSA':ssacalc6,'g':gcalc6,'AOD':AOD6}
    output = {'AeroMix version': '1.0.0','Relative humidity':var['Layer1 relative humidity'],
              'Number concentration (1/cm³)':NumDens1,'Mass concentration (ug/m³)':mass_calc1,'Volume concentration (um³/m³)':vol_calc1,
                               'Number mixing ratio':no_mix_ratio1,'Mass mixing ratio':mass_mix_ratio1,'Volume mixing ratio':vol_mix_ratio1,'Extinction coefficient (1/km)':extcalc1,
                               'Scattering coefficient (1/km)':scacalc1,'Absorption coefficient (1/km)':abscalc1,'SSA':ssacalc1,'g':gcalc1,
                               'Total column AOD':TotalAOD,
                               'Layer1':layer1_params,
                               'Layer2':layer2_params,
                               'Layer3':layer3_params,
                               'Layer4':layer4_params,
                               'Layer5':layer5_params,
                               'Layer6':layer6_params,}
    return output
