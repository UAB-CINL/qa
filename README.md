# Prisma QA

## Getting started

## Description
This project aims to develop and disseminate a robust, reproducible quality assurance (QA) protocol for all kinds of MR sequences used at UAB's Research MRI Core (RMRIC).

## Installation
To run the python scripts and jupyter notebook, you will need to have python installed. Conda (Anaconda or Miniconda) is also very helpful. The conda environment is specified in `environment.yml`.

Create a new conda environment to use with this project:
`conda env create -f environment.yml`

Activate the environment before running any scripts or opening any notebooks:
`conda activate prismaqa`

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

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
