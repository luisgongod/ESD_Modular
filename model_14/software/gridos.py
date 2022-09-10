from europi_m14 import *
import machine
from time import ticks_diff, ticks_ms
from random import randint, uniform
from europi_script import EuroPiScript
from bjorklund import bjorklund as eucledian_rhythm

'''
GriDos
author: Luis G (github.com/luisgongod)
labels: sequencer, triggers, drums, randomness

A gate sequencer that builds on Nik Ansell's Consequencer. 

Inspired by Grids from mutable instruments. 
Can control up 6 instruments, adding sequences for each channel
Perfect to use with something like the Weston Audio AD110

CONTROLS:
knob_1: Randomness
knob_2: Fill, based on euclediaan rhythms

digital_in: clock in
analog_in: CV for Randomness, Fill or Pattern

button_1: 
- Short Press  (<300ms)  : Previous Drum pattern
- Medium Press (>300ms)  : Cycles through clock divisors (1/1, 1/2, 1/4)
- Long Press  (>2000ms)  : ??? TBD

button_2:
- Short Press  (<300ms)  : Next Drum pattern
- Medium Press (>300ms)  : Cycles what AIN can CV, (randomness -> fill -> Pattern -> randomness)
- Long Press   (>2000ms) : Toggle option for Random/Fill behaviour mode, 
    &: Randomness will change if a fill-step will be trigger
    |: Randomness will change in a fill-step if Patterns are triggered

output_1: trigger 1 / Bass Drum
output_2: trigger 2 / Snare Drum
output_3: trigger 3 / Hi-Hat
output_4: trigger 4 / Closed-Hat 
output_5: trigger 5 / Cymmbal
output_6: trigger 6 / Clap

'''

