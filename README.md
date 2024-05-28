# Prisma QA

## Getting started

## Description
This project aims to develop and disseminate a robust, reproducible quality assurance (QA) protocol for all kinds of MR sequences used at UAB's Research MRI Core (RMRIC).

The notebook currently supports basic analyses of fBIRN phantom fMRI as described in Friedman and Glover (JMRI 23:827-839 2006 https://doi.org/10.1002/jmri.20583). The following images and metrics are calculated:
- Signal image
- Signal-to-fluctuation-noise ratio (SFNR) image
- Signal-to-noise ratio (SNR)
- SFNR summary value
- Percent fluctuation summary value
- Percent drift summary value
- Residual magnitude spectrum after time series detrending (used to identify periodic sources of noise, e.g. mechanical vibrations, gradient-induced resonances)
- Weiskoff plot
- Radius of decorrelation (RDC)

## Installation
To run the python scripts and jupyter notebook, you will need to have python installed. Conda (Anaconda or Miniconda) is also very helpful. The conda environment is specified in `environment.yml`.

Create a new conda environment to use with this project:
`conda env create -f environment.yml`

Activate the environment before running any scripts or opening any notebooks:
`conda activate mriqa`

## Usage
The processing scripts use the python module nibabel to read image arrays from files in NIFTI format. Images from the MRI scanner are in DICOM format. To convert DICOM datasets to BIDS compliant NIFTI format, use heudiconv:
`heudiconv -s YOUR_SUBJECT_NAME -ss YOUR_SESSION_NAME --files PATH_THAT_INCLUDES_ALL_YOUR_DICOM_FILES -o PATH_TO_YOUR_NIFTI_OUTPUT -f PATH_TO_YOUR_HEURISTIC_FILE -c dcm2niix -b --overwrite`
For QA analysis:
- YOUR_SUBJECT_NAME = fbirn
- YOUR_SESSION_NAME = Qa_MMDDYYY_CINL####, where MMDDYYYY is the date of the scan, and #### is the 4-digit CINL number


## Support
If you need help with any of the scripts in this project, please contact us at cinl@uab.edu.

## Roadmap
QA protocols in development
- [ ] RF noise: to track changes in the radiofrequency environment of the MRI suits
- [ ] DWI: using a quantitative DTI phantom
- [ ] MRS: using quantitative MRS phantoms containing relevant metabolites (brain, liver, etc)
- [ ] Coil specific protocols
- [ ] Ghost-to-noise ratio: track changes in Nyquist ghosts due to gradient inhomogeneities, eddy currents, shim quality, and other sources.

## Contributing


## Authors and acknowledgment


## License


## Project status
