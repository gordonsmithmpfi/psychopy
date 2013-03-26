# Triggers when data arrives at the serial port.
# Sends stimcodes via Measurement Computing DAQ.
import serial, csv, time, math, datetime
from psychopy import core
import UniversalLibrary as UL
from abstractTrigger import trigger

class serialTriggerDaqOut(trigger):
    
    def __init__(self, args):
        #serial port setup
        self.boardNum = 0
        self.serialPortName = args
        self.ser = serial.Serial(self.serialPortName, 9600, timeout=0)
        self.basestate=1; # what is baseline state? 1 if stimtrig is high to low, 0 if low to high
        self.readSer=True; # if false, it will trigger immediately, but will still log data
        
        #DAQ setup        
        UL.cbDConfigPort(self.boardNum, UL.FIRSTPORTA, UL.DIGITALOUT)
        UL.cbDConfigPort(self.boardNum,UL.FIRSTPORTB, UL.DIGITALOUT)
        self.needToSendStimcode = False
            
        #CSV logging setup
        self.timer = core.Clock()
        self.triggerTimes = []
        self.stimCodes = []
        self.dateTime = datetime.datetime.now()
    
    # standard pre / post functions
    def preStim(self, args):
        stimNumber = args
        
        #record the stim number we're about to display
        self.stimCodes.append(stimNumber)
            
        #send stimcode to CED via measurement computing
        UL.cbDOut(self.boardNum,UL.FIRSTPORTA,stimNumber)
        UL.cbDOut(self.boardNum,UL.FIRSTPORTB,self.basestate)

        #wait for 2pt frame trigger
        if self.readSer:
            self.waitForSerial()
        
        #Tell ourselves to send the signal the CED as soon as we flip
        self.needToSendStimcode = True

    def postStim(self, args):
        pass

    def preFlip(self, args):
        UL.cbDOut(self.boardNum,UL.FIRSTPORTB,self.basestate)#return to base state


    def postFlip(self, args):                
        if self.needToSendStimcode:
            #record the time at the first flip
            self.triggerTimes.append(self.timer.getTime())
            #Tell CED to read stimcode
            #this costs 1.2ms (+/- 0.1ms).
            UL.cbDOut(self.boardNum,UL.FIRSTPORTB,0)
            #Only need to do this once per stim
            self.needToSendStimcode = False
        UL.cbDOut(self.boardNum,UL.FIRSTPORTB,self.basestate+2) # this should be an every frame trigger
            
    
    def wrapUp(self, args):
        logFilePath = args[0]
        expName = args[1]
        with open(logFilePath, "a") as csvfile:
            w = csv.writer(csvfile, dialect = "excel")
            w.writerow(["==========="])
            w.writerow([expName])
            w.writerow([self.dateTime])
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
        if self.readSer:
            #find how often we receive triggers
            frameTime = self.getTimeBetweenTriggers()
            #adjust stim duration to be some multiple of the frame time
            stimDurationInFrames = math.ceil(stimDuration / frameTime)
            stimDuration = frameTime * stimDurationInFrames
            print "stim duration has been increased to ",stimDuration," seconds (",stimDurationInFrames," frames)." 
        return stimDuration
       
      
#     def preTrialLogging(self, args)
#
#     dataDirName=args[2]
#     animalName=args[3]
#     testName=args[4]
#     # write the dirname and expname for spike2
#     f=open(datapath+'experimentname.txt','w')
#     f.write(animalName)
#     f.close()
#     f=open(datapath+'instruction.txt','w')
#     f.write(testName)
#     f.close()
#     # write the reference file, vht style
#     f=open(datapath+animalName+testName+'reference.txt','w')
#     f.write('name\tref\ttype\ntp\t'+str(1)+'\tprairietp')
#     f.close()
#     # now write the stim parameters
#     
#     
#     
#     # how best to write: really want header row, then values.
#     ; fprintf(fid,'%s',expname); fclose(fid);
#fid = fopen([datapath filesep 'instruction.txt'],'wt'); fprintf(fid,'%s',dirname); fclose(fid);
#     
#    
#        logFilePath = args[0]
#        expName = args[1]
#        with open(logFilePath, "a") as csvfile:
#            w = csv.writer(csvfile, dialect = "excel")
#            w.writerow(["==========="])
#            w.writerow([expName])
#            w.writerow([self.dateTime])
#            w.writerow([logFilePath])
#            w.writerow([self.stimCodes])
#            w.writerow([self.triggerTimes])
 