class Consequencer(EuroPiScript):
    def __init__(self):
        # Overclock the Pico for improved performance.
        machine.freq(250_000_000)

        # Initialize sequencer pattern arrays   
        p = pattern()     
        self.BD=p.BD
        self.SN=p.SN
        self.HH=p.HH
        self.OH=p.OH
        self.CY=p.CY
        self.CL=p.CL

        self.AIN_MODE = ['Random', 'Fill', 'Pattern']
        self.CLOCK_DIVISORS = [1, 2, 4]        

        # Initialize variables
        self.step = 0
        self.trigger_duration_ms = 50
        self.clock_step = 0
        self.clock_divisor = 0
        self.base_pattern = 0
        self.extra_pattern = 0
        self.pattern = 0
        self.random_HH = False
        self.minAnalogInputVoltage = 0.9 # Minimum voltage for analog input to be considered
        self.randomness = 0
        self.analogInputMode = 1 # initial mode 0: Randomness, 1: Fill, 2: Pattern 
        self.rand_fill_mode = 0 #  0: Random && Fill, 1: Random >> Fill
        self.CvPattern = 0
        self.reset_timeout = 500
        
        self.step_length = len(self.BD[self.pattern])

        self.fill = []
        
        # Calculate the longest pattern length to be used when generating random sequences
        self.maxStepLength = len(max(self.BD, key=len))
      

        # Triggered when button 2 is released.
        # - Short Press  (<300ms)  : Next Drum pattern
        # - Medium Press (>300ms)  : Cycles what AIN can CV, (randomness -> fill -> Pattern -> randomness)
        # - Long Press   (>2000ms) : Toggle option for Random/Fill behaviour mode, 
        @b2.handler_falling
        def b2Pressed():
            #Toggle Random/Fill mode
            # if more modes are added, this will need to be updated
            #     &: Random applies only to Filled steps
            #     |: Random applies to all steps if > 0
            if ticks_diff(ticks_ms(), b2.last_pressed()) >  2000:
                self.rand_fill_mode = not(self.rand_fill_mode)
            
            # AIN CV mode
            elif ticks_diff(ticks_ms(), b2.last_pressed()) >  300:
                self.analogInputMode = self.analogInputMode + 1
                if self.analogInputMode >= len(self.AIN_MODE):
                    self.analogInputMode = 0
            
            #next drum pattern
            else:
                self.base_pattern = (self.base_pattern + 1)%len(self.BD)
                self.pattern = (self.base_pattern + self.extra_pattern)%len(self.BD)
                self.step_length = len(self.BD[self.pattern])
            
        # - Short Press  (<300ms)  : Previous Drum pattern
        # - Medium Press (>300ms)  : Cycles through clock divisors (1/1, 1/2, 1/4)
        # - Long Press   (>2000ms) : ???
        @b1.handler_falling
        def b1Pressed():
            if ticks_diff(ticks_ms(), b1.last_pressed()) >  2000:
                pass
            
            # clock divisor
            elif ticks_diff(ticks_ms(), b1.last_pressed()) >  300:
                self.clock_divisor = (self.clock_divisor + 1) % len(self.CLOCK_DIVISORS)
            
            #prev drum pattern
            else:                
                self.base_pattern = (self.base_pattern - 1)%len(self.BD)
                self.pattern = (self.base_pattern + self.extra_pattern)%len(self.BD)
                self.step_length = len(self.BD[self.pattern])

        # Triggered on each clock into digital input. Output triggers.
        @din.handler
        def clockTrigger():

            # function timing code. Leave in and activate as needed
            #t = time.ticks_us()
            
            self.step_length = len(self.BD[self.pattern])
            
            # A pattern was selected which is shorter than the current step. Set to zero to avoid an error
            if self.step >= self.step_length:
                self.step = 0



            if self.rand_fill_mode == 0:            
            # Randomness will change if a full step will be trigger
            # Filled Steps will have a probability of triggering based on the randomness value from 50 to 100%
            # Non-filled steps will have a probability of triggering based on the randomness value from 50 to 0%
            # At randomness == 0, Filled-steps will always trigger, and non-filled steps will never trigge (if there is a pattern)   
            # at randomness == 25, Filled-pattern will have a 75% chance of triggering, Non-filled will have a 25%
            # at randomness == 50, trigger will happen at 50% of any Pattern
                if self.fill[self.step] == 1:
                    cv1.value(int(self.BD[self.pattern][self.step])*int(randint(0,99)>self.randomness))
                    cv2.value(int(self.SN[self.pattern][self.step])*int(randint(0,99)>self.randomness))
                    cv3.value(int(self.HH[self.pattern][self.step])*int(randint(0,99)>self.randomness))
                    cv4.value(int(self.OH[self.pattern][self.step])*int(randint(0,99)>self.randomness))
                    cv5.value(int(self.CY[self.pattern][self.step])*int(randint(0,99)>self.randomness))
                    cv6.value(int(self.CL[self.pattern][self.step])*int(randint(0,99)>self.randomness))
                else:
                    cv1.value(int(self.BD[self.pattern][self.step])*int(randint(0,99)<self.randomness))
                    cv2.value(int(self.SN[self.pattern][self.step])*int(randint(0,99)<self.randomness))
                    cv3.value(int(self.HH[self.pattern][self.step])*int(randint(0,99)<self.randomness))
                    cv4.value(int(self.OH[self.pattern][self.step])*int(randint(0,99)<self.randomness))
                    cv5.value(int(self.CY[self.pattern][self.step])*int(randint(0,99)<self.randomness))
                    cv6.value(int(self.CL[self.pattern][self.step])*int(randint(0,99)<self.randomness))
            
            elif self.rand_fill_mode == 1:
            #Randomness will change the probability of a pattern and filled step 
            # Non-filled steps will never be triggered
            # at Filled-steps:
            # At randomness == 0, only patterns will trigger
            # at randomness == 25, Pattern will have a 75% chance of triggering, non patterns 25%
            # at randomness == 50, Pattern will have a 50% chance of triggering, non patterns 50%
            
                if self.fill[self.step] == 1:
                    if int(self.BD[self.pattern][self.step]) == 1:
                        cv1.value(int(randint(0,99)>self.randomness))
                    else:
                        cv1.value(int(randint(0,99)<self.randomness))
                    
                    if int(self.SN[self.pattern][self.step]) == 1:
                        cv2.value(int(randint(0,99)>self.randomness))
                    else:
                        cv2.value(int(randint(0,99)<self.randomness))

                    if int(self.HH[self.pattern][self.step]) == 1:
                        cv3.value(int(randint(0,99)>self.randomness))
                    else:
                        cv3.value(int(randint(0,99)<self.randomness))

                    if int(self.OH[self.pattern][self.step]) == 1:
                        cv4.value(int(randint(0,99)>self.randomness))
                    else:
                        cv4.value(int(randint(0,99)<self.randomness))

                    if int(self.CY[self.pattern][self.step]) == 1:
                        cv5.value(int(randint(0,99)>self.randomness))
                    else:
                        cv5.value(int(randint(0,99)<self.randomness))

                    if int(self.CL[self.pattern][self.step]) == 1:
                        cv6.value(int(randint(0,99)>self.randomness))
                    else:
                        cv6.value(int(randint(0,99)<self.randomness))




                
            # Incremenent the clock step
            self.clock_step +=1
            self.step += 1

            # function timing code. Leave in and activate as needed
            #delta = time.ticks_diff(time.ticks_us(), t)
            #print('Function {} Time = {:6.3f}ms'.format('clockTrigger', delta/1000))

        @din.handler_falling
        def clockTriggerEnd():
            cv1.off()
            cv2.off()
            cv3.off()
            cv4.off()
            cv5.off()
            cv6.off()
        
    def getParams(self):

        # Random
        #CV attenuated by mk1
        val = (ma1.percent())*mk1.percent() 
        extra_random = int(val*50) # 0-50            
        self.randomness = min(k1.read_position(steps=51) + extra_random,50)

        # Fill
        val = (ma2.percent())*mk2.percent() 
        extra_fill = round(val*self.step_length) # 0 to step_length-1
        nfill = k2.read_position(self.step_length+1) + extra_fill
        if nfill < 1: nfill = 1
        elif nfill > self.step_length: nfill = self.step_length
        self.fill = eucledian_rhythm(self.step_length,nfill)

        # Pattern
        val = (ma3.percent())*mk3.percent() 
        self.extra_pattern = round(val*(len(self.BD)-1))-1 # 0- number of patterns
        self.pattern = (self.base_pattern + self.extra_pattern)%len(self.BD)
        self.step_length = len(self.BD[self.pattern])



        # extra_random = 0
        # extra_fill = 0
        # self.extra_pattern = 0
            
        # if self.analogInputMode == 0: #Random
        #     extra_random = int(val*50) # 0-50            
            
        # elif self.analogInputMode == 1: #Fill
        #     extra_fill = round(val*self.step_length) # 0 to step_length-1
            
        # elif self.analogInputMode == 2: # Pattern
        #     self.extra_pattern = round(val*(len(self.BD)-1))-1 # 0- number of patterns

        #     self.pattern = (self.base_pattern + self.extra_pattern)%len(self.BD)
        #     self.step_length = len(self.BD[self.pattern])

            
        # self.randomness = min(k1.read_position(steps=51) + extra_random,50)

        # nfill = k2.read_position(self.step_length+1) + extra_fill
        # if nfill < 1: nfill = 1
        # elif nfill > self.step_length: nfill = self.step_length
        # self.fill = eucledian_rhythm(self.step_length,nfill)


    def main(self):
        while True:
            self.getParams()            
            self.updateScreen()
            # If I have been running, then stopped for longer than reset_timeout, reset the steps and clock_step to 0
            if self.clock_step != 0 and ticks_diff(ticks_ms(), din.last_triggered()) > self.reset_timeout:
                self.step = 0
                self.clock_step = 0

    def visualizePattern(self, pattern):
        self.t = pattern
        self.t = self.t.replace('1','o')
        self.t = self.t.replace('0',' ')
        return self.t
    
    def visualizeFill(self, fillpattern):

        for i in range(len(fillpattern)):
            oled.pixel((8*i)+2,0,fillpattern[i])
            oled.pixel((8*i)+3,0,fillpattern[i])
            oled.pixel((8*i)+4,0,fillpattern[i])
            oled.pixel((8*i)+5,0,fillpattern[i])       


        filltext = ''
        for i in range(0, len(fillpattern)):
            if fillpattern[i] == 1:
                filltext += '-'
            else:
                filltext += ' '
        return filltext
    
    def downarrow(self,pos,color = 1):  
        x= (8 * pos) + 1
        
        for i in range(6):
            oled.pixel(x+i,0,color)
        for i in range(4):
            oled.pixel(x+i+1,1,color)
        for i in range(2):
            oled.pixel(x+i+2,2,color)

    def displayPattern(self):
        # Show selected pattern visually
        spacing = 8
        oled.text(self.visualizePattern(self.BD[self.pattern]), 0, spacing*0+6, 1)
        oled.text(self.visualizePattern(self.SN[self.pattern]), 0, spacing*1+6, 1)
        oled.text(self.visualizePattern(self.HH[self.pattern]), 0, spacing*2+6, 1)
        oled.text(self.visualizePattern(self.OH[self.pattern]), 0, spacing*3+6, 1)
        oled.text(self.visualizePattern(self.CY[self.pattern]), 0, spacing*4+6, 1)
        oled.text(self.visualizePattern(self.CL[self.pattern]), 0, spacing*5+6, 1)
        
        self.visualizeFill(self.fill)
        
    def updateScreen(self):
        
        oled.fill(0) 
        self.displayPattern()
        self.downarrow(self.step-1)
        
        #' R99 F16 P42 &4 '       
        oled.fill_rect(self.analogInputMode*32+8,OLED_HEIGHT- 9, 24, 8, 1)

        oled.text('R' + str(int(self.randomness)), CHAR_WIDTH*1, OLED_HEIGHT-CHAR_HEIGHT, self.analogInputMode !=0) #randomness analogInputMode = 0
        oled.text('F' + str(sum(self.fill)), CHAR_WIDTH*5, OLED_HEIGHT-CHAR_HEIGHT, self.analogInputMode != 1)       #fill analogInputMode =1
        oled.text('P' + str(self.pattern), CHAR_WIDTH*9, OLED_HEIGHT-CHAR_HEIGHT, self.analogInputMode != 2)         #pattern analogInputMode =2

        if self.rand_fill_mode == 0:
            oled.text('A', CHAR_WIDTH*13, OLED_HEIGHT-CHAR_HEIGHT, True)
        else:
            oled.text('B', CHAR_WIDTH*13, OLED_HEIGHT-CHAR_HEIGHT, True)
        
        oled.text(str(self.CLOCK_DIVISORS[self.clock_divisor]), CHAR_WIDTH*14, OLED_HEIGHT-CHAR_HEIGHT, 1)
        oled.show()
    
