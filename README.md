# fsri-residential-gasburner-2016
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.5703080.svg)](https://zenodo.org/record/5703080#.YZKBYr3MK50)


This repository contains the data and supporting files from natural gas burner experiments conducted in both single-story and two-story residential structures. This work was part of a larger series of experiments that studied the impact of ventilation on fire patterns. Data from those experiments can be explored here: [Impact of Fixed Ventilation on Fire Damage Patterns](https://fireinvestigation.fsri.org/)

This project was supported by Award No. 2015-DN-BX-K052, awarded by the National Institute of Justice, Office of Justice Programs, U.S. Department of Justice. The opinions, findings, and conclusions or recommendations expressed in this publication/program/exhibition are those of the author(s) and do not necessarily reflect those of the Department of Justice.

## 01_Data
The data directory is broken into two subdirectories: one for the single-story experiments (5 experiments) and one for the two-story experiments (8 experiments). More information on the structure of the included files and the corresponding experiments can be found here: [Data Details](01_Data/README.md) 

## 02_Info
The info directory contains a plaintext __.csv__ channel list and info file for each structure. The channel list maps the individual channels to their respective measurement arrays. Dimensioned, instrumented floor plans can be found here: [Instrumentation Details](02_Info/README.md). The channel list file also sets the channel labels and file names for graphs produced by the included scripts (03_Scripts). The info file is used to set the start and end times for graphs as well as the y-axis values for the respective measurement quantities.

## 03_Scripts
Python scripts are included to produce **.pdf** graphs for each of the measurement locations for each experiment. In conjunction with Matplotlib, Seaborn is used to style the graph. If seaborn is not already installed, it can be added by the following:
```
pip install seaborn
```
If you are using the Anaconda distribution of python, it can alternatively be installed by:
```
conda install seaborn
```

## 04_Charts
The chart directories gets produced upon execution of __Single_Story_Plot.py__ and __Two_Story_Plot.py__. Graphs are produced for each measurement location for each experiment. Because the graphs can be produced from files included in this repository, the graphs themselves are not files under version control. Additionally, the **04_Charts** directory is included in the __.gitignore__ file to prevent accidental commits of the graphs.

###
For more information about the project, [Contact Us](https://fsri.org/contact-fire-safety-research-institute).
