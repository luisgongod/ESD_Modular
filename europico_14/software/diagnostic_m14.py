"""
diagnostics_m14.py
Modified from diagnotic.py to be used with the model_14 board.
"""

# from machine import ADC
from time import sleep
from machine import Pin
from europi_m import OLED_HEIGHT, OLED_WIDTH, b1, b2, cvs, k1, k2, oled ,mas, mks,din1,din2

# from europi_script import EuroPiScript
LOW = 0
HIGH = 1

def main():

    while True:
        oled.fill(0)
        
        channel = 0

        # display the input values
        #display.text('Hello World', 0, 0, 1)    # draw some text at x=0, y=0, colour=1
        # oled.text(f"ain: {ain.read_voltage():5.2f}v ch:{channel}", 2, 3, 1)
        
        # oled.text(f"k1: {k1.read_position():2}  k2: {k2.read_position():2}", 2, 13, 1)
        # oled.text(f"d1{din2.value()} b1{b1.value()} b2{b2.value()} d2{din.value()}", 2, 23, 1)
        # oled.text(f"Ks:{mk1.read_position():2} {mk2.read_position():2} {mk3.read_position():2} {mk4.read_position():2}", 2, 33, 1)
        # oled.text(f"As:{ma1.read_voltage():5.2f} {ma2.read_voltage():5.2f}", 2, 43, 1)
        # oled.text(f"As:{ma3.read_voltage():5.2f} {ma4.read_voltage():5.2f}", 2, 53, 1)

        oled.text(f"1:{int(k1.percent()*100)} {mas[0].read_voltage():5.2f}", 0, 13, 1)
        oled.text(f"2:{int(k2.percent()*100)} {mas[1].read_voltage():5.2f}", 0, 23, 1)
        oled.text(f"3:{int(mks[0].percent()*100)} {mas[2].read_voltage():5.2f}", 0, 33, 1)
        oled.text(f"4:{int(mks[1].percent()*100)} {mas[3].read_voltage():5.2f}", 0, 43, 1)
        oled.text(f"5:{int(mks[2].percent()*100)} {din1.value()}", 0, 53, 1)
        oled.text(f"6:{int(mks[3].percent()*100)} {din2.value()}", 0, 63, 1)


        cvs[0].voltage(int(k1.percent()*10))
        cvs[1].voltage(int(k2.percent()*10))
        cvs[2].voltage(int(mks[0].percent()*10))
        cvs[3].voltage(int(mks[1].percent()*10))
        cvs[4].voltage(int(mks[2].percent()*10))
        cvs[5].voltage(int(mks[3].percent()*10))

        # show the screen boundaries
        oled.rect(0, 0, OLED_WIDTH, OLED_HEIGHT, 1)
        oled.show()

        sleep(0.1)


if __name__ == "__main__":
    main()









