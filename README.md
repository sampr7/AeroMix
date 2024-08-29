# AeroMix
*by [Sam P Raj](https://github.com/sampr7/) and [P R Sinha](https://www.iist.ac.in/ess/prs)*  
*Department of Earth and Space Sciences*  
*[Indian Institute of Space Science and Technology, Thiruvananthapuram](https://www.iist.ac.in/), IN*  

[![Downloads](https://static.pepy.tech/badge/AeroMix)](https://pepy.tech/project/AeroMix)

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
See detailed documentation [here](https://github.com/sampr7/AeroMix/blob/main/Documentation.md).

## How to cite
If you use AeroMix in your research, please cite the following paper:

>Raj, S. P., Sinha, P. R., Srivastava, R., Bikkina, S., and Subrahamanyam, D. B.: AeroMix v1.0.1: a Python package for modeling aerosol optical properties and mixing states, Geosci. Model Dev., 17, 6379–6399, https://doi.org/10.5194/gmd-17-6379-2024, 2024.

## License

[GNU General Public License v3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Contact
We are continuously working to improve and enhance the capabilities of our package. Your feedback, suggestions, and reports of any bugs you encounter are incredibly valuable to us. We welcome you to join the discussion on our [GitHub page](https://github.com/sampr7/AeroMix)  or feel free to reach out directly via email. Please send your thoughts and reports to sampr7@gmail.com. 

