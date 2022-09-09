from europi_m import *
from math import cos, radians
from time import sleep_ms
from machine import freq
from random import randint
from europi_script import EuroPiScript

MAX_VOLTAGE = MAX_OUTPUT_VOLTAGE #Default is inherited but this can be overriden by replacing "MAX_OUTPUT_VOLTAGE" with an integer
MAX_HARMONIC = 32 #Too high a value may be hard to select using the knob, but the actual hardware limit is only reached at 4096

class HarmonicLFOs(EuroPiScript):
    def __init__(self):
        super().__init__()
        
        #Retreive saved state information from file
        state = self.load_state_json()
        
        #Overclock the Pico for improved performance
        freq(250_000_000)
        
        #Use the saved values for the LFO divisions and mode if found in the save state file, using defaults if not
        # self.divisions = state.get("divisions", [1, 3, 5, 7, 11, 13])
        self.divisions = state.get("divisions", [1, 2, 4, 8, 16, 32])
        self.DIVSISION_CHOICES = [1, 2, 4, 8, 16, 32]
        self.modes = state.get("modes", [0, 0, 0, 0, 0, 0])
        self.MODE_COUNT = 5
        
        #Initialise all the other variables
        self.degree = 0
        self.delay, self.increment_value = self.get_delay_increment_value()
        self.pixel_x = OLED_WIDTH-1
        self.pixel_y = int(OLED_HEIGHT/2)-1
        self.selected_lfo = 0
        self.selected_lfo_start_value = self.get_clock_division()
        
        #Set the digital input and button handlers
        din.handler(self.reset)
        b1.handler(self.change_mode)
        b2.handler(self.increment_selection)

    def get_clock_division(self):
        """Determine the new clock division based on the position of knob 2"""       

        # return k2.read_position(MAX_HARMONIC) + 1
        return k2.choice([1, 2, 4, 8, 16, 32])

    def reset(self):
        """Reset all LFOs to zero volts, maintaining their divisions"""
        self.degree = 0

    def change_mode(self):
        """Change the mode that controls wave shape"""
        self.modes[self.selected_lfo] = (self.modes[self.selected_lfo] + 1) % self.MODE_COUNT
        self.save_state()

    def get_delay_increment_value(self):
        """Calculate the wait time between degrees"""
        # delay = (0.1 - (k1.read_position(100, 1)/1000)) + (ain.read_voltage(1)/100)
        delay = (0.1 - (k1.read_position(100, 1)/1000)) 
        return delay, round((((1/delay)-10)/1)+1)

    def increment_selection(self):
        """Move the selection to the next LFO"""
        self.selected_lfo = (self.selected_lfo + 1) % 6
        self.selected_lfo_start_value = self.get_clock_division()

    def save_state(self):
        """Save the current set of divisions to file"""
        if self.last_saved() < 5000:
            return
        
        state = {
            "divisions": self.divisions,
            "modes": self.modes
        }
        self.save_state_json(state)
        
    def update_display(self):
        """Update the OLED display every 10 cycles (degrees)"""
        oled.scroll(-1,0)
        if round(self.degree, -1) % 10 == 0:
            oled.show()
            
    def increment(self):
        """Increment the current degree and determine new values of delay and increment_value"""
        self.degree += self.increment_value
        self.delay, self.increment_value = self.get_delay_increment_value()
        sleep_ms(int(self.delay))
        
    def draw_wave(self,lfo=0):
        shape = self.modes[lfo]
        position = lfo*21
        if shape == 0: #Sine
            oled.pixel(position + 3,31,1)
            oled.pixel(position + 3,30,1)
            oled.pixel(position + 3,29,1)
            oled.pixel(position + 4,28,1)
            oled.pixel(position + 4,27,1)
            oled.pixel(position + 4,26,1)
            oled.pixel(position + 4,25,1)
            oled.pixel(position + 5,24,1)
            oled.pixel(position + 6,23,1)
            oled.pixel(position + 7,23,1)
            oled.pixel(position + 8,24,1)
            oled.pixel(position + 9,25,1)
            oled.pixel(position + 9,26,1)
            oled.pixel(position + 9,27,1)
            oled.pixel(position + 10,28,1)
            oled.pixel(position + 10,29,1)
            oled.pixel(position + 11,30,1)
            oled.pixel(position + 12,31,1)
            oled.pixel(position + 13,31,1)
            oled.pixel(position + 14,30,1)
            oled.pixel(position + 15,29,1)
            oled.pixel(position + 15,28,1)
            oled.pixel(position + 15,27,1)
            oled.pixel(position + 15,26,1)
            oled.pixel(position + 16,25,1)
            oled.pixel(position + 16,24,1)
            oled.pixel(position + 16,23,1)
        elif shape == 1: #Saw
            oled.line( position + 3 ,31 ,position + 9,24,1)
            oled.vline(position + 9 ,24 ,8,1)
            oled.line( position + 9 ,31 ,position + 15,24,1)
            oled.vline(position + 15,24 ,8,1)
        elif shape == 2: #Square
            oled.vline(position + 3,24,8,1)
            oled.hline(position + 3,24,6,1)
            oled.vline(position + 9,24,8,1)
            oled.hline(position + 9,31,6,1)
            oled.vline(position + 15,24,8,1)
        elif shape == 3: #Ramp
            oled.vline(position + 3,24 ,8,1)
            oled.line( position + 3 ,24 ,position + 9,31,1)
            oled.vline(position + 9 ,24 ,8,1)
            oled.line( position + 9 ,24 ,position + 15,31,1)
        elif shape == 4: #Random(ish)
            oled.pixel(position + 3,29,1)
            oled.pixel(position + 4,28,1)
            oled.pixel(position + 4,27,1)
            oled.pixel(position + 5,26,1)
            oled.pixel(position + 6,26,1)
            oled.pixel(position + 7,27,1)
            oled.pixel(position + 8,28,1)
            oled.pixel(position + 9,28,1)
            oled.pixel(position + 10,27,1)
            oled.pixel(position + 10,26,1)
            oled.pixel(position + 10,25,1)
            oled.pixel(position + 11,24,1)
            oled.pixel(position + 12,25,1)
            oled.pixel(position + 13,26,1)
            oled.pixel(position + 13,27,1)
            oled.pixel(position + 14,28,1)
            oled.pixel(position + 14,29,1)
            oled.pixel(position + 15,30,1)
            oled.pixel(position + 16,30,1)        
        
    def display_selected_lfo(self,lfo=0):
        """Draw the current LFO's number and division to the OLED display"""

        oled.fill_rect(21*lfo,0,20,32,0)
        if lfo == self.selected_lfo:
            oled.rect(21*lfo,0,20,32,1)

        # oled.fill_rect(21*lfo,0,20,9,1)
        
        oled.text(str(lfo+1),6+21*lfo,1,1)        
        # number = self.divisions[self.selected_lfo]
        number = self.divisions[lfo]
        x = 2 if number >= 10 else 6
        oled.text(str(number),x+21*lfo,12,1)
        
        self.draw_wave(lfo)
        
    def round_nearest(self, x, a):
        return round(x / a) * a
        
    def calculate_voltage(self, cv, multiplier):
        """Determine the voltage based on current degree, wave shape, and MAX_VOLTAGE"""
        three_sixty = 360*multiplier
        degree_three_sixty = self.degree % three_sixty
        lfo_mode = self.modes[cvs.index(cv)]
        if lfo_mode == 0: #Sin
            voltage = ((0-(cos(self.rad*(1/multiplier)))+1)) * (MAX_VOLTAGE/2)
        elif lfo_mode == 1: #Saw
            voltage = (degree_three_sixty / (three_sixty)) * MAX_VOLTAGE
        elif lfo_mode == 2: #Square
            voltage = MAX_VOLTAGE * (int((degree_three_sixty / (three_sixty)) * MAX_VOLTAGE) < (MAX_VOLTAGE/2))
        elif lfo_mode == 3: #Off
            voltage = MAX_VOLTAGE -((degree_three_sixty / (three_sixty)) * MAX_VOLTAGE)
        elif lfo_mode == 4: #Random(ish). This is NOT actually random, it is the sum of 3 out of sync sine waves, but it produces a flucutating voltage that is near impossible to predict over time, and which can be clocked to be in time
            voltage = ((((0-(cos(self.rad*(1/multiplier)))+1)) * (MAX_VOLTAGE/2)) / 3) + ((((0-(cos(self.rad*(1/(multiplier*2.3))))+1)) * (MAX_VOLTAGE/2)) / 3) + ((((0-(cos(self.rad*(1/(multiplier*5.6))))+1)) * (MAX_VOLTAGE/2)) / 3)
        return voltage
        
    def display_graphic_lines(self):
        """Draw the lines displaying each LFO's voltage to the OLED display"""
        self.rad = radians(self.degree)
        oled.vline(self.pixel_x,0,OLED_HEIGHT,0)
        for cv, multiplier in zip(cvs, self.divisions):
            volts = self.calculate_voltage(cv, multiplier)
            cv.voltage(volts)
            oled.pixel(self.pixel_x,self.pixel_y+self.pixel_y-int(volts*(self.pixel_y/10)),1)

    def check_change_clock_division(self):
        """Change current LFO's division with knob movement detection"""
        self.clock_division = self.get_clock_division()

        self.divisions[0] = 1
        self.divisions[1] = mks[0].read_position(MAX_HARMONIC)+1
        self.divisions[2] = mks[1].read_position(MAX_HARMONIC)+1
        self.divisions[3] = mks[2].read_position(MAX_HARMONIC)+1
        self.divisions[4] = mks[3].read_position(MAX_HARMONIC)+1
        self.divisions[5] = k2.read_position(MAX_HARMONIC)+1


        # if self.clock_division != self.selected_lfo_start_value:
            # self.selected_lfo_start_value = self.clock_division 
            # self.divisions[self.selected_lfo] = self.clock_division
            # self.save_state()
        

    def main(self):
        while True:
            self.check_change_clock_division()
            
            self.display_graphic_lines()
            
            for lfo_num in range(6):
                self.display_selected_lfo(lfo_num)
            
            self.update_display()
            
            self.increment()


if __name__ == "__main__":
    HarmonicLFOs().main()
