#!/bin/env python
import RPi.GPIO as GPIO
from phue import Bridge
from time import time
pin_global=13 #set global 

b=Bridge('11.1.11') #enter ip address for hue light bridge. 
b.connect()
light_names = b.get_light_objects('name') # get the names of the hue lights in home
def setup():
    
    light_names = b.get_light_objects('name')
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(pin_global, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def on_ir_receive(): #for version one accept the light signal and set toggle the light.
    GPIO.wait_for_edge(pin_global, GPIO.FALLING)
    light_names["LightName"].on = not light_names["LightName"].on
    
    return True

def destroy():
    GPIO.cleanup()


if __name__ == "__main__":
    setup()
    try:
        print("Starting IR Listener")
        while True:
            print("Waiting for signal")  
            GPIO.wait_for_edge(pin_global, GPIO.RISING) # wait to see a rising edge from the GPIO off the board.
            code = on_ir_receive()
            if code:
                print(str(hex(code)))
            else:
                print("Invalid code")
    except KeyboardInterrupt:
        pass
    except RuntimeError:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        pass
    print("Quitting")
    destroy()
