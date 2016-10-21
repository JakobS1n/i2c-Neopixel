""" Includes """
import smbus
import sys
import time
import logging

logging.basicConfig(filename='error.log',level=logging.DEBUG)

def errorHandler(type, errorMsg):
    if type == 1: # Debug
        logging.debug(errorMsg)
        print("Debug Message: See logfile")
    elif type == 2: # info
        logging.info(errorMsg)
    elif type == 3: # Warning 
        logging.warning(errorMsg)
    elif type == 4: # Error
        logging.error(errorMsg)
        print("Error: See logfile")
    elif type == 5: # Error
        logging.critical(errorMsg)
        print("Critical Error: See logfile")
    else:
        logging.critical(errorMsg)
        print("Something went terribly wrong! Not even the errorhandler was able to find out what. Which basically means 'You are doomed'") 
    

""" Variables """
lockdown = False

def version():
    print "i2cPixel is Version 1.0.0"

def available():
    global lockdown
    return lockdown

def setAddress(address):
    global arduinoAddress
    arduinoAddress = address

def setBus(n):
    if available == False:
        return 2
    else:
        lockdown = False
        global bus
        try:
            bus = smbus.SMBus(n)
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    lockdown = True
    
def greeting():
    if available == False:
        return 2
    else:
        lockdown = False
        try:
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
        
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    lockdown = True

def ping():
    # Send 0x07 vil faa tilbake 42 hvis live
    return False

def setBrightness(intensity):
    if available == False:
        return 2
    else:
        lockdown = False
        try:
            bus.write_block_data(arduinoAddress, 0x06, [intensity])
        except:
            errorMsg = sys.exec_info()[0]
            errorHandler(5, errorMsg)
    lockdown = True

def disableTimeout():
    if available == False:
        return 2
    else:
        lockdown = False
        try:
            bus.write_byte(arduinoAddress, 0x05)
        except:
            errorMsg = sys.exec_info()[0]
            errorHandler(5, errorMsg)
    lockdown = True

def blink(n, Red, Green, Blue):
    bus.write_block_data(arduinoAddress, 0x04, [Red, Green, Blue, n])
            
def setPixel(n, red, green, blue):
    """ Send values for changing pixel values """
    if available == False:
        return 2
    else:
        lockdown = False
        try:
            if n > 255:
                n1 = 255
                n2 = n - 255
            else:
                n1 = 0
                n2 = n
            #print("{", n1, n2, "}")
            bus.write_block_data(arduinoAddress, 0x02, [n1, n2, red, green, blue])
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    lockdown = True

def show():
    """ Send values for turning pixels on """
    if available == False:
        return 2
    else:
        lockdown = False
        try:
            bus.write_byte(arduinoAddress, 0x03)
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    lockdown = True
    
def blink(time, red, green, blue):
    """ Flash all pixels with a colour """
    if available == False:
        return 2
    else:
        lockdown = False
        try:
            bus.write_block_data(arduinoAddress, 0x04, [red, green, blue, time])
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    lockdown = True

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
