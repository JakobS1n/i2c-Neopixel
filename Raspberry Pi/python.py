""" Imports """
import logging
import smbus
import time
import json
import i2cPixel

""" Decalrations """
pixels = 72 # Change this to the appropriate number for your setup

def hexToRgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def setup():
    # Get settings from config.json
    
    """ Setup i2c communication """
    i2cPixel.version()
    i2cPixel.setBus(1)
    i2cPixel.setAddress(0x04)

def main():
    
    """ Wait for heartbeat from Arduino """
    while True:
        if i2cPixel.greeting():
            print "Arduino is Online"
            break

    while True:
        test = raw_input()
        colour = hexToRgb(test)
        
        i = 0
        while i < pixels:
            i2cPixel.setPixel(i, colour[0], colour[1], colour[2])
            i = i + 1
            i2cPixel.showPixel()


""" Start script """
setup() #configure
main() #Start main
