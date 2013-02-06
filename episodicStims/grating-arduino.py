from psychopy import visual, logging, core, filters, event
import pylab, math, random, numpy, serial, time

#trials and timing
stimDuration = 3
isi = 2.0
numTrials = 5 #Run all the stims this many times
doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.

#stim timing properties
temporalFreq = 4
changeDirectionAt=stimDuration / 2 #When will the grating reverse directions? Set equal to stimDuration for single direction, or stimDuration/2 for bidirectional.

#grating parameters
orientations = numpy.arange(0.0,180,22.5) #Remember, ranges in Python do NOT include the final value!
spatialFreq = 0.2
contrast = 1.0
textureType = 'sqr' #'sqr' = square wave, 'sin' = sinusoidal

#aperture and position parameters
centerPoint = [0,0] 
stimSize = [500, 500] #Size of grating. Right now only full screen works well.

#trigger properties
triggered = 1 #0 = display stims at will; 1 = display stims only when triggered (low->high)
sendToCED = 1#0=don't send stimcodes to CED, 1=send stimcodes
doFrameTriggers = 1 #0=don't send post-flip triggers to CED, 1=send post-flip triggers

#set up serial port
if triggered or sendToCED or doFrameTriggers:
    arduino = serial.Serial('/dev/tty.usbmodem1a21', 9600, timeout=0)
    time.sleep(3)

#make a window
mywin = visual.Window(monitor='StimMonitor',size=(1920,1080),fullscr=True,screen=1)

#create grating stim
gratingStim = visual.PatchStim(win=mywin,tex=textureType,units='deg',pos=centerPoint,size=stimSize, sf=spatialFreq)

#run
print "\n",str(len(orientations)+doBlank), "stims will be run for",str(numTrials),"trials."
for trial in range(0,numTrials):
    #determine stim order
    print "Beginning Trial",trial+1
    stimOrder = range(0,len(orientations)+doBlank)
    random.shuffle(stimOrder)

    for stimNumber in stimOrder:
        #display each stim
        
        #wait for 2pt frame trigger
        if triggered:
            arduino.write('t')
            print "Waiting for trigger"
            response = ''
            while len(response)==0:
                response = arduino.readline()
            
        #send stimcode to CED via arduino on serial port
        if sendToCED:
            arduino.write('w' + str(stimNumber+1))
        
        if stimNumber == len(orientations):
            #do blank
            print "\tStim",stimNumber+1, "(blank)"
            clock = core.Clock()
            while clock.getTime()<stimDuration+isi:
                gratingStim.setContrast(0)
                mywin.flip()
        else:
            #display stim
            print "\tStim",stimNumber+1
            gratingStim.ori = orientations[stimNumber] + 90
            gratingStim.setContrast(contrast)
            gratingStim.setAutoDraw(True)
            clock = core.Clock()
            while clock.getTime()<stimDuration:
                if clock.getTime()>changeDirectionAt:
                    gratingStim.setPhase(changeDirectionAt*temporalFreq - (clock.getTime()-changeDirectionAt)*temporalFreq)
                else:
                    gratingStim.setPhase(clock.getTime()*temporalFreq)
                mywin.flip()

            #now do ISI
            clock = core.Clock()
            while clock.getTime()<isi:
                gratingStim.setContrast(0)
                mywin.flip()
