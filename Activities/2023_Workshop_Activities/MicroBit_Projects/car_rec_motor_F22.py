from microbit import *
import radio
chnl = XX #change channel to your team number
import robotbit_library as r
# Define Ports for the bank of high current output
M1A = 0x1
M1B = 0x2
M2A = 0x3
M2B = 0x4
r.setup()

radio.config(channel=chnl)
radio.on()

def Drive(lft,rgt):
    r.motor(M2B, lft)
    r.motor(M1A, rgt)

while True:
    s = radio.receive()
    if s is not None:
        if s=="N":
            Drive(-255,255)
            display.show(Image.ARROW_N)
        elif s=="S":
            Drive(255,-255)
            display.show(Image.ARROW_S)
        elif s=="E":
            Drive(-255,0)
            display.show(Image.ARROW_E)
        elif s=="W":
            Drive(0,255)
            display.show(Image.ARROW_W)
    else:
        Drive(0,0)
    sleep(20)

