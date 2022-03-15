# ml4bio
[![PyPI](https://img.shields.io/pypi/v/ml4bio.svg)](https://pypi.org/project/ml4bio/)
[![Test ml4bio](https://github.com/gitter-lab/ml4bio/workflows/Test%20ml4bio/badge.svg)](https://github.com/gitter-lab/ml4bio/actions?query=workflow%3A%22Test+ml4bio%22)

This package is a graphical interface wrapper for sklearn classification.
It is intended to be used with the [ML4Bio workshop](https://github.com/carpentries-incubator/ml4bio-workshop) training materials.

## Python environment

Requires:
- Python 3.5
- pandas
- numpy
- sklearn
- matplotlib
- pyqt 5
- scipy

See `conda_env.yml` for one set of compatible package versions.
Create the `ml4bio` [conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html) with the command `conda env create -f conda_env.yml`.
Activate the environment with `conda activate ml4bio`.

The full Anaconda installation also provides all required dependencies.

## Running

The ML4Bio workshop repository provides [scripts](https://github.com/carpentries-incubator/ml4bio-workshop/tree/gh-pages/scripts) for installing and launching the ml4bio GUI.
Once the ml4bio package and its dependencies have been installed, the GUI can be launched using the `ml4bio` command from the command line.

## Citation

[An approachable, flexible, and practical machine learning workshop for biologists](https://doi.org/10.1101/2022.02.03.479008).  
Chris S Magnano, Fangzhou Mu, Rosemary S Russ, Milica Cvetkovic, Debora Treu, Anthony Gitter.  
bioRxiv, 2022. doi:10.1101/2022.02.03.479008

## Third party materials
The icons in the `ml4bio/icons` directory were downloaded from http://thenounproject.com under the Creative Commons license.
Instructions on how to give credit to the creators: [link](https://thenounproject.zendesk.com/hc/en-us/articles/200509928-How-do-I-give-creators-credit-in-my-work-)

Add this attribution where appropriate:
> Created by sachin modgekar from Noun Project.
