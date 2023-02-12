from machine import Pin, ADC, PWM, freq
from time import sleep
from europi import oled, b1, b2
from europi_script import EuroPiScript

CALIBRATION_FILE = "lib/calibration_values.py"
SAMPLE_SIZE = 256
HIGH = 1
LOW = 0
HIGH_RES = 2
LOW_RES = 1

class Calibrate(EuroPiScript):
    @classmethod
    def display_name(cls):
        """Push this script to the end of the menu."""
        return "~Calibrate"

    def main(self):
        ain = ADC(Pin(26, Pin.IN, Pin.PULL_DOWN))
        cv1 = PWM(Pin(21))
        usb = Pin(24, Pin.IN)

        def sample():
            readings = []
            for reading in range(SAMPLE_SIZE):
                readings.append(ain.read_u16())
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

        # Calibration start

        if usb.value() == HIGH:
            oled.centre_text("Make sure rack\npower is on\nDone: Button 1")
            wait_for_b1(HIGH)
            wait_for_b1(LOW)

        text_wait("Calibration\nMode", 3)

        oled.centre_text("Choose Process\n\n1         2")
        while True:
            if b1.value() == HIGH:
                chosen_process = HIGH_RES
                break
            elif b2.value() == HIGH:
                chosen_process = LOW_RES
                break

        # Input calibration
        open(CALIBRATION_FILE, 'w').close()

        readings = []
        if chosen_process == LOW_RES:
            readings.append(wait_for_voltage(0))
            readings.append(wait_for_voltage(10))
        else:
            for voltage in range(11):
                readings.append(wait_for_voltage(voltage))

        with open(f"lib/calibration_values.py", "w") as file:
            values = ", ".join(map(str, readings))
            file.write(f"INPUT_CALIBRATION_VALUES=[{values}]")

        # Output Calibration

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
    Calibrate().main()

