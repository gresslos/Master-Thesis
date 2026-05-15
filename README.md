# Master's Thesis

This repository contains scripts, data files, and plots used for my Master's thesis on atmospheric radiative transfer using EarthCARE data.

## Project description

The thesis evaluates 1D and 3D atmospheric radiative transfer simulations using EarthCARE atmospheric profiles and satellite observations of top-of-atmosphere fluxes.

The work includes simulations with the 3D radiative transfer model MYSTIC and the 1D radiative transfer model DISORT. The results are used to assess radiative closure and the importance of atmospheric input data, model parameter choices, and 3D radiation transport.

## Repository structure

- `MakeRTM.py` - creates and runs radiative transfer model input files.
- `ReadEC.py` - reads, processes, and plots EarthCARE data and simulation results.
- `UVspec.py` - libRadtran/uvspec simulation setup.
- `plot_data.py` - creates additional analysis plots.
- `plot_target_classification.py` - plot target classification from the EarthCARE AC-TC product.
- `regression.py` - performs and plots linear regression.
- `run.sh` - shell script for running the libRadtran radiative transfer simulations.
- `Master_Plots/` - contains plots used in the thesis.
- `Surface_Analysis/` - contains files and plots related to the surface analysis found on the Master's Thesis.
- `Master_UiO_Benjamin_Gressløs.pdf` - PDF of the Master's Thesis.

## Requirements

The scripts require Python and several Python packages:

- `numpy`
- `scipy`
- `matplotlib`
- `cartopy`
- `h5py`
- `netCDF4`
- `mpi4py`
- `dted`

Additional software used in the thesis includes libRadtran (https://www.libradtran.org/doku.php?id=start), a radiative transfer software package that includes the two radiative transfer models used: MYSTIC and DISORT.

To run simulation jobs, the following requirements must be met:

1. libRadtran must be downloaded and installed.
2. The folders `output`, `tmpRTIO`, and `RESULTS` must exist in the same folder as `MakeRTM.py`. These folders are used to store temporary files and result files.


