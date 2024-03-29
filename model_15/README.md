# Model 15

Programable Eurorack module Remix of by Allen-Synthesis' [EuroPi](https://github.com/Allen-Synthesis/EuroPi).

<img src="./docs/front.jpg" width="480" >

## Description

This module is based on the schematics of the EuroPi, the slight differences:

- Added CV to the Knobs (analogue input)
- Access to un-used pins thru a header (for expansions)
- Jumper to change analog input from bipolar-unipolar* (Experimental! see TODOS)

This module is fully compatible with all Europi [scripts](https://github.com/Allen-Synthesis/EuroPi/tree/main/software/contrib) as long as the modified firmware is used `europi_m15.py`.


## TODOs:

- Better Diagnosis Script
- Change Calibration to acommodate bipolar and inverted Analog signal
- Add Bipolar support (change fw)

## Get your own

Under `hardwared` you can find the gerbers and BOM files. This gerber was done to be printed in one go, a v-cut is used to separate both pcnbs. Be careful about it when ordering. Exported files to `altium` are also included but _atention_ these were not verified (i dont have altium)

<img src="./docs/back.jpg" width="480" >

## Get Started

You can use the same setup as decribed in EuroPi's page ([here](https://github.com/Allen-Synthesis/EuroPi/blob/main/software/programming_instructions.md)). 

If you want to use `menu.py` script as `main.py`. Use `ampy` pip package to move files to the `contrib` folder

```
 C:\EuroPi-main\software> ampy  --port COM21 put contrib /lib/contrib
```
 
Other useful `ampy` commands can be found [here](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/file-operations)