arduino sketch works... as long as proper clock is provided to the ic
mosi spits out 15khz clock, but it's not enough for the ic to work


sketch needs to be modified to use 1mhz clock from arduino

reference: http://www.florentflament.com/blog/driving-ym2149f-sound-chip-with-an-arduino.html




# CLK

The YM2149 needs a 1Mhz clock (or 2 if SEL pin is used) to work properly. The arduino can provide that writing the right settings in the PWM register. A great explanation of it is available [here](https://docs.arduino.cc/tutorials/generic/secrets-of-arduino-pwm). And a direct example from [here](https://forum.arduino.cc/t/generate-high-frequency-square-wave/74253/7) explains how to get it in 4 lines. See function `set_ym_clock` in the sketch.