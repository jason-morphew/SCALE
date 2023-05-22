from microbit import *
from time import sleep
import math, ustruct

# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

S1 = 0x1
S2 = 0x2
S3 = 0x3
S4 = 0x4
S5 = 0x5
S6 = 0x6
S7 = 0x7
S8 = 0x8

M1A = 0x1
M1B = 0x2
M2A = 0x3
M2B = 0x4

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04
RESET              = 0x00

SERVO_MIN = 90
SERVO_MAX = 430
SERVOC_CENTER = 127
SERVOC_RANGE = 127

address = PCA9685_ADDRESS
def setup():
# startup process - initialize i2c connection with motor driver
    i2c.init()
    i2c.write(0x40,bytearray([MODE1, RESET]))        #self.i2c.send(bytearray([MODE1, RESET]), self.address)
    set_all_pwm(0,0)
    i2c.write(address,bytearray([MODE2, OUTDRV]))    # self.i2c.send(bytearray([MODE2, OUTDRV]), self.address)
    i2c.write(address,bytearray([MODE1, ALLCALL]))    #self.i2c.send(bytearray([MODE1, ALLCALL]), self.address)
    sleep(0.005)  # wait for oscillator
    i2c.write(address, bytearray([MODE1])) # write register we want to read from first
    mode1 = i2c.read(address,1)[0]
    mode1 = mode1 & ~SLEEP
    i2c.write(address,bytearray([MODE1, mode1]))
    sleep(0.005)  # Wait for ascillator
    set_pwm_freq(50)
#    print("pwm data ",set_pwm(S1,None,None))

def set_all_pwm(on, off):
#  Sets all PWM channels."""
#    i2c.send(bytearray([ALL_LED_ON_L, on & 0xFF]), self.address)
    i2c.write(address,bytearray([ALL_LED_ON_L, on & 0xFF]))
#    i2c.send(bytearray([ALL_LED_ON_H, on >> 8]), self.address)
    i2c.write(address,bytearray([ALL_LED_ON_H, on >> 8]))  # Original Had error
#    i2c.send(bytearray([ALL_LED_OFF_L, off & 0xFF]), self.address)
    i2c.write(address,bytearray([ALL_LED_OFF_L, off & 0xFF]))
#    i2c.send(bytearray([ALL_LED_OFF_H, off >> 8]), self.address)
    i2c.write(address,bytearray([ALL_LED_OFF_H, off >> 8]))

def set_pwm_freq(freq_hz):
#Set the PWM frequency to the provided value in hertz."""
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq_hz)
    prescaleval -= 1.0
    # print('Setting PWM frequency to {0} Hz'.format(freq_hz))
    # print('Estimated pre-scale: {0}'.format(prescaleval))
    prescale = int(math.floor(prescaleval + 0.5))
    # print('Final pre-scale: {0}'.format(prescale))
    # self.i2c.send(bytearray([MODE1]), self.address) # write register we want to read from first
    #oldmode = self.i2c.mem_read(1, self.address, MODE1)[0]
    i2c.write(address, bytearray([MODE1])) # These two lines replace mem_read
    oldmode = i2c.read(address,1)[0]
    newmode = (oldmode & 0x7F) | 0x10    # sleep
    i2c.write(address,bytearray([MODE1, newmode]))  # go to sleep
    i2c.write(address,bytearray([PRESCALE, prescale]))
    i2c.write(address,bytearray([MODE1, oldmode]))
    sleep(0.005)
    i2c.write(address,bytearray([MODE1, oldmode | 0x80]))

def set_pwm(channel, on, off):
# Sets a single PWM channel."""
    if on is None or off is None:
    # self.i2c.send(bytearray([LED0_ON_L+4*channel]), self.address) # write register we want to read from first
        #data = self.i2c.mem_read(4, self.address, LED0_ON_L+4*channel)
        i2c.write(address, bytearray([LED0_ON_L+4*channel])) # These two lines replace mem_read
        data = i2c.read(address,4)
        return ustruct.unpack('<HH', data)

    i2c.write(address,bytearray([LED0_ON_L+4*channel, on & 0xFF]))
    i2c.write(address,bytearray([LED0_ON_H+4*channel, on >> 8]))
    i2c.write(address,bytearray([LED0_OFF_L+4*channel, off & 0xFF]))
    i2c.write(address,bytearray([LED0_OFF_H+4*channel, off >> 8]))

def servo(index, degree):
# Standard servo
# 50hz: 20,000 us
#    v_us = (degree*1000/180+1000)
#    value = int(v_us*4096/20000) * 2
    gain = int(SERVO_MAX - SERVO_MIN)/180
    value = int(degree*gain + SERVO_MIN)
    set_pwm(index+7, 0, value)

def servoc(index, pct_speed):
        # 50hz: 20,000 us
#        v_us = (degree*1000/180+1000)
#        value = int(v_us*4096/20000) * 2
# Positive speed is CW and Negative speed is CCW
    if pct_speed > 99:
        pct_speed = 99
    elif pct_speed < -99:
        pct_speed == -99
    value = SERVOC_CENTER - int((pct_speed*SERVOC_RANGE)/100)
    set_pwm(index+7, 0, value)

def servoc_stop(index):
    servoc(index,0)

def motor(index, pct_speed):
    speed = int((pct_speed/100)*255) 
    speed = speed * 16 # map from 256 to 4096
    if index>4 or index<=0:
        return
    pp = (index-1)*2
    pn = (index-1)*2+1
    if speed < 0:
        set_pwm(pp, 0, -speed)
        set_pwm(pn, 0, 0)
    else:
        set_pwm(pp, 0, 0)
        set_pwm(pn, 0, speed)
