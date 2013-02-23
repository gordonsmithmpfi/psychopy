from psychopy import visual, logging, core, filters, event
import pylab, math, random, numpy, time, imp, sys
sys.path.append("../triggers") #path to trigger clases
import noTrigger, serialTriggerDaqOut #trigger imports

# ---------- Stimulus Description ---------- #
'''A static grating with a short display time for orientation tuning'''

# ---------- Stimulus Parameters ---------- #

#trials and duration
numTrials = 1 #Run all the stims this many times
doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDuration = 0.3
changeDirectionAt = stimDuration * 0.5 #In case the grating is moving, when do we change movement directions?
isi = 0

#grating parameters
orientations = numpy.arange(0.0,180,11.25) #Remember, ranges in Python do NOT include the final value!
temporalFreq = 0 #keep this at 0 for a static grating
spatialFreq = 0.2
contrast = 1.0
textureType = 'sqr' #'sqr' = square wave, 'sin' = sinusoidal

#aperture and position parameters
centerPoint = [0,0] 
stimSize = [500, 500] #Size of grating in degrees

#Triggering type
#Can be either:
# "NoTrigger" - no triggering; stim will run freely
# "SerialDaqOut" - Triggering by serial port. Stim codes are written to the MCC DAQ.
triggerType = "SerialDaqOut" 
serialPortName = 'COM7' # ignored if triggerType is "None"

#Experiment logging parameters
logFilePath = 'c:/users/fitzlab1/exp001.txt'
expName = 'test001'

# ---------- Stimulus code begins here ---------- #

#make a window
myWin = visual.Window(monitor='testMonitor',fullscr=True,screen=1)

#Set up the trigger behavior
trigger = None
if triggerType == "NoTrigger":
    trigger = noTrigger.noTrigger(None) 
elif triggerType == "SerialDaqOut":
    trigger = serialTriggerDaqOut.serialTriggerDaqOut(serialPortName) 
    #Record a bunch of serial triggers and fit the stim duration to an exact multiple of the trigger time
    stimDuration = trigger.extendStimDurationToFrameEnd(stimDuration)
    changeDirectionAt = stimDuration * 0.5
else:
    print "Unknown trigger type", triggerType

#create grating stim
gratingStim = visual.PatchStim(win=myWin,tex=textureType,units='deg',pos=centerPoint,size=stimSize, sf=spatialFreq)

#run
print "\n",str(len(orientations)+doBlank), "stims will be run for",str(numTrials),"trials."
for trial in range(0,numTrials):
    #determine stim order
    print "Beginning Trial",trial+1
    stimOrder = range(0,len(orientations)+doBlank)
    random.shuffle(stimOrder)
    for stimNumber in stimOrder:
        #display each stim
        trigger.preStim(stimNumber+1)
        
        if stimNumber == len(orientations):
            #do blank
            print "\tStim",stimNumber+1, "(blank)"
            clock = core.Clock()
            while clock.getTime()<stimDuration+isi:
                gratingStim.setContrast(0)
                trigger.preFlip(None)
                myWin.flip()
                trigger.postFlip(None)
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
                trigger.preFlip(None)
                myWin.flip()
                trigger.postFlip(None)
            #now do ISI
            clock = core.Clock()
            while clock.getTime()<isi:
                gratingStim.setContrast(0)
                trigger.preFlip(None)
                myWin.flip()
                trigger.postFlip(None)
        trigger.postStim(None)

trigger.wrapUp([logFilePath, expName])
