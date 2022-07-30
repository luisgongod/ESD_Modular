#oled_diagnostic
# https://wokwi.com/projects/337429303218143826
from machine import Pin, I2C
import ssd1306
import random

# ESP32 Pin assignment 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
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

spacing = 10
oled.text(" v < k1 k2 > v",0,spacing *0)
oled.text(" 0 0 99  99 0 0 ",0,spacing *1)
hline(spacing *1 +8)
oled.text(" m1  m2  m3  m4",0,spacing *2)
oled.text(" 99  99  99  99 ",0,spacing *3)
oled.text(" 99  99  99  99 ",0,spacing *4)
oled.text(" 99  99  99  99 ",0,spacing *5)

char_w_size = int(128/16)
char_h_size = int(32/2)
x_margin =2
y_margin =2

oled.show()

