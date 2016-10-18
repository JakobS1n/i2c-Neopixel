""" Imports """
import logging
import smbus
import time
import json
import i2cPixel

""" Decalrations """
pixels = 72 # Change this to the appropriate number for your setup
pixels = 10
addresses = [0, 24, 25, 35] # legg til en start og en stopp for hvert trinn

def hexToRgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def lightStaircase(direction):
	repeats = len(addresses)
	repeats = repeats / 2
	
	if direction = "up":
		loopCondition = repeats
		while loopCondition >> pixels
			
	else:
		loopCondition = 0
	
	return true
	
def setup():

    """ Setup i2c communication """
    i2cPixel.version()
    i2cPixel.setBus(1)
    i2cPixel.setAddress(0x04)

def main():
    
    """ Wait for heartbeat from Arduino """
    while True:
	try:
        	if i2cPixel.greeting():
            		print "Arduino is Online"
            		break
	except Exception:
		pass

    """while True:
        i2cPixel.waitForSensor()"""
    
    """ Test, set all pixels to entered color """
    while True:
        test = raw_input()
        colour = hexToRgb(test)
        
        i = 0
        while i < pixels:
            i2cPixel.setPixel(i, colour[0], colour[1], colour[2])
            i = i + 1
            i2cPixel.show()

    i2cPixel.waitForSensor()
    
    
""" Start script """
setup() #configure
main() #Start main
