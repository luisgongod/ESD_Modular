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
        self.links = [False, False, False, False, False, False]
        self.outputs = [0, 0, 0, 0, 0, 0]
        self.selected_pair = 0 # up to 5 pairs (6 outputs)
        

        din.handler(self.beat) #external clock in signal
        b1.handler(self.change_link) 
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

    def beat(clocks,links):
        """Called when the clock input is triggered"""    
        #TODO:  use better var names
        clk_iter = iter(clocks)
        links_iter = iter(links)

        out = []
    
        for c in clk_iter:        
            try:
                l=next(links_iter)                
            except StopIteration:
                break

            if c.clock():
                out.append(1)
                if(l):
                    out.extend(beat(clk_iter,links_iter))
            else:
                out.append(0)
                while l:
                    try:
                        l=next(links_iter)
                        next(clk_iter)
                    except StopIteration:
                        break
                    out.append(0)

        return out

    def change_link(self):
        """Toggles the link"""
        self.modes[self.selected_lfo] = (self.modes[self.selected_lfo] + 1) % self.MODE_COUNT
        self.save_state()

    def increment_selection(self):
        """Move the selection to the next Link"""
        self.selected_pair = (self.selected_pair + 1) % 5

        
    
    def main(self):
        while True:
            self.read_knobs()




            #read the knob positions 



if __name__ == "__main__":
    ChronoTrigger().main()
