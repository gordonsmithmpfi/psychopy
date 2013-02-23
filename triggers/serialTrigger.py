# Triggers when data arrives at the serial port.
# Does not send stimcodes.
import serial
from abstractTrigger import trigger

class serialTrigger(trigger):
    #serial port vars
    ser = None
    serialPortName = None

    def __init__(self, args):
        self.serialPortName = args
        self.ser = serial.Serial(self.serialPortName, 9600, timeout=0)
        
    def preStim(self, args):
        self.waitForSerial()

    def postStim(self, args):
        pass

    def preFlip(self, args):
        pass

    def postFlip(self, args):
        pass

    def wrapUp(self, args):
        pass

    # additional functions 
    def waitForSerial(self):
        #wait for the next time a trigger appears on the serial port
        #Make sure to call ser.flushInput() so that the buffer will be clear before we reach here.
        bytes = ""
        self.ser.flushInput()
        while(bytes == ""):
            bytes = self.ser.read()