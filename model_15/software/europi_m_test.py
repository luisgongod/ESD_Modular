"""
diagnostics_dev.py
Modified from diagnotic.py to be used with the europi_dev board.
Use with original in lib/europi.py

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

        oled.text(f"k1:{int(k1.percent()*100)}", 16, 3, 1)
        oled.text(f"k2:{int(k2.percent()*100)}", 64, 3, 1)
        oled.text(f"ma1", 16, 13, 1)
        oled.text(f"ma3", 64, 13, 1)

        #percents
        oled.text(f"%:", 0, 23, 1)
        oled.text(f"{int(mas[0].percent()*100)}", 16, 23, 1)
        oled.text(f"{int(mas[2].percent()*100)}", 64, 23, 1)

        oled.text(f"v:", 0, 33, 1)
        oled.text(f"{mas[0].read_voltage():5.1f}", 16, 33, 1)
        oled.text(f"{mas[2].read_voltage():5.1f}", 64, 33, 1)


        cvs[0]._set_duty(int(0xffff * k1.percent()))
        cvs[1]._set_duty(int(0xffff * k2.percent()))
        cvs[2]._set_duty(int(0xffff * mks[0].percent()))
        cvs[3]._set_duty(int(0xffff * mks[1].percent()))
        cvs[4]._set_duty(int(0xffff * mks[2].percent()))
        cvs[5]._set_duty(int(0xffff * mks[3].percent()))

        # show the screen boundaries
        oled.rect(0, 0, OLED_WIDTH, OLED_HEIGHT, 1)
        oled.show()

        sleep(0.1)


if __name__ == "__main__":
    main()









