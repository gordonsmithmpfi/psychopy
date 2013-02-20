from psychopy import visual, logging, core, filters, event
import pylab, math, random, numpy, serial, time, csv
import UniversalLibrary as UL

#trials and timing
path = 'c:/users/fitzlab1/exp001.txt'
expName = 'test001'
isi = 1
stimDuration = 1
numTrials = 1 #Run all the stims this many times
doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.

#grating parameters
orientations = numpy.arange(0.0,180,11.25) #Remember, ranges in Python do NOT include the final value!
spatialFreq = 0.2
contrast = 1.0
textureType = 'sqr' #'sqr' = square wave, 'sin' = sinusoidal

#aperture and position parameters
centerPoint = [0,0] 
stimSize = [500, 500] #Size of grating.

#trigger properties
useSerialTrigger = 1 #0 = display stims at will; 1 = display stims only when serial port trigger appears
sendToCED = 1 #0=don't send stimcodes to CED, 1=send stimcodes

#stim timing properties 
temporalFreq = 4

#DAQ setup
boardNum = 0
portNumA = UL.FIRSTPORTA
portNumB = UL.FIRSTPORTB
portDxn = UL.DIGITALOUT
UL.cbDConfigPort(boardNum, portNumA, portDxn)
UL.cbDConfigPort(boardNum,portNumB, portDxn)

#serial port info
ser = None
serialPortName = 'COM2'
if useSerialTrigger==1:
    ser = serial.Serial(serialPortName, 9600, timeout=0)

#CSV logging 
triggerTimes = []
stimCodes = []

def waitForSerial(ser):
    #wait for the next time a trigger appears on the serial port
    #Make sure to call ser.flushInput() on each flip so that the buffer will be clear before we reach here.
    bytes = ""
    while(bytes == ""):
        bytes = ser.read()
    
#make a window
myWin = visual.Window(monitor='testMonitor',size=(1920,1080),fullscr=True,screen=1)

#create grating stim
gratingStim = visual.PatchStim(win=myWin,tex=textureType,units='deg',pos=centerPoint,size=stimSize, sf=spatialFreq)

#figure out the time between frame triggers by recording 10 of them and determining the duration
if useSerialTrigger:
    print "Waiting for serial trigger on ", serialPortName, "."
    timer = core.Clock()
    offTime = None
    waitForSerial(ser)
    onTime = timer.getTime()
    for count in range(0,10):
        #Wait 15 msecs - this is because the serial triggers stay on for 10ms each, 
        #and we don't want to count a single trigger multiple times
        time.sleep(0.015)
        ser.flushInput()
        waitForSerial(ser)
    offTime = timer.getTime()
    frameTime = (offTime-onTime)/10
    print "frame triggers are ", frameTime, " seconds apart."
    #adjust stim duration to be some multiple of the frame time
    stimDurationInFrames = math.ceil(stimDuration / frameTime)
#    isiDurationInFrames = math.ceil(isi/frameTime)
#    isi = frameTime * isiDurationInFrames
    stimDuration = frameTime * stimDurationInFrames
    changeDirectionAt = stimDuration/2
    print "stim duration has been increased to ",stimDuration," seconds (",stimDurationInFrames," frames)."
    
#run
print "\n",str(len(orientations)+doBlank), "stims will be run for",str(numTrials),"trials."
timer2 = core.Clock()
for trial in range(0,numTrials):
    #determine stim order
    print "Beginning Trial",trial+1
    stimOrder = range(0,len(orientations)+doBlank)
    random.shuffle(stimOrder)
    for stimNumber in stimOrder:
        #display each stim
        if sendToCED:
            #send stimcode to CED via measurement computing
            UL.cbDOut(boardNum,portNumA,stimNumber+1)
            UL.cbDOut(boardNum,portNumB,1)
        #wait for 2pt frame trigger
        serialNeedsReset = 0
        if useSerialTrigger:
            waitForSerial(ser)
            triggerTimes.append([timer2.getTime()])
            stimCodes.append(stimNumber)
            
        if sendToCED:
            #this costs 1.2ms (+/- 0.1ms).
            UL.cbDOut(boardNum,portNumB,0)
            
        if stimNumber == len(orientations):
            #do blank
            print "\tStim",stimNumber+1, "(blank)"
            clock = core.Clock()
            while clock.getTime()<stimDuration+isi:
                gratingStim.setContrast(0)
                myWin.flip()
                if useSerialTrigger:
                    ser.flushInput() #clear serial input buffer after every flip
        else:
            #display stim
            print "\tStim",stimNumber+1
            gratingStim.ori = orientations[stimNumber]
            # convert orientations to standard lab notation
            gratingStim.setContrast(contrast)
            gratingStim.setAutoDraw(True)
            clock = core.Clock()
            while clock.getTime()<stimDuration:
                if clock.getTime()>changeDirectionAt:
                    gratingStim.setPhase(changeDirectionAt*temporalFreq - (clock.getTime()-changeDirectionAt)*temporalFreq)
                else:
                    gratingStim.setPhase(clock.getTime()*temporalFreq)
                myWin.flip()
                if useSerialTrigger:
                    ser.flushInput() #clear serial input buffer after every flip
            #now do ISI
            clock = core.Clock()
            while clock.getTime()<isi:
                gratingStim.setContrast(0)
                myWin.flip()
                if useSerialTrigger:
                    ser.flushInput() #clear serial input buffer after every flip

#Hazel is jigglypuff
with open(path, "a") as csvfile:
    w = csv.writer(csvfile, dialect = "excel")
    w.writerow([expName])
    w.writerow([path])
    w.writerow([stimCodes])
    if useSerialTrigger:
        w.writerow([triggerTimes])
        w.writerow([frameTime])
