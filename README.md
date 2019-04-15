# Four ways to fit an ion current model

This repository contains all data, code, figures, and animations for the paper "Four ways to fit an ion current model", by Clerx, Beattie, Gavaghan, and Mirams.

## Supporting materials

* [Animations of protocols](./animations)
* [Figures, and figure generating code](./figures)
  * [Data for all cells](./figures/f1-protocols)
  * [Method 1 cross-validation for all cells](./figures/f4-cross-validation-1)
  * [Method 2 cross-validation for all cells](./figures/f5-cross-validation-2)
  * [Method 3 cross-validation for all cells](./figures/f6-cross-validation-3)
  * [Method 4 cross-validation for all cells](./figures/f7-cross-validation-4)
  * [AP Validation for all cells](./figures/f8-validation-ap)
* [Supplementary figures](./figures-supp)
* [Unused figures](./figures-unused)
  
## Code

The code requires Python (either 2.7 or 3.3+) and two dependencies: PINTS and Myokit.
Myokit can be installed using `pip install myokit` (or `pip3 install myokit` for some python 3 environments), or following the instructions on http://myokit.org.
PINTS can be installed using the instructions on https://github.com/pints-team/pints.
[Matplotlib](https://pypi.org/project/matplotlib/) is required to regenerate the figures, and one of the supplementary figures also requires [Seaborn](https://pypi.org/project/seaborn/).

Organisation:

* `data`: all experimental data
* `method-1`: scripts to run method 1
* `method-2`: scripts to run method 2
* `method-3`: scripts to run method 3
* `method-4`: scripts to run method 4
* `models-and-protocols`: the Myokit models and protocols used in the study
* `python`: shared Python scripts, the most important bits of code live here
* `surface`: scripts to perform surface mapping
* `surface-ap-fit`: scripts to fit to the validation signal, only ever used for surface mapping
* `validation`: scripts that post-process results from methods 1-4 and assess their performance

## Data source

This project uses the sine wave data from Beattie 2018, see: https://github.com/mirams/sine-wave

For the publication, see: https://physoc.onlinelibrary.wiley.com/doi/full/10.1113/JP275733

Beattie, K. A., Hill, A. P., Bardenet, R., Cui, Y., Vandenberg, J. I., Gavaghan, D. J., de Boer, T. P. & Mirams, G. R. Sinusoidal voltage protocols for rapid characterisation of ion channel kinetics. J. Physiol. 596, 1813–1828 (2018).


