# Basic remote control from microbit V1
# Trace the code to determine how the basic system works
# What would would a better interface for a different context?

from microbit import *
import radio

chnl = xx #change the channel to your team number
radio.config(channel=chnl)
radio.on()

while True:
    y = accelerometer.get_y() 
    a = button_a.is_pressed()
    b = button_b.is_pressed()
    if  a:
        #left
        display.show(Image.ARROW_W)
        radio.send("W")
    elif b:
        #right
        display.show(Image.ARROW_E)
        radio.send("E")
    elif y>300:
        #backwards
        display.show(Image.ARROW_S)
        radio.send("S")
    elif y<-300:
        # forwards
        display.show(Image.ARROW_N)
        radio.send("N")
    else:
        continue
    sleep(20)
