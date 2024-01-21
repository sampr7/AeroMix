# AeroMix
*by [Sam P Raj](https://github.com/sampr7/) and [P R Sinha](https://www.iist.ac.in/ess/prs)*  
*Department of Earth and Space Sciences*  
*[Indian Institute of Space Science and Technology, Thiruvananthapuram](https://www.iist.ac.in/), IN*  

AeroMix is a versatile open-source aerosol optical model framework designed for computing a wide range of optical and physical properties of complex aerosol mixtures.

## Installation

Use the package manager [pip](https://pypi.org/) to install AeroMix.

```bash
pip install AeroMix
```

## Usage

```python
import AeroMix

# get a sample input dictionary
input_dict = AeroMix.getAerosolType('urban',[0.4,0.5,0.6,0.7,0.8],80]

# run the AeroMix model
AeroMix.run(input_dict)

```

## Documentation
See detailed documentation [here](Documentation.md)

## License

[GNU General Public License v3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Contact
We are continuously working to improve and enhance the capabilities of our package. Your feedback, suggestions, and reports of any bugs you encounter are incredibly valuable to us. We welcome you to join the discussion on our [GitHub page](https://github.com/sampr7/AeroMix)  or feel free to reach out directly via email. Please send your thoughts and reports to sampr7@gmail.com. 
