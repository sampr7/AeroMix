#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AeroMix v 1.0.0 | Python package for modeling aerosol optical properties
Copyright © 2023  Sam P Raj
"""

import os
import sys
import numpy as np
from math import sqrt as sqrt
from numpy import log as ln
from numpy import log10 as log
from math import pi as pi
from math import exp as exp
from scipy.integrate import trapezoid as trap
import PyMieScatt as ps


def getSampleInputDict_ext():
    input_dict = {'Name':'new',
                  'Output directory':'def',
                  'Output filename':'custom10',
                  'RH':0,
                  'Minimum radius':5e-3,
                  'Maximum radius':20,
                  'Mode radius':1.18e-2,
                  'Std dev':2,
                  'Density': 1.8,
                  'Spectral refractive indices':
                      {0.25: (1.62+0.45j), 0.3: (1.74+0.47j),
                        0.35: (1.75+0.465j), 0.4: (1.75+0.46j),
                        0.45: (1.75+0.455j), 0.5: (1.75+0.45j),
                        0.55: (1.75+0.44j), 0.6: (1.75+0.435j),
                        0.65: (1.75+0.435j), 0.7: (1.75+0.43j),
                        0.75: (1.75+0.43j), 0.8: (1.75+0.43j), 
                        0.9: (1.75+0.435j), 1.0: (1.76+0.44j),
                        1.25: (1.76+0.45j), 1.5: (1.77+0.46j),
                        1.75: (1.79+0.48j), 2.0: (1.8+0.49j),
                        2.5: (1.82+0.51j), 3.0: (1.84+0.54j),
                        3.2: (1.86+0.54j), 3.39: (1.87+0.5495j), 
                        3.5: (1.88+0.56j), 3.75: (1.9+0.57j), 
                        4.0: (1.92+0.58j), 4.5: (1.94+0.59j), 
                        5.0: (1.97+0.6j), 5.5: (1.99+0.61j), 
                        6.0: (2.02+0.62j), 6.2: (2.03+0.625j),
                        6.5: (2.04+0.63j), 7.2: (2.06+0.65j),
                        7.9: (2.12+0.67j), 8.2: (2.13+0.68j),
                        8.5: (2.15+0.69j), 8.7: (2.16+0.69j),
                        9.0: (2.17+0.7j), 9.2: (2.18+0.7j),
                        9.5: (2.19+0.71j), 9.8: (2.2+0.715j),
                        10.0: (2.21+0.72j), 10.6: (2.22+0.73j),
                        11.0: (2.23+0.73j), 11.5: (2.24+0.74j),
                        12.5: (2.27+0.75j), 13.0: (2.28+0.76j),
                        14.0: (2.31+0.775j), 14.8: (2.33+0.79j),
                        15.0: (2.33+0.79j), 16.4: (2.36+0.81j),
                        17.2: (2.38+0.82j), 18.0: (2.4+0.825j),
                        18.5: (2.41+0.83j), 20.0: (2.45+0.85j),
                        21.3: (2.46+0.86j), 22.5: (2.48+0.87j),
                        25.0: (2.51+0.89j), 27.9: (2.54+0.91j),
                        30.0: (2.57+0.93j), 35.0: (2.63+0.97j),
                        40.0: (2.69+1j)}
                  }
    return input_dict
    
def getSampleInputDict_cs():
    input_dict = {'Name':'SSamBC_4',
                  'Output directory':'def',
                  'Output filename':'custom11',
                  'RH':50,
                  'Component file directory':'def',
                  'Core':'SSam',
                  'Shell':'BC',
                  'Method':'CSR',
                  'CSR':0.9,
                  'Mass of core':5,
                  'Mass of shell':2
                  }
    return input_dict

def _miecoeff(n,sigma,rad_array,lamb,rm,ref):
    bext_array = []
    bsca_array = []
    babs_array = []
    g_array = []
    for r in rad_array:  
        qext, qsca, qabs, g, qpr, qback, qratio = ps.MieQ(m = ref,
                                                          wavelength=lamb*1000,
                                                          diameter=r*2*1000,
                                                          asDict=False,
                                                          asCrossSection=False)    # Mie program
        bext = 1e-3*sqrt(pi/2.0)*(n/ln(sigma))*r*qext*exp(-0.5*(((ln(r/rm))**2)/(ln(sigma))**2)) # Mie coeff calculation
        bsca = 1e-3*sqrt(pi/2.0)*(n/ln(sigma))*r*qsca*exp(-0.5*(((ln(r/rm))**2)/(ln(sigma))**2)) # for log-normal dist.
        babs = 1e-3*sqrt(pi/2.0)*(n/ln(sigma))*r*qabs*exp(-0.5*(((ln(r/rm))**2)/(ln(sigma))**2))
        g_val = 1e-3*sqrt(pi/2.0)*(n/ln(sigma))*r*qsca*g*exp(-0.5*(((ln(r/rm))**2)/(ln(sigma))**2))
        bext_array.append(bext)
        bsca_array.append(bsca)
        babs_array.append(babs)
        g_array.append(g_val)
    return bext_array,bsca_array,babs_array,g_array

def ext_aerosol(input_dict):
    RMIN = input_dict['Minimum radius']
    RMAX = input_dict['Maximum radius']
    SIGMA = input_dict['Std dev']
    RMOD = input_dict['Mode radius']
    RHO = input_dict['Density']
    REF = input_dict['Spectral refractive indices']
    RH = input_dict['RH']
    wavelengths = list(input_dict['Spectral refractive indices'].keys())
    def_save_dir = (os.path.join(os.path.dirname(__file__), 'aerosol_components'))    
    save_dir = def_save_dir if input_dict['Output directory']=='def' else input_dict['Output directory']
    filename = input_dict['Output filename']+'_0'+str(RH) if input_dict['RH']==0 else input_dict['Output filename']+'_'+str(RH)
    """
    Creating radius array
    """
    xrmin = RMIN
    xrmax = RMAX
    deltar = 0.015
    xr = np.zeros(100000)
    xr[0] = xrmin
    ix = 1
    xranf = log(xrmin)
    while xr[ix-1] < xrmax:
        xrl = xranf+deltar*(ix-1)
        xr[ix] = 10**(xrl)
        ix = ix+1
    rad_array = xr[1:np.argmax(xr)+1]
    
    """
    Calculating mie coefficients
    """

    Bsca = {}
    Babs = {}
    Bext = {}
    SSA = {}
    g = {}
    ext_norm = {}
    real = {}
    img = {}
    for lamb in wavelengths:    # Calculation for each wavelengths
        bext_array,bsca_array,babs_array,g_array = _miecoeff(n=1,sigma=SIGMA,
                                                            rad_array=rad_array,
                                                            lamb=lamb,
                                                            rm=RMOD,ref=REF[lamb])
        bext = trap(bext_array,rad_array)
        bsca = trap(bsca_array,rad_array)
        babs = trap(babs_array,rad_array)
        ssa = bsca/bext
        g_val = (trap(g_array,rad_array))/bsca
        nan = np.nan
        Bsca[lamb] = bsca
        Babs[lamb] = babs
        Bext[lamb] = bext
        SSA[lamb] = ssa
        g[lamb] = g_val
        real[lamb] = REF[lamb].real
        img[lamb] = REF[lamb].imag*-1
    for lamb in wavelengths:
        ext_norm[lamb] = Bext[lamb]/Bext[0.55]
        
    RHOn = RHO
    
    """
            Write to output file          
    """
    OutFile = open(save_dir+'\\'+filename,'w') if sys.platform == 'Windows' else open(save_dir+'/'+filename,'w')
    OutFile.write('#'+input_dict['Name']+'_'+str(RH)+'\n')
    OutFile.write('# size distribution: lognormal\n')
    OutFile.write('#\tminimum radius[um]:\t'+str(RMIN)+'\n')
    OutFile.write('#\tmaximum radius[um]:\t'+str(RMAX)+'\n')
    OutFile.write('#\tsigma:\t'+str(SIGMA)+'\n')
    OutFile.write('#\trho[g/cm**3]:\t'+str(round(RHOn,2))+'\n')
    OutFile.write('#\tRmod [um]:\t'+str(RMOD)+'\n')
    OutFile.write('#optical parameters\n')
    OutFile.write("\t".join(['Wavelength[um]','Ext.Coeff[1/km]','Sca.Coeff[1/km]',
                              'Abs.Coeff[1/km]','si.sc.alb','asym.par','ext.nor',
                              'ref.real','ref.imag']))
    OutFile.write('\n')
    for i in wavelengths:
        OutFile.write(",\t".join(["{:e}".format(i),"{:e}".format(Bext[i]),
                                  "{:e}".format(Bsca[i]),"{:e}".format(Babs[i]),
                                  "{:e}".format(SSA[i]),"{:e}".format(g[i]),
                                  "{:e}".format(ext_norm[i]),str(real[i]),str(img[i])]))
        OutFile.write('\n')
    OutFile.close()
    print(filename+' is ready in '+save_dir)
    

def _ReadSizeMassData(comp_name,rh,input_dict):
    rh = str(rh) if rh>0 else '00'
    def_comp_dir = (os.path.join(os.path.dirname(__file__), 'aerosol_components'))
    comp_dir = def_comp_dir if input_dict['Component file directory']=='def' else input_dict['Component file directory']
    if comp_dir[-1] != '/' and sys.platform != 'Windows':
        comp_dir = comp_dir+'/'
    elif comp_dir[-1] != '\\' and sys.platform == 'Windows':
        comp_dir = comp_dir+'\\' 
    if not os.path.exists(comp_dir):
        print("Error: Component file directory"+comp_dir+" not found\nExiting program")
        raise SystemExit
    non_hs = {'IS','BC','MDnm','MDam','MDcm'}
    comp_name = comp_name+'00' if comp_name in non_hs else comp_name+'_'+rh if comp_name[:6] == 'custom' else comp_name+rh
    if not os.path.exists(comp_dir+comp_name):
        print("Error: Component file directory "+comp_dir+comp_name+" not found\nExiting program")
        raise SystemExit
    REF = {}
    OptDataFile = open(comp_dir+comp_name,'r')
    for line in OptDataFile:
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
        if ',' in line:
            wavelength,extc,scac,absc,ssa,g,extn,real,img = line.split(",")
            REF[float(wavelength)] = complex(float(real),-1*float(img))
    sizemassdata = {'Rmin':float(min_rad),'Rmax':float(max_rad),
              'sigma':float(sigma),'rho':float(rho),'Rmod':float(Rmod)}
    return sizemassdata,REF

def _csr(Mc,Ms,RHOc,RHOs):               # Calculate CSR
    ans = (1+((Ms*RHOc)/(Mc*RHOs)))**(-1/3)
    return round(ans,2)

def _csmiecoeff(n,sigma,rad_array,csr,lamb,rm,refc,refs):
    bext_array = []
    bsca_array = []
    babs_array = []
    g_array = []
    
    for r in rad_array:  
        Rc = r*csr      #Radius of core
        qext, qsca, qabs, g, qpr, qback, qratio = ps.MieQCoreShell(mCore = refc,
                                                                   mShell=refs,
                                                                   wavelength=lamb*1000,
                                                                   dCore=Rc*2*1000,
                                                                   dShell=r*2*1000,
                                                                   asDict=False,
                                                                   asCrossSection=False)    # Mie program
        bext = 1e-3*sqrt(pi/2.0)*(n/ln(sigma))*r*qext*exp(-0.5*(((ln(r/rm))**2)/(ln(sigma))**2)) # Mie coeff calculation
        bsca = 1e-3*sqrt(pi/2.0)*(n/ln(sigma))*r*qsca*exp(-0.5*(((ln(r/rm))**2)/(ln(sigma))**2)) # for log-normal dist.
        babs = 1e-3*sqrt(pi/2.0)*(n/ln(sigma))*r*qabs*exp(-0.5*(((ln(r/rm))**2)/(ln(sigma))**2))
        g_val = 1e-3*sqrt(pi/2.0)*(n/ln(sigma))*r*qsca*g*exp(-0.5*(((ln(r/rm))**2)/(ln(sigma))**2))
        bext_array.append(bext)
        bsca_array.append(bsca)
        babs_array.append(babs)
        g_array.append(g_val)
    return bext_array,bsca_array,babs_array,g_array

def cs_aerosol(input_dict):
    c_data,c_ref = _ReadSizeMassData(input_dict['Core'],input_dict['RH'],input_dict)
    s_data,s_ref = _ReadSizeMassData(input_dict['Shell'],input_dict['RH'],input_dict)
    if input_dict['Method'] == 'CSR':
        CSR = input_dict['CSR']
        if CSR < 0 or CSR > 1:
            print("Error: Invalid Core to shell radius ratio. Enter a value between 0 and 1")
            raise SystemExit
    elif input_dict['Method'] == 'mass':
        CSR = _csr(input_dict['Mass of core'],input_dict['Mass of shell'],c_data['rho'],s_data['rho'])
    else:
        print('only \'CSR\' or \'mass\' are acceptble inputs for Method. Check your input dictionary.')
        raise SystemExit
    """
    Creating radius array
    """
    xrmin = s_data['Rmin']
    xrmax = s_data['Rmax']
    deltar = 0.015
    xr = np.zeros(100000)
    xr[0] = xrmin
    ix = 1
    xranf = log(xrmin)
    while xr[ix-1] < xrmax:
        xrl = xranf+deltar*(ix-1)
        xr[ix] = 10**(xrl)
        ix = ix+1
    rad_array = xr[1:np.argmax(xr)+1]
    
    """
    Calculating mie coefficients
    """

    Bsca = {}
    Babs = {}
    Bext = {}
    SSA = {}
    g = {}
    ext_norm = {}
    real = {}
    img = {}
    for lamb in list(s_ref.keys()):    # Calculation for each wavelengths
        bext_array,bsca_array,babs_array,g_array = _csmiecoeff(n=1,sigma=s_data['sigma'],
                                                            rad_array=rad_array,
                                                            csr=CSR,lamb=lamb,
                                                            rm=s_data['Rmod'],refc=c_ref[lamb],
                                                            refs=s_ref[lamb])
        bext = trap(bext_array,rad_array)
        bsca = trap(bsca_array,rad_array)
        babs = trap(babs_array,rad_array)
        ssa = bsca/bext
        g_val = (trap(g_array,rad_array))/bsca
        nan = 999
        Bsca[lamb] = bsca
        Babs[lamb] = babs
        Bext[lamb] = bext
        SSA[lamb] = ssa
        g[lamb] = g_val
        real[lamb] = nan
        img[lamb] = nan
    for lamb in list(s_ref.keys()):
        ext_norm[lamb] = Bext[lamb]/Bext[0.55]
        
    RHOn = c_data['rho']*(CSR**3)+s_data['rho']*(1-(CSR**3))
     
    """
            Write to output file          
    """
    def_save_dir = (os.path.join(os.path.dirname(__file__), 'aerosol_components'))    
    save_dir = def_save_dir if input_dict['Output directory']=='def' else input_dict['Output directory']
    filename = input_dict['Output filename']+'_0'+str(input_dict['RH']) if input_dict['RH']==0 else input_dict['Output filename']+'_'+str(input_dict['RH'])
    OutFile = open(save_dir+'\\'+filename,'w') if sys.platform == 'Windows' else open(save_dir+'/'+filename,'w')
    OutFile.write('#'+input_dict['Core']+input_dict['Shell']+'_'+str(round(CSR,2))+str(input_dict['RH'])+'\n')
    OutFile.write('# size distribution: lognormal\n')
    OutFile.write('#\tminimum radius[um]:\t'+str(s_data['Rmin'])+'\n')
    OutFile.write('#\tmaximum radius[um]:\t'+str(s_data['Rmax'])+'\n')
    OutFile.write('#\tsigma:\t'+str(s_data['sigma'])+'\n')
    OutFile.write('#\trho[g/cm**3]:\t'+str(round(RHOn,2))+'\n')
    OutFile.write('#\tRmod [um]:\t'+str(s_data['Rmod'])+'\n')
    OutFile.write('#optical parameters\n')
    OutFile.write("\t".join(['Wavelength[um]','Ext.Coeff[1/km]','Sca.Coeff[1/km]',
                             'Abs.Coeff[1/km]','si.sc.alb','asym.par','ext.nor',
                             'ref.real','ref.imag']))
    OutFile.write('\n')
    for i in list(s_ref.keys()):
        OutFile.write(",\t".join(["{:e}".format(i),"{:e}".format(Bext[i]),
                                 "{:e}".format(Bsca[i]),"{:e}".format(Babs[i]),
                                 "{:e}".format(SSA[i]),"{:e}".format(g[i]),
                                 "{:e}".format(ext_norm[i]),str(real[i]),str(img[i])]))
        OutFile.write('\n')
    OutFile.close()
    
    
