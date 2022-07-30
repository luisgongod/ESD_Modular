from machine import Pin, I2C
import ssd1306
import random

# ESP32 Pin assignment 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def rect(x,y,width,height, color = 1):
  for h in range(width):
    oled.pixel(x+h,y,color)
    oled.pixel(x+h,y+ height,color)
  for v in range(height):
    oled.pixel(x,y+v,color)
    oled.pixel(x+width,y+ v,color)
  
  oled.show()

def fill_rect(x,y,width,height, color = 1):
  for h in range(width):
    for v in range(height):       
      oled.pixel(x+h,y+v,color)
  
  oled.show()
  
def hline(y,color=1):
  for i in range(oled_width):
    oled.pixel(i,y,color)  
  oled.show()

def vline(x,color=1):
  for i in range(oled_height):
    oled.pixel(x,i,color)  
  oled.show()

def randseq():
  seq = ['.']
  for i in range(15):    
    seq.append( random.choice([' ','.']))
  
  return ''.join(seq)

def downarrow(pos,color = 1):  
  x= 8*pos +1
  
  for i in range(6):
    oled.pixel(x+i,0,color)
  for i in range(4):
    oled.pixel(x+i+1,1,color)
  for i in range(2):
    oled.pixel(x+i+2,2,color)

  oled.show()

downarrow(0)
downarrow(3)
downarrow(5)
downarrow(6)
oled.text("................",0,0)


# hline(31)

spacing = 3

for i in range(6):
  oled.text(randseq(), 0, spacing * i)      

oled.text(" R99 F16 P99 &4",0,oled_height-8)

char_w_size = int(128/16)
char_h_size = int(32/2)
x_margin =2
y_margin =2

step_size = int(12)

# rect(char_w_size-2, oled_height-10, (char_w_size*3)+3,10, 1)
fill_rect((char_w_size*5)-2, oled_height-9, (char_w_size*3)+3,10, 1)
oled.text("F16",(char_w_size*5),oled_height-8,0)

# vline(8)
oled.show()



# s=int(32/3)
# ss = 0
# oled.text('8 ian nrOI!B',0,0,1)
# oled.text('8 i nO I!B',0,10,1)
# oled.text('8 ianIB',0,23,1)
# oled.show()