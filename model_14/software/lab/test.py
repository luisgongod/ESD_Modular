# %%

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

clocks = []
clocks.append(Clock(1))
clocks.append(Clock(2))
clocks.append(Clock(2))
clocks.append(Clock(2))
clocks.append(Clock(4))
clocks.append(Clock(8))
links = [True, True, False, True, False, True]
outputs = [0, 0, 0, 0, 0, 0]


def beat(clocks,links):
    """Called when the clock input is triggered"""    
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
    

for t in range(18):
    print(t+1,beat(clocks,links))    


# %%
