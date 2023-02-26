from machine import Pin, PWM
from time import sleep

PIN_CLK = 0

ADDR_PIN = 4
WRITE_PIN = 16
READ_PIN = 17

RESET_PIN = 33

DA0_PIN = 10
DA1_PIN = 9
DA2_PIN = 13
DA3_PIN = 12
DA4_PIN = 14
DA5_PIN = 27
DA6_PIN = 26
DA7_PIN = 25

SHORT_DELAY = 0.001
FMASTER = 1000000 # 1MHz

# a to g
TONE = [142,134,127,119,113,106,100,95,89,84,80,75,71]

        

class Bus():
    def __init__(self, da0, da1, da2, da3, da4, da5, da6, da7):
        self.da0 = Pin(da0, Pin.OUT)
        self.da1 = Pin(da1, Pin.OUT)
        self.da2 = Pin(da2, Pin.OUT)
        self.da3 = Pin(da3, Pin.OUT)
        self.da4 = Pin(da4, Pin.OUT)
        self.da5 = Pin(da5, Pin.OUT)
        self.da6 = Pin(da6, Pin.OUT)
        self.da7 = Pin(da7, Pin.OUT)

    def set(self, upper, lower):
        self.da0.value(upper & 0x01)
        self.da1.value(upper & 0x02)
        self.da2.value(upper & 0x04)
        self.da3.value(upper & 0x08)
        self.da4.value(lower & 0x01)
        self.da5.value(lower & 0x02)
        self.da6.value(lower & 0x04)
        self.da7.value(lower & 0x08)
    
    def register(self, value):
        self.set(0x00, value)

    
    def clr(self):
        self.set(0, 0)
    

    def __del__(self):
        self.da0.deinit()
        self.da1.deinit()
        self.da2.deinit()
        self.da3.deinit()
        self.da4.deinit()
        self.da5.deinit()
        self.da6.deinit()
        self.da7.deinit()



class Clock():
    def __init__(self, pin):
        self.p = PWM(pin)
        self.p.freq(1000000)
        self.p.init()

    def set(self, freq):
        self.p.freq(freq)

    def stop(self):
        self.p.deinit()

    def start(self):
        self.p.init()

    def __del__(self):
        self.p.deinit()


class BusControl():    
    def __init__(self, addr_pin, write_pin, read_pin,reset_pin):
        self.addr_pin = Pin(addr_pin, Pin.OUT)
        self.write_pin = Pin(write_pin, Pin.OUT)
        self.read_pin = Pin(read_pin, Pin.OUT)
        self.reset_pin = Pin(reset_pin, Pin.OUT)
    
    def reset(self):
        self.reset_pin.value(1)
        sleep(10)
        self.reset_pin.value(0)
        sleep(10)
        self.reset_pin.value(1)
    
    def inact(self):
        self.addr_pin.value(0)
        self.write_pin.value(0)
        self.read_pin.value(0)
    
    def addr(self):
        self.addr_pin.value(1)
        self.write_pin.value(0)
        self.read_pin.value(0)

    def addr_read(self):
        self.addr_pin.value(1)
        self.write_pin.value(0)
        self.read_pin.value(1)
     
    def addr_write(self):
        self.addr_pin.value(1)
        self.write_pin.value(1)
        self.read_pin.value(0)

    def read(self):
        self.addr_pin.value(0)
        self.write_pin.value(0)
        self.read_pin.value(1)

    def write(self):
        self.addr_pin.value(0)
        self.write_pin.value(1)
        self.read_pin.value(0)
    

class Voice():
    def __init__(self, freq_fine_reg, freq_coarse_reg, volume_reg):
        self.freq_fine_reg = freq_fine_reg
        self.freq_coarse_reg = freq_coarse_reg
        self.volume_reg = volume_reg
        self.freq_fine = 0
        self.freq_coarse = 0
        self.volume = 0

    def set(self, freq, volume):
        self.freq_fine = freq & 0xFF
        self.freq_coarse = freq >> 8    
        self.volume = volume

