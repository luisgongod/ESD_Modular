"""
diagnostics_m14.py
Modified from diagnotic.py to be used with the model_14 board.
"""

# from machine import ADC
from time import sleep
from machine import Pin
from europi_m14 import OLED_HEIGHT, OLED_WIDTH, b1, b2, cvs, k1, k2, oled ,mas, mks,din1,din2,MAX_UINT16

# from europi_script import EuroPiScript
LOW = 0
HIGH = 1

def main():

    while True:
        oled.fill(0)
        
        spacing = 10
        oled.text(" v < k1  k2 > v",0,spacing *0)        
        oled.text(f" {din1.value()} {b1.value()} {int(k1.percent()*99):2d}  {int(k2.percent()*99):2d} {b2.value()} {din2.value()}", 0, spacing *1, 1)
        oled.text(" m1  m2  m3  m4",0,spacing *2)        
        oled.text(f"k{int(mks[0].percent()*99):2d}  {int(mks[1].percent()*99):2d}  {int(mks[2].percent()*99):2d}  {int(mks[3].percent()*99):2d}",0,spacing *3)        
        oled.text(f"a{int(mas[0].percent()*99):2d}  {int(mas[1].percent()*99):2d}  {int(mas[2].percent()*99):2d}  {int(mas[3].percent()*99):2d}",0,spacing *4)        
        oled.text(f"v{int(mas[0].read_voltage()):2d}  {int(mas[1].read_voltage()):2d}  {int(mas[2].read_voltage()):2d}  {int(mas[3].read_voltage()):2d}",0,spacing *5)        
        

        cvs[0]._set_duty(int(k1.percent()*MAX_UINT16))
        cvs[1]._set_duty(int(k2.percent()*MAX_UINT16))
        cvs[2]._set_duty(int(mks[0].percent()*MAX_UINT16))
        cvs[3]._set_duty(int(mks[1].percent()*MAX_UINT16))
        cvs[4]._set_duty(int(mks[2].percent()*MAX_UINT16))
        cvs[5]._set_duty(int(mks[3].percent()*MAX_UINT16))

        # show the screen boundaries
        # oled.rect(0, 0, OLED_WIDTH, OLED_HEIGHT, 1)
        oled.show()

        sleep(0.1)


if __name__ == "__main__":
    main()










