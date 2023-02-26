arduino sketch works... as long as proper clock is provided to the ic
mosi spits out 15khz clock, but it's not enough for the ic to work


sketch needs to be modified to use 1mhz clock from arduino

reference: http://www.florentflament.com/blog/driving-ym2149f-sound-chip-with-an-arduino.html
k