from machine import Pin, ADC, PWM, freq
from time import sleep
from europi_m import oled, b1, b2, m0, ma1,ma2, ma3, ma4
from europi_script import EuroPiScript

CALIBRATION_FILE = "lib/calibration_values_m.py"
SAMPLE_SIZE = 256
HIGH = 1
LOW = 0

HIGH_RES = 2
LOW_RES = 1
class Calibrate_m(EuroPiScript):
    @classmethod
    def display_name(cls):
        """Push this script to the end of the menu."""
        return "~Calibrate"

    def main(self):
        # Overclock for faster calibration
        freq(250_000_000)

        ain = ADC(Pin(26, Pin.IN, Pin.PULL_DOWN))

        #Pin 19 is leftmost Out on the module
        cv1 = PWM(Pin(19))
        usb = Pin(24, Pin.IN)

        def sample():
            readings = []
            for reading in range(SAMPLE_SIZE):
                readings.append(ain.read_u16())
                
                #Progress bar
                if reading % (SAMPLE_SIZE / 10) == 0:
                    oled.rect(0, 60, int((reading * oled.width)/SAMPLE_SIZE), 64, 1) 
                    oled.show()

            # At 0V input the ADC will have 10V (from the sum of the reference) or 0xffff,
            # so we need to subtract that
            return (0xffff - round(sum(readings) / SAMPLE_SIZE))

        def wait_for_voltage(voltage):
            wait_for_b1(LOW)
            if voltage != 0:
                oled.centre_text(f"Plug in {voltage}V\n\nDone: Button 1")
                wait_for_b1(HIGH)
            else:
                oled.centre_text(f"Unplug all\n\nDone: Button 1")
                wait_for_b1(HIGH)
            oled.centre_text("Calibrating...")
            sleep(1.5)
            return sample()

        def text_wait(text, wait):
            oled.centre_text(text)
            sleep(wait)

        def fill_show(colour):
            oled.fill(colour)
            oled.show()

        def flash(flashes, period):
            for flash in range(flashes):
                fill_show(1)
                sleep(period / 2)
                fill_show(0)
                sleep(period / 2)

        def wait_for_b1(value):
            while b1.value() != value:
                sleep(0.05)

        def calib_input_channel(channel, chosen_process , name_set , min_voltage=0, max_voltage=10):
            # Input calibration
            # assuming resolution readings of 1V

            m0.set_channel(channel)

            readings = []
            voltage_range = max_voltage - min_voltage + 1
            if chosen_process == LOW_RES:
                readings.append(wait_for_voltage(min_voltage))
                readings.append(wait_for_voltage(max_voltage))            

            #TODO: apply low res algorithm to fill in between values

            
            else:                
                for voltage in range( voltage_range ):
                    readings.append(wait_for_voltage(voltage-min_voltage))

            with open(CALIBRATION_FILE, "a+ ") as file:
                values = ", ".join(map(str, readings))
                file.write(f"{name_set}=[{values}]\n")
            
            return readings

        # Calibration start

        if usb.value() == HIGH:
            oled.centre_text("Make sure rack\npower is on\nDone: Button 1")
            wait_for_b1(HIGH)
            wait_for_b1(LOW)

        text_wait("Calibration\nMode", 3)

        oled.centre_text("Choose Process\n\n1:H      2:L\n")
        
        while True:
            if b1.value() == HIGH:
                chosen_process = HIGH_RES
                break
            elif b2.value() == HIGH:
                chosen_process = LOW_RES
                break
        
        # # Creates empty file
        open(CALIBRATION_FILE, 'w').close()

        # Calibaratrion ch 5 and 7 (0-10V) for 1st and 2nd input
        # AnalogIn channels (left to right) 5,7,4,6
        # ain 1 and 2 have unipoar 0 to 10V range
        # ain 3 and 4 have bipolar -8 to 8V range    
         
        oled.centre_text("Calibrate\n Input 1\nready: Button 1")
        wait_for_b1(HIGH)
        wait_for_b1(LOW)    

        #TODO: INPUT_CALIBRATION_VALUES name expected in europi_dev.py, change to INPUT_CALIBRATION_VALUES_DEFAULT?

        readings = calib_input_channel(ma1.channel, chosen_process, "INPUT_CALIBRATION_VALUES",0, 10) # temp_readings to be use in output calibration
        oled.centre_text("Calibrate\n Input 2\nready: Button 1")
        wait_for_b1(HIGH)
        wait_for_b1(LOW)    
        calib_input_channel(ma2.channel, chosen_process, "INPUT_CALIBRATION_VALUES_2",0, 10)
        oled.centre_text("Calibrate\n Input 3\nready: Button 1")
        wait_for_b1(HIGH)
        wait_for_b1(LOW)    
        calib_input_channel(4, chosen_process, "INPUT_CALIBRATION_VALUES_3",-8, 8)
        oled.centre_text("Calibrate\n Input 4\nready: Button 1")
        wait_for_b1(HIGH)
        wait_for_b1(LOW)    
        calib_input_channel(6, chosen_process, "INPUT_CALIBRATION_VALUES_4",-8, 8)


        # Output Calibration
        #change to 1st input channel
        m0.set_channel(ma1.channel)
        oled.centre_text(f"Plug CV1 into\nanalogue in\nDone: Button 1")
        wait_for_b1(HIGH)
        oled.centre_text("Calibrating...")        

       
        #if LOW_RES, a set of 10 readings are calculated as 1/10th of the range
        if chosen_process == LOW_RES:
            new_readings = [readings[0]]
            m = (readings[1] - readings[0]) / 10
            c = readings[0]
            for x in range(1, 10):
                new_readings.append(round((m * x) + c))
            new_readings.append(readings[1])
            readings = new_readings
        
        output_duties = [0]
        duty = 0
        cv1.duty_u16(duty)
        reading = sample()
        
        for index, expected_reading in enumerate(readings[1:]):
            while abs(reading - expected_reading) > 0.002 and reading < expected_reading:
                cv1.duty_u16(duty)
                duty += 10
                reading = sample()
                if duty>=0xffff:
                    break
            output_duties.append(duty)
            oled.centre_text(f"Calibrating...\n{index+1}V")

        with open(CALIBRATION_FILE, "a+") as file:
            values = ", ".join(map(str, output_duties))
            file.write(f"\nOUTPUT_CALIBRATION_VALUES=[{values}]")

        oled.centre_text("Calibration\nComplete!")


if __name__ == "__main__":
    Calibrate_m().main()


