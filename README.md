# relative_dose_1d

Python package to read an 1-dimensional dose profile from text file and perform subtraction and gamma index comparison.

![image_gui](/docs/assets/GUI_v011.PNG)

## Format specifications
The data should be in M ​​rows by 2 columns, corresponding to positions and
dose values, respectively.

The package has been tested with the following examples:

* File in w2CAD format (format used by the TPS Eclipse 16.1, from the Varian(R) company).
  In the algorithm, the start of the data is identified by the words: 'STOM' or 'STOD'
  Physical unit assumed to be in mm.

* File in mcc format (format used by Verisoft 7.1.0.199 software, from PTW(R) company).
  In the algorithm, the beginning of the data is identified by the word: 'BEGIN_DATA'
  Physical unit assumed to be in mm.

* File in text format
  The data must be distributed in M ​​rows by 2 columns and separated
  for a blank space.
  The script ask for a word to identify the beginning of the data in the text file, 
  a number to add to the positions, and a factor for distance dimension conversion.

## Installation
**Linux**<br/>
The easiest method of installation is by typing in a terminal:
```bash
pip install relative_dose_1d
```
**Windows**<br/>

Prior to installation, it is necessary to have a python package manager. If you are not familiar with Python packages, it is recommended to use [ANACONDA](https://www.anaconda.com/products/individual).
After ANACONDA has been installed, open *Anaconda Prompt*. Once inside the terminal (window with a black background), follow the indication described for Linux (previous paragraph).

## Usage

Once the installation is complete, open a terminal (or Anaconda Prompt in the case of Windows) and type the command **python**:

```bash
python
```
Finally, write:

```python
import relative_dose_1d.GUI
```

## Versions
April-2023  Versión 0.0.3
  * *relative_dose_1d* is added to [PyPi](https://pypi.org/)

May-2023 Version 0.1.0
  * It is now possible to perform unit transformation for distance using a multiplication factor, and move the origin of the coordinate system.

May-2023 Version 0.1.2
  * New web page for documentation, following [PEP 287 – reStructuredText Docstring Format](https://peps.python.org/pep-0287/).
