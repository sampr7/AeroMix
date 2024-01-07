# AeroMix

Python package for modeling aerosol optical properties

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
Detailed documentation is coming soon

## License

[GNU General Public License v3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html)
