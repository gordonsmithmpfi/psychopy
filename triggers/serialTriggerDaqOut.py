# Triggers when data arrives at the serial port.
# Sends stimcodes via Measurement Computing DAQ.
import serial, csv, time, math
from psychopy import core
import UniversalLibrary as UL
from abstractTrigger import trigger

class serialTriggerDaqOut(trigger):
    #serial port vars
    ser = None
    serialPortName = None

    #DAQ vars
    boardNum = 0 #We assume that there is only one DAQ plugged in, and that it is board 0.

    #CSV logging 
    timer = None
    triggerTimes = []
    stimCodes = []
    
    def __init__(self, args):
        #serial port setup
        self.serialPortName = args
        self.ser = serial.Serial(self.serialPortName, 9600, timeout=0)
        
        #DAQ setup        
        UL.cbDConfigPort(self.boardNum, UL.FIRSTPORTA, UL.DIGITALOUT)
        UL.cbDConfigPort(self.boardNum,UL.FIRSTPORTB, UL.DIGITALOUT)
        
        #CSV logging setup
        self.timer = core.Clock()
        
    # standard pre / post functions
    def preStim(self, args):
        stimNumber = args
        #send stimcode to CED via measurement computing
        UL.cbDOut(self.boardNum,UL.FIRSTPORTA,stimNumber)
        UL.cbDOut(self.boardNum,UL.FIRSTPORTB,1)

        #wait for 2pt frame trigger
        self.waitForSerial()
        self.triggerTimes.append(self.timer.getTime())
        self.stimCodes.append(stimNumber)
        
        #Tell CED to read stimcode
        #this costs 1.2ms (+/- 0.1ms).
        UL.cbDOut(self.boardNum,UL.FIRSTPORTB,0)
    
    def postStim(self, args):
        pass

    def preFlip(self, args):
        pass

    def postFlip(self, args):                
        self.ser.flushInput() #clear serial input buffer after every flip

    def wrapUp(self, args):
        logFilePath = args[0]
        expName = args[1]
        with open(logFilePath, "a") as csvfile:
            w = csv.writer(csvfile, dialect = "excel")
            w.writerow([expName])
            w.writerow([logFilePath])
            w.writerow([self.stimCodes])
            w.writerow([self.triggerTimes])
       
    # additional functions 
    def waitForSerial(self):
        #wait for the next time a trigger appears on the serial port
        #Make sure to call ser.flushInput() so that the buffer will be clear before we reach here.
        bytes = ""
        self.ser.flushInput()
        while(bytes == ""):
            bytes = self.ser.read()
        
    def getTimeBetweenTriggers(self):
        print "Waiting for serial trigger on ", self.serialPortName, "."
        timer = core.Clock()
        offTime = None
        self.waitForSerial()
        onTime = timer.getTime()
        for count in range(0,10):
            #Wait 15 msecs - this is because the serial triggers stay on for 10ms each, 
            #and we don't want to count a single trigger multiple times
            time.sleep(0.015)
            self.waitForSerial()
        offTime = timer.getTime()
        frameTime = (offTime-onTime)/10
        print "frame triggers are ", frameTime, " seconds apart." 
        return frameTime
    
    def extendStimDurationToFrameEnd(self, stimDuration):
        #find how often we receive triggers
        frameTime = self.getTimeBetweenTriggers()
        #adjust stim duration to be some multiple of the frame time
        stimDurationInFrames = math.ceil(stimDuration / frameTime)
        stimDuration = frameTime * stimDurationInFrames
        print "stim duration has been increased to ",stimDuration," seconds (",stimDurationInFrames," frames)." 
        return stimDuration