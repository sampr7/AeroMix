# AeroMix documentation

*by [Sam P Raj](https://github.com/sampr7/) and [P R Sinha](https://www.iist.ac.in/ess/prs)*  
*Department of Earth and Space Sciences*  
*[Indian Institute of Space Science and Technology, Thiruvananthapuram](https://www.iist.ac.in/), IN*  

This document outlines the guidelines for installing and using the AeroMix Python package.

## Installation

Use the package manager [pip](https://pypi.org/) to install AeroMix.

```bash
pip install AeroMix
```
## Usage
AeroMix is a versatile Python package designed for computing a wide range of optical and physical properties of aerosol mixtures using the inputs on component-wise aerosol number/mass concentration, wavelengths, relative humidity, and aerosol vertical profile information. The output parameters of AeroMix encompasses the aerosol optical properties such as,

1. Aerosol optical depth (AOD)
2. Single scattering albedo (SSA)
3. Asymmetry parameter (g)
4. Extinction coefficient ($\\beta\_{ext}$)
5. Scattering coefficient ($\\beta\_{sca}$)
6. Absorption coefficient ($\\beta\_{abs}$)

and the physical properties, such as

1. Mass concentration
2. Number concentration
3. Volume concentration
4. Mass mixing ratio
5. Number mixing ratio
6. Volume mixing ratio

### Configuring AeroMix inputs
AeroMix operates by taking a dictionary of input parameters, which include information about the aerosol concentration, wavelengths of interest, relative humidity, and vertical profile of the aerosol layer. Sample input dictionaries in the required format are given for ten different aerosol mixtures. The *getAerosolType* function is provided to help users generate a sample input dictionary. This function returns a dictionary pre-filled with default values for a specified aerosol type, which can then be modified as needed.

***AeroMix.getAerosolType(aerosol_type, [wavelength_array], mixed_layer_relative_humidity,max_no_comps)***

> Parameters:
>
> *aerosol_type* (str):  A string representing the type of aerosol. Predefined types are  (*'default','urban','continental clean','continental average','continental polluted','desert',''desert',maritime clean','maritime polluted','maritime tropical','antarctic','arctic'*).
>
> *Wavelength_array* (1D array of floats):An array specifying the wavelengths (in µm) at which the optical properties are to be calculated. Acceptable values are *[0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.2, 3.39, 3.5, 3.75, 4.0, 4.5, 5.0, 5.5, 6.0, 6.2, 6.5, 7.2, 7.9, 8.2, 8.5, 8.7, 9.0, 9.2, 9.5, 9.8, 10.0, 10.6, 11.0, 11.5, 12.5, 13.0, 14.0, 14.8, 15.0, 16.4, 17.2, 18.0, 18.5, 20.0, 21.3, 22.5, 25.0, 27.9, 30.0, 35.0, 40.0]*.
>
> *mixed_layer_relative_humidity* (int): An integer representing the relative humidity percentage in the mixed layer. Acceptable values are (*0,50,70,80,90,95,98,99*)
> 
> *max_no_comps* (int): Maximum number of aerosol components to constitute the mixture.
> 
> Returns:
>
> A dictionary containing input parameters for running AeroMix. 
>


This dictionary can be used as an input for the AeroMix to run to calculate the optical properties of respective aerosol mixtures. The parameters in this dictionary can be edited, or a new dictionary in the same format can be created to define custom aerosol mixtures. Here is an example of how to generate an input dictionary and modify it:
```python
import AeroMix
# get a sample input dictionary
input_dict = AeroMix.getAerosolType('urban',[0.4,0.5,0.6,0.7,0.8],80)
# changing the maximum number of components and adjusting number concentrations of components in each layer
input_dict['Maximum number of components'] = 9
input_dict['Layer1 component concentration'] = {1: 0,2: 2200,3: 0,4: 0,5: 0.001,6: 0,7: 0,8: 0,9:0}
input_dict['Layer2 component concentration'] = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9:0}
input_dict['Layer3 component concentration'] = {1: 0.0013,2: 438.0,3: 438.0,4: 0,5: 0,6: 0,7: 0,8: 0,9:0}
input_dict['Layer4 component concentration'] = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9:3}
input_dict['Layer5 component concentration'] = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9:0}
input_dict['Layer6 component concentration'] = {1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9:0}
# changing the aerosol profile type in layer 3
input_dict['Layer3 profile type'] = 0
```

### Running AeroMix
The *run* function in AeroMix calculates the optical and physical properties of aerosols based on the provided input parameters.

***AeroMix.run(input_dict)***

> Parameters:
>
> *input_dict* (dict):  A dictionary containing the input parameters for the AeroMix. This includes:
>
> > *input_dict['Wavelengths']* (1D array of floats): An array specifying the wavelengths (in µm) at which the optical properties are to be calculated. Acceptable values are *[0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.2, 3.39, 3.5, 3.75, 4.0, 4.5, 5.0, 5.5, 6.0, 6.2, 6.5, 7.2, 7.9, 8.2, 8.5, 8.7, 9.0, 9.2, 9.5, 9.8, 10.0, 10.6, 11.0, 11.5, 12.5, 13.0, 14.0, 14.8, 15.0, 16.4, 17.2, 18.0, 18.5, 20.0, 21.3, 22.5, 25.0, 27.9, 30.0, 35.0, 40.0]*.
> >
> > *input_dict['Maximum radius']* (float): The maximum radius of aerosol particles, setting the upper limit of the size distribution for the calculation of mass and volume.
> >
> > *input_dict['Maximum number of components']* (int): Maximum number of aerosol components to constitute the mixture.
> >
> > *input_dict['Component file directory']* (str): Path to the aerosol database. Put *'def'* for the default directory.
> >
> > *input_dict['Input unit']* (int): The unit of aerosol concentration input. Use 0 for number concentration (N cm<sup>-3</sup>) and  1 for mass concentration (µg cm<sup>-3</sup>). This setting is common for all layers.
> >
> > *input_dict['Layer1 profile type']* (int): Function type representing aerosol vertical profile in the first vertical layer (mixed layer). Use 0 for exponential function, 1 for a homogenous layer and 2 for a cubic function.
> >
> > *input_dict['Layer1 relative humidity']* (int): An integer representing the relative humidity percentage in the first vertical layer. Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> > *input_dict['Layer1 profile params']* (1D array of floats):  Parameters defining the thickness of first layer and distribution of aerosols in it. \[Layer base height, Layer top height, Scale height\] if *input_dict['Layer1 profile type']=0*. [Layer base height, Layer top height] if *input_dict['Layer1 profile type']=1* and  [Layer base height, Layer top height, a,b,c,d] if *input_dict['Layer1 profile type']=2* where a,b,c and d are the coefficients of cubic function ah<sup>3</sup>+bh<sup>2</sup>+ch+d.
> >
> > *input_dict['Layer1 component concentration']* (Dict of floats):  Dictionary specifying the number or mass concentration of aerosol components in the first layer of the atmosphere. Assign zero for components not present in the mixture. Ensure that the total count of components matches the value specified in *input_dict['Maximum number of components']*. The component numbers from 1 to 9 are reserved for predefined aerosol components representing the number or mass concentrations of water-insoluble, water-soluble, black carbon, sea-salt accumulation mode, sea-salt coarse mode, mineral dust nucleation mode, mineral dust accumulation mode, mineral dust coarse mode and stratospheric sulfate aerosols. Component number 10 and onwards can be used for user defined aerosol components.
> >
> > Example:
> >
> > ```python
> > input_dict['Layer1 component concentration'] = {1: 1.5,2: 28000,3: 130000,4: 0,5: 0,6: 0,7: 0,8: 0, 9: 0,10: 0,11: 0,12: 0,13: 0,14: 0,15: 0}
> > ```
> > For each layer *x* from 2 to 6,
> > 
> > *input_dict['Layerx profile type']* (int): Function type representing aerosol vertical profile in the vertical layer *x*. Use 0 for exponential function, 1 for a homogenous layer and 2 for a cubic function.
> >
> > *input_dict['Layerx relative humidity']* (int): An integer representing the relative humidity percentage in the vertical layer *x*. Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> > *input_dict['Layerx profile params']* (1D array of floats):   Parameters defining the thickness of layer *x* and distribution of aerosols in it. \[Layer base height, Layer top height, Scale height\] if *input_dict['Layerx profile type']=0*. [Layer base height, Layer top height, 1] if *input_dict['Layerx profile type']=1* and  [Layer base height, Layer top height, a,b,c,d] if *input_dict['Layerx profile type']=2* where a,b,c and d are the coefficients of cubic function ah<sup>3</sup>+bh<sup>2</sup>+ch+d.
> >
> > *input_dict['Layerx component concentration']* (Dict of floats):  Dictionary of number concentration or mass concentration of aerosol components constituting the mixture in vertical layer *x*. Set zero for non-constituting compoenents. The total number of components should be same as that of *input_dict['Maximum number of components']*. The component numbers from 1 to 9 are reserved for predefined aerosol components representing the number or mass concentrations of water-insoluble, water-soluble, black carbon, sea-salt accumulation mode, sea-salt coarse mode, mineral dust nucleation mode, mineral dust accumulation mode, mineral dust coarse mode and stratospheric sulfate aerosols. Component number 10 and onwards can be used for user defined aerosol components.
> >
>
> Returns:
>
> Dictionary of output parameters.
> > *output_dict['Relative humidity']*: Relative humidity used for calculations in the first vertical layer.
> > 
> > *output_dict['Number concentration)']*: Number concentration of aerosol components in the first vertical layer.
> > 
> > *output_dict['Mass concentration']*: Mass concentration of aerosol components in the first vertical layer.
> > 
> > *output_dict['Volume concentration']*: Volume concentration of aerosol components in the first vertical layer.
> > 
> > *output_dict['Number mixing ratio']*: Number mixing ratio of aerosol components in the first vertical layer.
> > 
> > *output_dict['Mass mixing ratio']*: Mass mixing ratio of aerosol components in the first vertical layer.
> > 
> > *output_dict['Volume mixing ratio']*: Volume mixing ratio of aerosol components in the first vertical layer.
> > 
> > *output_dict['Extinction coefficient']*: Extinction cofficient at the first vertical layer.
> > 
> > *output_dict['Scattering coefficient']*: Scattering cofficient at the first vertical layer.
> > 
> > *output_dict['Absorption coefficient']*: Absorption cofficient at the first vertical layer.
> > 
> > *output_dict['SSA']*: Single scattering albedo at the first vertical layer.
> > 
> > *output_dict['g']*: Asymmetry parameter at the first vertical layer.
> > 
> > *output_dict['Total column AOD']*: Total column Aerosol optical depth.
> > 
> > *output_dict['Units']*: Units of the output parameters.
> > 
> > For each layer *x* from 1 to 6,
> > 
> > *output_dict['Layerx']['Layer']*: Layer number
> > 
> > *output_dict['Layerx']['Relative humidity']*: Relative humidity used to calculate the results in the layer *x*.
> > 
> > *output_dict['Layerx']['Number concentration']*: Number concentration of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Mass concentration']*: Mass concentration of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Volume concentration']*: Volume concentration of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Number mixing ratio']*: Number mixing ratio of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Mass mixing ratio']*: Mass mixing ratio of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Volume mixing ratio']*: Volume mixing ratio of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Extinction coefficient']*: Extinction cofficient in the layer *x*.
> > 
> > *output_dict['Layerx']['Absorption coefficient']*: Absorption cofficient in the layer *x*.
> > 
> > *output_dict['Layerx']['SSA']*: Single scattering albedo in the layer *x*.
> > 
> > *output_dict['Layerx']['g']*: Asymmetry parameter in the layer *x*.
> > 
> > *output_dict['Layerx']['AOD']*: Aerosol optical depth in the layer *x*.
> 
> Example
> ```python
> In[1]: import AeroMix
> # Running AeroMix
> In[2]: input_dict = AeroMix.getAerosolType('urban',[0.4,0.5,0.6,0.7,0.8],80)
> In[3]: output = AeroMix.run(input_dict)
> # Accessing output parameters
> In[4]: print(output['Total column AOD'])
> Out[4]: 
> {0.4: 0.9523364416499044, 0.5: 0.7304236336114844, 0.6: 0.5715173653793031, 0.7: 0.45918529871590336, 0.8: 0.37323228400622516}
> In[5]: print(output['Absorption coefficient (1/km)'])
> Out[5]: {0.4: 0.09103009999999999, 0.5: 0.07176779999999999, 0.6: 0.0584251, 0.7: 0.0495307, 0.8: 0.0440769}
> In[6]: print(output['Layer3']['Scattering coefficient'])
> Out[6]: {0.4: 0.0043851591, 0.5: 0.003322391, 0.6: 0.0025509650999999997, 0.7: 0.0019946607000000003, 0.8: 0.0015466363799999999}
> ```
### Creating custom aerosol database
AeroMix utilizes the aerosol size distribution and optical data from Koepke et al. (1997), [Hess et. al (1998)](https://doi.org/10.1175/1520-0477(1998)079<0831:OPOAAC>2.0.CO;2) and [Koepke et al. (2015)](https://doi.org/10.5194/acp-15-5947-2015). Users can incorporate custom aerosol databases into AeroMix by specifying the database location in the input dictionary using *input_dict['Component file directory']*. To create a custom aerosol database, first copy the default database to your desired location using:

***AeroMix.CopyAerosolData(data_dir)***
> Parameters:
>
> *data_dir* (str):  The target location where the database will be copied.
>  
>  Returns:
>  Database directory copied to target location.


#### Modeling externally mixed aerosol component

Create new aerosol components in an externally mixed state (where one component constitutes a particle) using:

***AeroMix.ext_aerosol(ext_input)***
> Parameters:
>
> *ext_input* (dict):  Dictionary containing input parameters for the new component, including:
> >
> > *ext_input['Name']* (str): Name of the component
> >
> > *ext_input['Output directory']* (str): Location to save the component data file.
> > 
> > *ext_input['Output filename']* (str): Filename of the component data file in the format customxx where xx is the assigned component number to call in AeroMix. Component number for custom aerosol components should be greater than 9 and unique.
> >
> > *ext_input['RH']* (int): Relative humidity corresponding to the size distribution parameters and refractive indices of the component. Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> > *ext_input['Minimum radius']* (float): Lower limit of the radius in the particle size distribution (log-normal) in µm.
> > 
> > *ext_input['Maximum radius']* (float): Upper limit of the radius in the particle size distribution (log-normal) in µm.
> >  
> > *ext_input['Mode radius']* (float): Mode radius of the particle size distribution (log-normal) in µm.
> >  
> > *ext_input['Std dev']* (float): Standard deviation of the particle size distribution (log-normal).
> >
> > *ext_input['Density']* (float): Specific mass density of the component in g cm<sup>-3</sup>.
> >
> > *ext_input['Spectral refractive indices']* (Dict of complex numbers): Complex refractive indices in the form (m+kj) for each wavelength in the list *[0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.2, 3.39, 3.5, 3.75, 4.0, 4.5, 5.0, 5.5, 6.0, 6.2, 6.5, 7.2, 7.9, 8.2, 8.5, 8.7, 9.0, 9.2, 9.5, 9.8, 10.0, 10.6, 11.0, 11.5, 12.5, 13.0, 14.0, 14.8, 15.0, 16.4, 17.2, 18.0, 18.5, 20.0, 21.3, 22.5, 25.0, 27.9, 30.0, 35.0, 40.0]*. m and k are the real and imaginary part of the refractive index.
> >
> > Example
> > ```python
> > input_dict['Spectral refractive indices'] = {0.25: (1.62+0.45j), 0.3: (1.74+0.47j),0.35: (1.75+0.465j),
> >                        0.4: (1.75+0.46j),0.45: (1.75+0.455j), 0.5: (1.75+0.45j),
> >                        0.55: (1.75+0.44j), 0.6: (1.75+0.435j),0.65: (1.75+0.435j),
> >                        0.7: (1.75+0.43j),0.75: (1.75+0.43j), 0.8: (1.75+0.43j), 
> >                        0.9: (1.75+0.435j), 1.0: (1.76+0.44j),1.25: (1.76+0.45j),
> >                        1.5: (1.77+0.46j), 1.75: (1.79+0.48j), 2.0: (1.8+0.49j),
> >                        2.5: (1.82+0.51j), 3.0: (1.84+0.54j), 3.2: (1.86+0.54j),  
> >                        3.39: (1.87+0.5495j), 3.5: (1.88+0.56j), 3.75: (1.9+0.57j),
> >                        4.0: (1.92+0.58j), 4.5: (1.94+0.59j),  5.0: (1.97+0.6j),
> >                        5.5: (1.99+0.61j), 6.0: (2.02+0.62j), 6.2: (2.03+0.625j),
> >                        6.5: (2.04+0.63j), 7.2: (2.06+0.65j), 7.9: (2.12+0.67j), 
> >                        8.2: (2.13+0.68j), 8.5: (2.15+0.69j), 8.7: (2.16+0.69j),
> >                        9.0: (2.17+0.7j), 9.2: (2.18+0.7j), 9.8: (2.2+0.715j),
> >                        9.5: (2.19+0.71j), 10.0: (2.21+0.72j), 10.6: (2.22+0.73j),
> >                        11.0: (2.23+0.73j), 11.5: (2.24+0.74j), 12.5: (2.27+0.75j),
> >                        13.0: (2.28+0.76j), 14.0: (2.31+0.775j), 14.8: (2.33+0.79j),
> >                        15.0: (2.33+0.79j), 16.4: (2.36+0.81j), 17.2: (2.38+0.82j),
> >                        18.0: (2.4+0.825j), 18.5: (2.41+0.83j), 20.0: (2.45+0.85j),
> >                        22.5: (2.48+0.87j), 25.0: (2.51+0.89j), 27.9: (2.54+0.91j),
> >                        30.0: (2.57+0.93j), 35.0: (2.63+0.97j), 40.0: (2.69+1j)}
> > ```
> Returns
> 
> A datafile containing mie coefficients normalised for one particle of the component.
>


A sample input dictionary for modeling externally mixed aerosols can be loaded using 

***AeroMix.getSampleInputDict_ext()***

>  
>  Returns:
>  A dictionary of input parameters for modeling an externally mixed aerosol component.
  
#### Modeling core-shell mixed aerosol component

Create aerosol components in a core-shell mixed state (two components forming a core-shell structure) using:

***AeroMix.cs_aerosol(cs_input)***
> Parameters:
>
> *cs_input* (dict):  Dictionary containing input parameters for the new core-shell mixed component, including:
> >
> > *cs_input['Name']* (str): Name of the component
> > 
> > *cs_input['Output directory']* (str): Target location to save the component data file.
> > 
> > *cs_input['Output filename']* (str): Filename of the component data file. Name should be in the format customxx where xx is the assigned component number to call in AeroMix. Component number for custom aerosol components should be greater than 9 and unique.
> >
> > *cs_input['RH']* (int): Relative humidity corresponding to the size distribution parameters and refractive indices of the component. Acceptable values are (*0,50,70,80,90,95,98,99*).
> > 
> > *cs_input['Component file directory']* (str): Location where the core and shell component datafiles are located. Use 'def' to use predefined components.
> > *cs_input['Core']* (str): Name of the datafile of the core component without relative humidity value. Predefined components are 'IS','WS','BC','SSam','SScm','MDnm','MDam','MDcm' and 'SUSO'.
> > 
> > *cs_input['Shell']* (str): Name of the datafile of the shell component without relative humidity value. Predefined components are 'IS','WS','BC','SSam','SScm','MDnm','MDam','MDcm' and 'SUSO'.
> > 
> > *cs_input['Method']* (str): The method to input core to shell radius ratio (CSR) of the component. Put 'CSR' if the CSR value need to specified directely or put 'mass' for the program to calculate the CSR value from the mass of core and shell component.
> > 
> > *cs_input['CSR']* (float): Core to shell radius ratio (CSR) of the component. Will not be used if *input_dict['Method']* = 'mass'.
> > 
> > *cs_input['Mass of core']* (float): Mass of core component participating in the core-shell mixing. Will not be used if *input_dict['Method']* = 'CSR'.
> > 
> > *cs_input['Mass of shell']* (float): Mass of shell component participating in the core-shell mixing. Will not be used if *cs_input['Method']* = 'CSR'.
> > 
> Returns  
> A datafile containing mie coefficients normalised for one particle of the component.
>

A sample input dictionary for modeling core-shell mixed aerosols can be loaded using 

***AeroMix.getSampleInputDict_cs()***

>  
>  Returns:
>  Dictionary of input parameters required for modeling an externally mixed aerosol component

## Sample program
A [Python code](https://github.com/sampr7/AeroMix/blob/main/AeroMix_test.py) demonstrating the above-mentioned functions is available in the GitHub page.

## Contact
We are continuously working to improve and enhance the capabilities of our package. Your feedback, suggestions, and reports of any bugs you encounter are incredibly valuable to us. We welcome you to join the discussion on our [GitHub page](https://github.com/sampr7)  or feel free to reach out directly via email. Please send your thoughts and reports to sampr7@gmail.com. 
