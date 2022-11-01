from europi_m14 import *
from time import sleep_ms
from europi_script import EuroPiScript

class Clock:
    def __init__(self, division = 1):
        self.counter = 0
        self.division = division
        self.DIV_CHOICES = [1, 2, 4, 8, 16, 32]

    def clock(self):
        self.counter += 1
        if self.counter >= self.division:
            self.counter = 0
            return True
        else:
            return False
             
    def reset(self):
        self.counter = 0

class ChronoTrigger(EuroPiScript):
    
    def __init__(self):
        super().__init__()
        self.divisions = [1, 2, 2, 2, 4, 8]
        self.clocks = []
        self.clocks.append(Clock(self.divisions[0]))
        self.clocks.append(Clock(self.divisions[1]))
        self.clocks.append(Clock(self.divisions[2]))
        self.clocks.append(Clock(self.divisions[3]))
        self.clocks.append(Clock(self.divisions[4]))
        self.clocks.append(Clock(self.divisions[5]))
        
        self.links = [False, False, False, False, False, False]
        self.outputs = [0, 0, 0, 0, 0, 0]
        self.selected_pair = 0 # up to 5 pairs (6 outputs)
        
        din1.handler(self.beat_hander) #external clock in signal
        din1.handler_falling(self.beat_off) #external clock in signal lenght 
        din2.handler(self.reset) #external reset signal

        b1.handler(self.change_link) #toggle link
        b2.handler(self.increment_selection) #select next link

    def reset(self):
        """Reset all clocks to zero"""
        for clock in self.clocks:
            clock.reset()
    
    def read_knobs(self):
        """Read the knob positions and return a list of values"""

        #k1 and k2  
        self.clocks[0].division = k1.choice(self.clocks[0].DIV_CHOICES)
        self.clocks[5].division = k2.choice(self.clocks[5].DIV_CHOICES)

        #CV clocks
        self.clocks[1].division = mka1.choice(self.clocks[1].DIV_CHOICES)
        self.clocks[2].division = mka2.choice(self.clocks[2].DIV_CHOICES)
        self.clocks[3].division = mka3.choice(self.clocks[3].DIV_CHOICES)
        self.clocks[4].division = mka4.choice(self.clocks[4].DIV_CHOICES)

    def beat_hander(self):
        self.beat(self.clocks,self.links)


    def beat(self,clocks,links):
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
                    out.extend(self.beat(clk_iter,links_iter))
            else:
                out.append(0)
                while l:
                    try:
                        l=next(links_iter)
                        next(clk_iter)
                    except StopIteration:
                        break
                    out.append(0)
                
        for i in range(len(out)):
            if out[i] == 1:
                cvs[i].on()
            else:
                cvs[i].off()
        
        return out
    
    def beat_off(self):
        """Called when the clock input is triggered down"""
        for cv in cvs:
            cv.off()


    def change_link(self):
        """Toggles the link""" 
        self.links[self.selected_pair] = not self.links[self.selected_pair]
        #TODO: save state
        # self.save_state()

    def increment_selection(self):
        """Move the selection to the next Link"""
        self.selected_pair = (self.selected_pair + 1) % 5

    def save_state(self):
        """Save the current set of divisions to file"""
        if self.last_saved() < 5000:
            return
        
        state = {
            "divisions": self.divisions,
            "links": self.modes
        }
        self.save_state_json(state)

    def update_display(self):
        """Update the display"""
        oled.clear()

      

        for i in range(len(self.clocks)):
            oled.text(str(self.clocks[i].division), 0, i*10)
            if self.links[i]:
                oled.text("L", 20, i*10)
            if i == self.selected_pair:
                oled.text(">", 30, i*10)           
        oled.show()


        pass
    
    def main(self):
        while True:
            self.read_knobs()            
            self.update_display()
            sleep_ms(10)
            



if __name__ == "__main__":
    ChronoTrigger().main()
