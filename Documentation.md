# AeroMix documentation

Documentation of the AeroMix Python package

## Installation

Use the package manager [pip](https://pypi.org/) to install AeroMix.

```bash
pip install AeroMix
```
## Usage
AeroMix requires the inputs of component-wise aerosol number/mass concentration, wavelengths, relative humidity, and aerosol vertical profile information to calculate the optical properties, such as

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

AeroMix takes input as a dictionary of input parameters. Sample input dictionaries in the required format are given for ten different aerosol mixtures. This can be loaded as

***AeroMix.getAerosolType(aerosol_type, [wavelength_array], mixed_layer_relative_humidity)***

> Parameters:
>
> *aerosol_type* (str):  Name of the aerosol type from  (*'default','urban','continental clean','continental average','continental polluted','desert',''desert',maritime clean','maritime polluted','maritime tropical','antarctic','arctic'*).
>
> *Wavelength_array* (1D array of floats): Wavelength values at which optical properties need to be calculated. Acceptable values are *[0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.2, 3.39, 3.5, 3.75, 4.0, 4.5, 5.0, 5.5, 6.0, 6.2, 6.5, 7.2, 7.9, 8.2, 8.5, 8.7, 9.0, 9.2, 9.5, 9.8, 10.0, 10.6, 11.0, 11.5, 12.5, 13.0, 14.0, 14.8, 15.0, 16.4, 17.2, 18.0, 18.5, 20.0, 21.3, 22.5, 25.0, 27.9, 30.0, 35.0, 40.0]*.
>
> *mixed_layer_relative_humidity* (int): Relative humidity value at the mixed layer. Acceptable values are (*0,50,70,80,90,95,98,99*)
>
> Returns:
>
> Dictionary of input parameters required for running AeroMix.
>
> Example:
>
> ```python
> import AeroMix
> 
> # get a sample input dictionary
> input_dict = AeroMix.getAerosolType('urban',[0.4,0.5,0.6,0.7,0.8],80)
> ```

This dictionary can be used as an input for the AeroMix to run to calculate the optical properties of respective aerosol mixtures. The parameters in this dictionary can be edited, or a new dictionary in the same format can be created to define custom aerosol mixtures.

To calculate the optical properties, run

***AeroMix.run(input_dict)***

> Parameters:
>
> *input_dict* (dict):  Dictionary of input parameters.
>
> > *input_dict['Wavelengths']* (1D array of floats): Wavelength values at which optical properties need to be calculated. Acceptable values are *[0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.2, 3.39, 3.5, 3.75, 4.0, 4.5, 5.0, 5.5, 6.0, 6.2, 6.5, 7.2, 7.9, 8.2, 8.5, 8.7, 9.0, 9.2, 9.5, 9.8, 10.0, 10.6, 11.0, 11.5, 12.5, 13.0, 14.0, 14.8, 15.0, 16.4, 17.2, 18.0, 18.5, 20.0, 21.3, 22.5, 25.0, 27.9, 30.0, 35.0, 40.0]*.
> >
> > *input_dict['Maximum radius']* (float): Maximum radius of aerosols. This sets the upper limit of the size distribution for the calculation of mass and volume.
> >
> > *input_dict['Maximum number of components']* (int): Maximum number of aerosol components in the mixture.
> >
> > *input_dict['Component file directory']* (str): Path to the aerosol database. Put *'def'* to use default directory.
> >
> > *input_dict['Input unit']* (int): Unit of aerosol concentration input. Select 0 for number concentration (N cm^-3) and  1 for mass concentration (µg cm<sup>-3</sup>).
> >
> > *input_dict['Layer1 profile type']* (int): Type of function to represent aerosol vertical profile in the first vertical layer (mixed layer). Select 0 for exponential function, 1 for a homogenous layer and 2 for a cubic function.
> >
> > *input_dict['Layer1 relative humidity']* (int): Relative humidity value at the first vertical layer (mixed layer). Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> > *input_dict['Layer1 profile params']* (1D array of floats):  Parameters defining the thickness of first layer and distribution of aerosols in it. \[Layer base height, Layer top height, Scale height\] if *input_dict['Layer1 profile type']=0*. [Layer base height, Layer top height, 1] if *input_dict['Layer1 profile type']=1* and  [Layer base height, Layer top height, a,b,c,d] if *input_dict['Layer1 profile type']=2* where a,b,c and d are the coefficients of cubic function ah<sup>3</sup>+bh<sup>2</sup>+ch+d.
> >
> > *input_dict['Layer1 component concentration']* (Dict of floats):  Dictionary of number concentration or mass concentration of aerosol components constituting the mixture in first layer. Set zero for non-constituting compoenents. The total number of components should be same as that of *input_dict['Maximum number of components']*. For the default dataset, the components 1 to 9 represents the number or mass concentrations of water-insoluble, water-soluble, black carbon, sea-salt accumulation mode, sea-salt coarse mode, mineral dust nucleation mode, mineral dust accumulation mode, mineral dust coarse mode and stratospheric sulfate aerosols. Component number 10 onwards can be used for user defined aerosol components.
> >
> > Example:
> >
> > ```python
> > input_dict['Layer1 component concentration'] = {1: 1.5,2: 28000,3: 130000,4: 0,5: 0,6: 0,7: 0,8: 0, 9: 0,10: 0,11: 0,12: 0,13: 0,14: 0,15: 0}
> > ```
> >
> > *input_dict['Layer2 profile type']* (int): Type of function to represent aerosol vertical profile in the second vertical layer. Select 0 for exponential function, 1 for a homogenous layer and 2 for a cubic function.
> >
> > *input_dict['Layer2 relative humidity']* (int): Relative humidity value at the second vertical layer. Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> > *input_dict['Layer2 profile params']* (1D array of floats):  Parameters defining the thickness of second layer and distribution of aerosols in it. [Layer base height, Layer top height, Scale height] if *input_dict['Layer1 profile type']=0*. [Layer base height, Layer top height, 1] if *input_dict['Layer1 profile type']=1* and  [Layer base height, Layer top height, a,b,c,d] if *input_dict['Layer1 profile type']=2* where a,b,c and d are the coefficients of cubic function ah<sup>3</sup>+bh<sup>2</sup>+ch+d.
> >
> > *input_dict['Layer2 component concentration']* (Dict of floats):  Dictionary of number concentration or mass concentration of aerosol components constituting the mixture in second layer. Set zero for non-constituting compoenents. The total number of components should be same as that of *input_dict['Maximum number of components']*. For the default dataset, the components 1 to 9 represents the number or mass concentrations of water-insoluble, water-soluble, black carbon, sea-salt accumulation mode, sea-salt coarse mode, mineral dust nucleation mode, mineral dust accumulation mode, mineral dust coarse mode and stratospheric sulfate aerosols. Component number 10 onwards can be used for user defined aerosol components.
> >
> > *input_dict['Layer3 profile type']* (int): Type of function to represent aerosol vertical profile in the third vertical layer. Select 0 for exponential function, 1 for a homogenous layer and 2 for a cubic function.
> >
> > *input_dict['Layer3 relative humidity']* (int): Relative humidity value at the third vertical layer. Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> >*input_dict['Layer3 profile params']* (1D array of floats):  Parameters defining the thickness of third layer and distribution of aerosols in it. [Layer base height, Layer top height, Scale height] if *input_dict['Layer1 profile type']=0*. [Layer base height, Layer top height, 1] if *input_dict['Layer1 profile type']=1* and [Layer base height, Layer top height, a,b,c,d] if *input_dict['Layer1 profile type']=2* where a,b,c and d are the coefficients of cubic function ah<sup>3</sup>+bh<sup>2</sup>+ch+d.
> >
> > *input_dict['Layer3 component concentration']* (Dict of floats):  Dictionary of number concentration or mass concentration of aerosol components constituting the mixture in third layer. Set zero for non-constituting compoenents. The total number of components should be same as that of *input_dict['Maximum number of components']*. For the default dataset, the components 1 to 9 represents the number or mass concentrations of water-insoluble, water-soluble, black carbon, sea-salt accumulation mode, sea-salt coarse mode, mineral dust nucleation mode, mineral dust accumulation mode, mineral dust coarse mode and stratospheric sulfate aerosols. Component number 10 onwards can be used for user defined aerosol components.
> >
> > *input_dict['Layer4 profile type']* (int): Type of function to represent aerosol vertical profile in the fourth vertical layer. Select 0 for exponential function, 1 for a homogenous layer and 2 for a cubic function.
> >
> > *input_dict['Layer4 relative humidity']* (int): Relative humidity value at the fourth vertical layer. Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> >*input_dict['Layer4 profile params']* (1D array of floats):  Parameters defining the thickness of fourth layer and distribution of aerosols in it. [Layer base height, Layer top height, Scale height] if *input_dict['Layer1 profile type']=0*. [Layer base height, Layer top height, 1] if *input_dict['Layer1 profile type']=1* and [Layer base height, Layer top height, a,b,c,d] if *input_dict['Layer1 profile type']=2* where a,b,c and d are the coefficients of cubic function ah<sup>3</sup>+bh<sup>2</sup>+ch+d.
> >
> > *input_dict['Layer4 component concentration']* (Dict of floats):  Dictionary of number concentration or mass concentration of aerosol components constituting the mixture in fourth layer. Set zero for non-constituting compoenents. The total number of components should be same as that of *input_dict['Maximum number of components']*. For the default dataset, the components 1 to 9 represents the number or mass concentrations of water-insoluble, water-soluble, black carbon, sea-salt accumulation mode, sea-salt coarse mode, mineral dust nucleation mode, mineral dust accumulation mode, mineral dust coarse mode and stratospheric sulfate aerosols. Component number 10 onwards can be used for user defined aerosol components.
> >
> >*input_dict['Layer5 profile type']* (int): Type of function to represent aerosol vertical profile in the fifth vertical layer. Select 0 for exponential function, 1 for a homogenous layer and 2 for a cubic function.
> >
> > *input_dict['Layer5 relative humidity']* (int): Relative humidity value at the fifth vertical layer. Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> >*input_dict['Layer5 profile params']* (1D array of floats):  Parameters defining the thickness of fifth layer and distribution of aerosols in it. [Layer base height, Layer top height, Scale height] if *input_dict['Layer1 profile type']=0*. [Layer base height, Layer top height, 1] if *input_dict['Layer1 profile type']=1* and [Layer base height, Layer top height, a,b,c,d] if *input_dict['Layer1 profile type']=2* where a,b,c and d are the coefficients of cubic function ah<sup>3</sup>+bh<sup>2</sup>+ch+d.
> >
> > *input_dict['Layer5 component concentration']* (Dict of floats):  Dictionary of number concentration or mass concentration of aerosol components constituting the mixture in fifth layer. Set zero for non-constituting compoenents. The total number of components should be same as that of *input_dict['Maximum number of components']*. For the default dataset, the components 1 to 9 represents the number or mass concentrations of water-insoluble, water-soluble, black carbon, sea-salt accumulation mode, sea-salt coarse mode, mineral dust nucleation mode, mineral dust accumulation mode, mineral dust coarse mode and stratospheric sulfate aerosols. Component number 10 onwards can be used for user defined aerosol components.
> >
> > *input_dict['Layer6 profile type']* (int): Type of function to represent aerosol vertical profile in the sixth vertical layer. Select 0 for exponential function, 1 for a homogenous layer and 2 for a cubic function.
> >
> > *input_dict['Layer6 relative humidity']* (int): Relative humidity value at the sixth vertical layer. Acceptable values are (*0,50,70,80,90,95,98,99*).
> >
> >*input_dict['Layer6 profile params']* (1D array of floats):  Parameters defining the thickness of sixth layer and distribution of aerosols in it. [Layer base height, Layer top height, Scale height] if *input_dict['Layer1 profile type']=0*. [Layer base height, Layer top height, 1] if *input_dict['Layer1 profile type']=1* and [Layer base height, Layer top height, a,b,c,d] if *input_dict['Layer1 profile type']=2* where a,b,c and d are the coefficients of cubic function ah<sup>3</sup>+bh<sup>2</sup>+ch+d.
> >
> > *input_dict['Layer6 component concentration']* (Dict of floats):  Dictionary of number concentration or mass concentration of aerosol components constituting the mixture in sixth layer. Set zero for non-constituting compoenents. The total number of components should be same as that of *input_dict['Maximum number of components']*. For the default dataset, the components 1 to 9 represents the number or mass concentrations of water-insoluble, water-soluble, black carbon, sea-salt accumulation mode, sea-salt coarse mode, mineral dust nucleation mode, mineral dust accumulation mode, mineral dust coarse mode and stratospheric sulfate aerosols. Component number 10 onwards can be used for user defined aerosol components.
>
> Returns:
>
> Dictionary of output parameters.
> > *output_dict['Relative humidity']*: Relative humidity used to calculate the results in the first vertical layer.
> > 
> > *output_dict['Number concentration (1/cm³)']*: Number concentration of aerosol components in the first vertical layer.
> > 
> > *output_dict['Mass concentration (ug/m³)']*: Mass concentration of aerosol components in the first vertical layer.
> > 
> > *output_dict['Volume concentration (um³/m³)']*: Volume concentration of aerosol components in the first vertical layer.
> > 
> > *output_dict['Number mixing ratio']*: Number mixing ratio of aerosol components in the first vertical layer.
> > 
> > *output_dict['Mass mixing ratio']*: Mass mixing ratio of aerosol components in the first vertical layer.
> > 
> > *output_dict['Volume mixing ratio']*: Volume mixing ratio of aerosol components in the first vertical layer.
> > 
> > *output_dict['Extinction coefficient (1/km)']*: Extinction cofficient at the first vertical layer.
> > 
> > *output_dict['Scattering coefficient (1/km)']*: Scattering cofficient at the first vertical layer.
> > 
> > *output_dict['Absorption coefficient (1/km)']*: Absorption cofficient at the first vertical layer.
> > 
> > *output_dict['SSA']*: Single scattering albedo at the first vertical layer.
> > 
> > *output_dict['g']*: Asymmetry parameter at the first vertical layer.
> > 
> > *output_dict['Total column AOD']*: Total column Aerosol optical depth.
> > 
> > For each layer *x*
> > 
> > *output_dict['Layerx']['Layer']*: Layer number
> > 
> > *output_dict['Layerx']['Relative humidity']*: Relative humidity used to calculate the results in the layer *x*.
> > 
> > *output_dict['Layerx']['Number concentration (1/cm³)']*: Number concentration of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Mass concentration (ug/m³)']*: Mass concentration of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Volume concentration (um³/m³)']*: Volume concentration of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Number mixing ratio']*: Number mixing ratio of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Mass mixing ratio']*: Mass mixing ratio of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Volume mixing ratio']*: Volume mixing ratio of aerosol components in the layer *x*.
> > 
> > *output_dict['Layerx']['Extinction coefficient (1/km)']*: Extinction cofficient at the layer *x*.
> > 
> > *output_dict['Layerx']['Absorption coefficient (1/km)']*: Absorption cofficient at the layer *x*.
> > 
> > *output_dict['Layerx']['SSA']*: Single scattering albedo at the layer *x*.
> > 
> > *output_dict['Layerx']['g']*: Asymmetry parameter at the layer *x*.
> > 
> > *output_dict['Layerx']['AOD']*: Aerosol optical depth of aerosols in the layer *x*.
## License

[GNU General Public License v3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html)
