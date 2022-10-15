from secrets import choice
from europi_m14 import *
from math import cos, radians
from time import sleep_ms
from machine import freq
from random import randint
from europi_script import EuroPiScript

MAX_VOLTAGE = MAX_OUTPUT_VOLTAGE #Default is inherited but this can be overriden by replacing "MAX_OUTPUT_VOLTAGE" with an integer
MAX_HARMONIC = 32 #Too high a value may be hard to select using the knob, but the actual hardware limit is only reached at 4096


class Clock:
    def __init__(self, divisions = 1):
        self.counter = 0
        self.divisions = divisions
        self.delay = 0
        self.DIV_CHOICES = [1, 2, 4, 8, 16, 32]

    def clock(self):
        self.counter += 1
        if self.counter == self.divisions:
            self.counter = 0
            return True
        else:
            return False
             
    def reset(self):
        self.counter = 0


class ChronoTrigger(EuroPiScript):
    
    def __init__(self):
        super().__init__()
        self.clocks = []
        self.clocks.append(Clock(1))
        self.clocks.append(Clock(2))
        self.clocks.append(Clock(4))
        self.clocks.append(Clock(8))
        self.clocks.append(Clock(16))
        self.clocks.append(Clock(32))
        self.links = [False, False, False, False, False]
        self.outputs = [0, 0, 0, 0, 0, 0]
        

        din.handler(self.beat)
        b1.handler(self.change_mode)
        b2.handler(self.increment_selection)

    def reset(self):
        """Reset all clocks to zero"""
        for clock in self.clocks:
            clock.reset()
    
    def read_knobs(self):
        """Read the knob positions and return a list of values"""

        #k1 and k2  
        self.clocks[0] = k1.choice(self.clocks[0].DIV_CHOICES)
        self.clocks[5] = k2.choice(self.clocks[5].DIV_CHOICES)

        #CV clocks
        self.clocks[1] = mka1.choice(self.clocks[1].DIV_CHOICES)
        self.clocks[2] = mka2.choice(self.clocks[2].DIV_CHOICES)
        self.clocks[3] = mka3.choice(self.clocks[3].DIV_CHOICES)
        self.clocks[4] = mka4.choice(self.clocks[4].DIV_CHOICES)

    def beat(self):
        """Called when the clock input is triggered"""
        
        i_out = 0
        clk_iter = iter(self.clocks)
        for clock in clk_iter: 
            if clock.clock():
                self.outputs[i_out] = 1
            else:
                self.outputs[i_out] = 0
            i_out += 1


        


        
        

    def main(self):
        while True:
            self.read_knobs()




            #read the knob positions 



if __name__ == "__main__":
    ChronoTrigger().main()