class pattern:
    # Initialize pattern lists
    BD=[]
    SN=[]
    HH=[]
    OH=[]
    CY=[]
    CL=[]

    # Patterns above 16 steps are tracked but only first 16 are displayed
    # African Patterns
    #0
    # BD.append("10110000001100001011000000110000")
    # SN.append("10001000100010001010100001001010")
    # HH.append("00001011000010110000101100001011") 
    # OH.append("00010000010000000001010000000000")
    # CY.append("01000100000001010100000100001010")
    # CL.append("00000010010000010000000000100000")

    # BD.append("10101010101010101010101010101010")
    # SN.append("00001000000010000000100000001001")
    # HH.append("10100010101000101010001010100000")
    # OH.append("00000000000000000000000000000000")
    # CY.append("00000000000000000000000000000000")
    # CL.append("00000000000000000000000000000000")    

    # BD.append("11000000101000001100000010100000")
    # SN.append("00001000000010000000100000001010")
    # HH.append("10111001101110011011100110111001")
    # OH.append("00000000000000000000000000000000")
    # CY.append("00000000000000000000000000000000")
    # CL.append("00000000000000000000000000000000")

    # BD.append("10001000100010001000100010001010")
    # SN.append("00100100101100000010010010110010")
    # HH.append("10101010101010101010101010101011")
    # OH.append("00000000000000000000000000000000")
    # CY.append("00000000000000000000000000000000")
    # CL.append("00000000000000000000000000000000")

    # BD.append("00101011101000111010001110100010")
    # SN.append("00101011101000111010001110100010")
    # HH.append("00001000000010000000100000001000")
    # OH.append("00000000000000000000000000000000")
    # CY.append("00000000000000000000000000000000")
    # CL.append("00000000000000000000000000000000")

    # BD.append("10101111101000111010001110101000")
    # SN.append("10101111101000111010001110101000")
    # HH.append("00000000101000001010000010100010")
    # OH.append("00000000000000000000000000000000")
    # CY.append("00000000000000000000000000000000")
    # CL.append("00000000000000000000000000000000")

    # BD.append("10110110000011111011011000001111")
    # SN.append("10110110000011111011011000001111")
    # HH.append("11111010001011111010001110101100")
    # OH.append("00000000000000000000000000000000")
    # CY.append("00000000000000000000000000000000")
    # CL.append("00000000000000000000000000000000")

    # BD.append("10010100100101001001010010010100")
    # SN.append("00100010001000100010001000100010")
    # HH.append("01010101010101010101010101010101")
    # OH.append("00000000000000000000000000000000")
    # CY.append("00000000000000000000000000000000")
    # CL.append("00000000000000000000000000000000")

    # 0,1,1,2,3,5,8,12
    #9
    # BD.append("0101011011101111")
    # SN.append("1010100100010000")
    # HH.append("1110100100010000")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")


    # Add patterns
    # BD.append("1000100010001000")
    # SN.append("0000000000000000")
    # HH.append("0000000000000000")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000000000000000")
    # HH.append("0010010010010010")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000000000")
    # HH.append("0010010010010010")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000001000")
    # HH.append("0010010010010010")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000000000")
    # HH.append("0000000000000000")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000001000")
    # HH.append("0000000000000000")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000001000")
    # HH.append("0000100010001001")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000001000")
    # HH.append("0101010101010101")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000000000000000")
    # HH.append("1111111111111111")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000001000")
    # HH.append("1111111111111111")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000000000")
    # HH.append("0001000000000000")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # BD.append("1000100010001000")
    # SN.append("0000100000000000")
    # HH.append("0001001000000000")
    # OH.append("0000000000000000")
    # CY.append("0000000000000000")
    # CL.append("0000000000000000")

    # Source: https://docs.google.com/spreadsheets/d/19_3BxUMy3uy1Gb0V8Wc-TcG7q16Amfn6e8QVw4-HuD0/edit#gid=0
    #22
    # Billie Jean
    BD.append("1000000010000000")
    SN.append("0000100000001000")
    HH.append("1010101010101010")
    OH.append("0000000000000000")
    CY.append("0000000000000000")
    CL.append("0000000000000000")

    # The Funky Drummer
    BD.append("1010001000100100")
    SN.append("0000100101011001")
    HH.append("1111111011111011")
    OH.append("0000000100000100")
    CY.append("0000000000000000")
    CL.append("0000000000000000")

    #impeach the president
    BD.append("1000000110000010")
    SN.append("0000100000001000")
    HH.append("1010101110001010")
    OH.append("0000000000100000")
    CY.append("0000000000000000")
    CL.append("0000000000000000")

    # When The Levee Breaks
    BD.append("1100000100110000")
    SN.append("0000100000001000")
    HH.append("1010101010101010")
    OH.append("0000000000000000")
    CY.append("0000000000000000")
    CL.append("0000000000000000")

    # Walk this way
    BD.append("1000000110100000")
    SN.append("0000100000001000")
    HH.append("0010101010101010")
    OH.append("1000000000000000")
    CY.append("0000000000000000")
    CL.append("0000000000000000")

    # It's a new day
    BD.append("1010000000110001")
    SN.append("0000100000001000")
    HH.append("1010101010101010")
    OH.append("0000000000000000")
    CY.append("0000000000000000")
    CL.append("0000000000000000")

    #Papa was Too
    BD.append("1000000110100001")
    SN.append("0000100000001000")
    HH.append("0000100010101011")
    OH.append("0000100000000000")
    CY.append("0000000000000000")
    CL.append("0000000000000000")

    # The big beat
    BD.append("1001001010000000")
    SN.append("0000100000001000")
    HH.append("0000000000000000")
    OH.append("0000000000000000")
    CY.append("0000000000000000")
    CL.append("0000100000001000")

    #Ashley's Roachclip															
    BD.append("1010001001100000")
    SN.append("0000100000001000")
    HH.append("1010101010001010")
    OH.append("0000000000100000")
    CY.append("1010101010101010")
    CL.append("0000000000000000")

    BD.append("1010000101110001")
    SN.append("0000100000001000")
    HH.append("1010101010001010")
    OH.append("0000000000100000")
    CY.append("0000000000000000")
    CL.append("0000000000000000")

    # End external patterns
    #32
    BD.append("1100000001010000")
    SN.append("0000101000001000")
    HH.append("0101010101010101")
    OH.append("0001000101110000")
    CY.append("0110000000001000")
    CL.append("0010000010000101")

    BD.append("1100000001010000")
    SN.append("0000101000001000")
    HH.append("1111111111111111")
    OH.append("0100101000101001")
    CY.append("0000100010000000")
    CL.append("0110000010000101")

    BD.append("1001001001000100")
    SN.append("0001000000010000")
    HH.append("0101110010011110")
    OH.append("1000001100100001")
    CY.append("0000000100001000")
    CL.append("0000100010000001")

    BD.append("1001001001000100")
    SN.append("0001000000010000")
    HH.append("1111111111111111")
    OH.append("0000000000001001")
    CY.append("1001000000000000")
    CL.append("0000101000001001")

    # Be warned patterns < 16 steps can sound disjointed when using CV to select the pattern!

    # BD.append("10010000010010")
    # SN.append("00010010000010")
    # HH.append("11100110111011")

    # BD.append("1001000001001")
    # SN.append("0001001000001")
    # HH.append("1110011011101")

    # BD.append("100100000100")
    # SN.append("000100100000")
    # HH.append("111001101110")

    # BD.append("10010000010")
    # SN.append("00010010000")
    # HH.append("11100110111")

    # BD.append("10010000010")
    # SN.append("00010010000")
    # HH.append("11111010011")

    # BD.append("1001000010")
    # SN.append("0001000000")
    # HH.append("1111101101")

    # BD.append("100100010")
    # SN.append("000100000")
    # HH.append("111110111")

    # BD.append("10010010")
    # SN.append("00010000")
    # HH.append("11111111")

    # BD.append("1001001")
    # SN.append("0001000")
    # HH.append("1111111")

    # BD.append("100100")
    # SN.append("000100")
    # HH.append("111111")

    # BD.append("10000")
    # SN.append("00001")
    # HH.append("11110")

    # BD.append("1000")
    # SN.append("0000")
    # HH.append("1111")


    # BD.append("100")
    # SN.append("000")
    # HH.append("111")

    #49 extras:

    BD.append("1000100010010010")
    SN.append("0100010001000100")
    HH.append("1010101010101010")
    OH.append("0001000100010100")
    CY.append("0110000000000000")
    CL.append("0000000010000101")

if __name__ == '__main__':
    # Reset module display state.
    [cv.off() for cv in cvs]
    dm = Consequencer()
    dm.main()


