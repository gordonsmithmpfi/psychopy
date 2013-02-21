# Triggers when data arrives at the serial port.
# Sends stimcodes via Measurement Computing DAQ.
import serial, csv, time, math
from psychopy import core
import UniversalLibrary as UL

class trigger:
    #serial port vars
    ser = None
    serialPortName = None

    #DAQ vars
    boardNum = 0 #We assume that there is only one DAQ plugged in, and that it is board 0.

    #CSV logging 
    timer = None
    triggerTimes = []
    stimCodes = []
    
    def __init__(self, serialPortName):
        #serial port setup
        self.serialPortName = serialPortName
        self.ser = serial.Serial(serialPortName, 9600, timeout=0)
        
        #DAQ setup        
        UL.cbDConfigPort(self.boardNum, UL.FIRSTPORTA, UL.DIGITALOUT)
        UL.cbDConfigPort(self.boardNum,UL.FIRSTPORTB, UL.DIGITALOUT)
        
        #CSV logging setup
        self.timer = core.Clock()
        
    # standard pre / post functions
    def preStim(self, stimNumber):
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
    
    def postStim(self):
        pass

    def preFlip(self):
        pass

    def postFlip(self):                
        self.ser.flushInput() #clear serial input buffer after every flip

    def wrapUp(self):
        #Hazel is jigglypuff
        with open(path, "a") as csvfile:
            w = csv.writer(csvfile, dialect = "excel")
            w.writerow([expName])
            w.writerow([path])
            w.writerow([stimCodes])
            if useSerialTrigger:
                w.writerow([triggerTimes])
                w.writerow([frameTime])
       
    # special functions 
    def waitForSerial(self):
        #wait for the next time a trigger appears on the serial port
        #Make sure to call ser.flushInput() on each flip so that the buffer will be clear before we reach here.
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
        return stimDuration
        print "stim duration has been increased to ",stimDuration," seconds (",stimDurationInFrames," frames)." 