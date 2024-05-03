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

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
