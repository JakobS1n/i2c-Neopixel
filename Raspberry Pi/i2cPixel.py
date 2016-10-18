""" Includes """
import smbus
import sys
import time

""" Variables """
lockdown = False

def version():
    print "i2cPixel is Version 1.0.0"

def setAddress(address):
    global arduinoAddress
    arduinoAddress = address

def setBus(n):
    global bus
	try:
		bus = smbus.SMBus(n)
	except:
		errorMsg = sys.exc_info()[0]
		errorHandler(5, errorMsg)

def available():
	global lockdown
	return lockdown
	
def greeting():
    """ Send heartbeat """
    bus.write_byte(arduinoAddress, 0x01)

    """ Wait for response """
    try:	
        response = bus.read_byte(arduinoAddress)
        if response == 0x01:
            returnMsg = True
        else:
            returnMsg = False
    except:
		errorMsg = sys.exc_info()[0]
		errorHandler(5, errorMsg)
        returnMsg = False
		
    """ Return if heartbeat was received """        
    return returnMsg

def setPixel(n, red, green, blue):
    """ Send values for changing pixel values """
	try:
		bus.write_block_data(arduinoAddress, 0x02, [n, red, green, blue])
	except:
		errorMsg = sys.exc_info()[0]
		errorHandler(5, errorMsg)

def show():
	""" Send values for turning pixels on """
	try:
		bus.write_byte(arduinoAddress, 0x03)
	except:
		errorMsg = sys.exc_info()[0]
		errorHandler(5, errorMsg)
    
def blink(time, red, green, blue):
	""" Flash all pixels with a colour """
	try:
		bus.write_block_data(arduinoAddress, 0x04, [red, green, blue, time])
	except:
		errorMsg = sys.exc_info()[0]
		errorHandler(5, errorMsg)

def waitForSensor():
    while True:
        try:
            sensorData = bus.read_byte(arduinoAddress)
            if sensorData == 0x02:
                print "Sensor 1 Triggered"
                return 1
                break;
            if sensorData == 0x03:
                print "Sensor 2 Triggered"
                return 2
                break;
        except Exception:
            pass
