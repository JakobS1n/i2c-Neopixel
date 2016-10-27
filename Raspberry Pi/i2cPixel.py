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

def lockBus():
    lockdown = True
    
def unlockBus():
    lockdown = False

def available():
    global lockdown
    if lockdown == True:
        return False
    elif lockdown == False:
        return True
    else:
        return False

def setAddress(address):
    global arduinoAddress
    arduinoAddress = address

def setBus(n):
    if not available:
        return 2
    else:
        lockBus()
        global bus
        try:
            bus = smbus.SMBus(n)
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    unlockBus()
    
def greeting():
    if not available:
        return 2
    else:
        lockBus()
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
    unlockBus()

def ping():
    # Send 0x02 vil faa tilbake 42 hvis live
    return False

def setBrightness(intensity):
    if not available:
        return 2
    else:
        lockBus()
        try:
            if intensity > 255:
                n1 = 255
                n2 = n - 255
            else:
                n1 = 0
                n2 = intensity
                
            bus.write_block_data(arduinoAddress, 0x03, [n1, n2])
        except:
            errorMsg = sys.exec_info()[0]
            errorHandler(5, errorMsg)
    unlockBus()
    
def setPixel(n, red, green, blue):
    """ Send values for changing pixel values """
    if not available:
        return 2
    else:
        lockBus()
        try:
            if n > 255:
                n1 = 255
                n2 = n - 255
            else:
                n1 = 0
                n2 = n
            bus.write_block_data(arduinoAddress, 0x04, [n1, n2, red, green, blue])
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    unlockBus()

def blink(time, red, green, blue):
    """ Flash all pixels with a colour """
    if not available:
        return 2
    else:
        lockBus()
        try:
            bus.write_block_data(arduinoAddress, 0x05, [red, green, blue, time])
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    unlockBus()
    
            
def show():
    """ Send values for turning pixels on """
    if not available:
        return 2
    else:
        lockBus()
        try:
            bus.write_byte(arduinoAddress, 0x06)
        except:
            errorMsg = sys.exc_info()[0]
            errorHandler(5, errorMsg)
    unlockBus()
    
def disableTimeout():
    if not available:
        return 2
    else:
        lockBus()
        try:
            bus.write_byte(arduinoAddress, 0x07)
        except:
            errorMsg = sys.exec_info()[0]
            errorHandler(5, errorMsg)
    unlockBus()

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

     
def HEX(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))