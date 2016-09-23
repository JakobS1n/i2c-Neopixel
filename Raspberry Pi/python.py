""" Imports """
import smbus
import time
import i2cPixel

""" Decalrations """
pixels = 10

def hexToRgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def main():

    """ Setup i2c communication """
    i2cPixel.version()
    i2cPixel.setBus(1)
    i2cPixel.setAddress(0x04)

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
        while i < 10:
            i2cPixel.setPixel(i, colour[0], colour[1], colour[2])
            i = i + 1
            i2cPixel.show()

    i2cPixel.waitForSensor()
    
    
""" Start script """
main()