class Mixer():
    def __init__(self, mixer_reg,noise_freq_reg, env_fine_reg, env_coarse_reg, env_shape_reg):
        self.mixer_reg = mixer_reg
        self.env_fine_reg = env_fine_reg
        self.env_coarse_reg = env_coarse_reg
        self.env_shape_reg = env_shape_reg
        self.noise_freq_reg = noise_freq_reg

        self.noise_freq_data = 0x00
        self.mixer_data = 0x00
        self.env_shape_data = 0x00

    def set_io(self, io_A, io_B):
        self.mixer_data = self.mixer_data  | io_A << 7 | io_B << 6

    def set_mixer(self, ch_A, ch_B, ch_C, noise_A, noise_B, noise_C):
        self.mixer_data = self.mixer_data | ch_A << 0 | ch_B << 1 | ch_C << 2 | noise_A << 3 | noise_B << 4 | noise_C << 5

    def set_env(self, env_CONT, env_ALT, env_ATTACK, env_HOLD):
        self.env_shape_data = self.env_shape_data | env_CONT << 0 | env_ALT << 1 | env_ATTACK << 2 | env_HOLD << 3


class YM2149():
    def __init__(self, bus, bus_control):
        self.bus = bus
        self.bus_control = bus_control

        self.voice_A = Voice(0x00, 0x01, 0x08)
        self.voice_B = Voice(0x02, 0x03, 0x09)
        self.voice_C = Voice(0x04, 0x05, 0x0A)
        self.voices = [self.voice_A, self.voice_B, self.voice_C]
        self.mixer = Mixer(0x07, 0x06, 0x0B, 0x0C, 0x0D)


    def write(self, addr, data):
        self.bus.register(addr)
        self.bus_control.addr()
        sleep(SHORT_DELAY)

        self.bus.register(data)
        self.bus_control.addr_write()
        sleep(SHORT_DELAY)
        self.bus_control.write()
        sleep(SHORT_DELAY)
        self.bus_control.inact()    
        sleep(SHORT_DELAY)
    
    def set_mix(self, ch_A, ch_B, ch_C, noise_A, noise_B, noise_C):
        self.mixer.set_mixer(ch_A, ch_B, ch_C, noise_A, noise_B, noise_C)
        self.write(self.mixer.mixer_reg, self.mixer.mixer_data)
    
    def set_io(self, io_A, io_B):
        self.mixer.set_io(io_A, io_B)
        self.write(self.mixer.mixer_reg, self.mixer.mixer_data)
    
    def set_env(self, env_CONT, env_ALT, env_ATTACK, env_HOLD):
        self.mixer.set_env(env_CONT, env_ALT, env_ATTACK, env_HOLD)
        self.write(self.mixer.env_shape_reg, self.mixer.env_shape_data)

    def set_noise_freq(self, freq):
        self.mixer.noise_freq_data = freq
        self.write(self.mixer.noise_freq_reg, self.mixer.noise_freq_data)
    
    def set_voice(self, voice, freq, volume):
        if voice == 0:
            self.voice_A.set(freq, volume)
            self.write(self.voice_A.freq_fine_reg, self.voice_A.freq_fine)
            self.write(self.voice_A.freq_coarse_reg, self.voice_A.freq_coarse)
            self.write(self.voice_A.volume_reg, self.voice_A.volume)
        elif voice == 1:
            self.voice_B.set(freq, volume)
            self.write(self.voice_B.freq_fine_reg, self.voice_B.freq_fine)
            self.write(self.voice_B.freq_coarse_reg, self.voice_B.freq_coarse)
            self.write(self.voice_B.volume_reg, self.voice_B.volume)
        elif voice == 2:
            self.voice_C.set(freq, volume)
            self.write(self.voice_C.freq_fine_reg, self.voice_C.freq_fine)
            self.write(self.voice_C.freq_coarse_reg, self.voice_C.freq_coarse)
            self.write(self.voice_C.volume_reg, self.voice_C.volume)


    



def main():
    clock = Clock(Pin(PIN_CLK))
    clock.start()
    bus = Bus(DA0_PIN, DA1_PIN, DA2_PIN, DA3_PIN, DA4_PIN, DA5_PIN, DA6_PIN, DA7_PIN)
    bus_control = BusControl(ADDR_PIN, WRITE_PIN, READ_PIN, RESET_PIN)
    ym2149 = YM2149(bus, bus_control)
    
    ym2149.set_mix(1, 1, 1, 0, 0, 0)
    ym2149.set_io(0, 1)
    ym2149.set_env(0, 0, 0, 0)
    ym2149.set_noise_freq(0x00)

    while True:
        for i in range(0, 3):
            ym2149.set_voice(0, TONE[i], 0x0F)
            ym2149.set_voice(1, TONE[i+1], 0x0F)
            ym2149.set_voice(2, TONE[i+2], 0x0F)
            sleep(1)

        

    

    pass

if __name__ == '__main__':
    main()
    pass
    