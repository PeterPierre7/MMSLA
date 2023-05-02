
# MutiMSLA

This repository had been created to store the code base for the Mutli MSLA projet. In this README, you will find a desciption of the various script and how to run them.

## Author

- [Pierre Wadoux](https://github.com/PeterPierre7)


## Get the repository

Clone the project

```bash
  git clone https://github.com/PeterPierre7/MMSLA
```

Go to the project directory

```bash
  cd MMSLA
```



## Installation

To use thoses script you can use [PDM](https://github.com/pdm-project/pdm/blob/main/README.md) to quickly setup the environement :
```bash
  pdm install
```

## Use the scripts

This repo have multiple scripts that can help with different MMSLA tasks. 

### Serial connection :
```bash
  pdm run scripts/simple_serial.py
```
This script allow for a simple back and forth with the Elegoo Saturn S. When run, you can write gcode in the shell. The message recived by the printer will be display on the same shell. This lead to a confusing display if not use quickly.


### JSON file 
```bash
  pdm run scripts/file_example.py
```
This script is use to produce and verify a JSON file use to configure the MMSLA print. This file is simply structured with two file parameter and one list for parameter : 
```bash
"layer_height": (layer_height in mm) ,  
"ctb_file" : (your file.ctb),
"resine_changes": [ list of disctonary
 {
 "layer": (next cut off layer),  
 "resine": (resine name for display),
 "exposure_time": (in ms)
 }, ...]
 
 ```


### Main print file
```bash
  pdm run scripts/print_mmsla.py
```

This script is used to print the a MMSLA file. The necessary informations are supposed to be indicated in the JSON file created previously.