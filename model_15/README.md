# Model 15

Programable Eurorack module Remix of by Allen-Synthesis' [EuroPi](https://github.com/Allen-Synthesis/EuroPi).

<img src="./docs/front.jpg" width="480" >

## Description

This module is based on the schematics of the EuroPi, the slight differences:

- Added CV to the Knobs.
- Access to un-used pins thru a header for expansions.
- Solder Jumper to change analog input from bipolar-unipolar* (Experimental! see TODOS)

In order for the m15 to work with Europi's [scripts](https://github.com/Allen-Synthesis/EuroPi/tree/main/software/contrib), custom Firmware `europi_m15.py` needs to be used. This is because following changes were made:

- I2C1 is used for OLED, I2C0 is send to Expansion Header.
- Knobs pins are inverted. 
- Analog input is inverted so it can be used with bipolar signals. Therefore the calibration needs to be inverted as well




## TODOs:

- Better Diagnosis Script
- Change Calibration to acommodate bipolar and inverted Analog signal
- Add Bipolar support (change fw)

## Get your own

Under `hardwared` you can find the gerbers and BOM files. This gerber was done to be printed in one go, a v-cut is used to separate both pcnbs. Be careful about it when ordering. Exported files to `altium` are also included but _atention_ these were not verified (i dont have altium)

<img src="./docs/back.jpg" width="480" >

## Get Started

These instructions have been tested for Europi package __version__ = "0.7.1"

- Recommended to use Adafruit's  [flash_nuke.uf2](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython#flash-resetting-uf2-3083182) to clean your pico. 
- Install the latest [micropython](https://micropython.org/download/rp2-pico/) for the Raspberry Pi Pico.
- Using [Thonny](https://thonny.org/) install `micropython-ssd1306`, `micropython-europi` and `micropython-europi-contrib` packages.
- Copy the contents of `europi_m15.py` and paste in the `lib\europi.py` file.
- Copy the contents of `calibrate_m15.py` and paste in the `lib\calibrate.py` file.
- Create a `main.py` file and copy/paste the contents of `menu.py` in the `contrib` folder.



For new scripts Use `ampy` pip package to move files to the `contrib` folder
```
 C:\EuroPi-main\software> ampy  --port COM21 put contrib /lib/contrib
```
 
Other useful `ampy` commands can be found [here](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/file-operations)