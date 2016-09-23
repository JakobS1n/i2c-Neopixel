import smbus
import time

def version():
    print "i2cPixel is Version 1.0.0"

def setAddress(address):
    global arduinoAddress
    arduinoAddress = address

def setBus(n):
    global bus
    bus = smbus.SMBus(n)

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
        returnMsg = False
    """ Return if heartbeat was received """        
    return returnMsg

def setPixel(n, red, green, blue):
    """ Send values for switching a pixel on """
    bus.write_block_data(arduinoAddress, 0x02, [n, red, green, blue])

def show():
    bus.write_byte(arduinoAddress, 0x03)

def waitForSensor():

    while True:
        try:
            sensorData = bus.read_byte(arduinoAddress)
            if sensorData == 0x02:
                print "SENSOR 1"
                break;
            if sensorData == 0x03:
                print "SENSOR 2"
                break;
        except Exception:
            pass
