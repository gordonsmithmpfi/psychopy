from psychopy import visual, logging, core, filters, event
import pylab, math, random, numpy, serial, time, sys
sys.path.append("../triggers") #path to trigger clases
import noTrigger, serialTrigger #trigger imports

# ---------- Stimulus Description ---------- #
''' A flashing, jittering bar for azimuth and elevation mapping'''

# ---------- Stimulus Parameters ---------- #

#trials and timing
numTrials = 5 #Run all the stims this many times
doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDuration = 4
isi=2

#stim timing properties
flashFrequency = 4 #number of flashes per second
dutyCycle = 0.5 #Amount of time flash bar is "on" vs "off". 0.5 will be on 50% of the time.

#aperture and position parameters.  Numbers are in visual degrees.
centerPoint = [20,0] 
stimSize = (1920,2) #Size of bar. First number is the longer dimension no matter what the orientation is.

#Stim properties. Check monitor center to make sure your screen distance is correct.
shifts = range(-16,18,2) # bar positions. Remember, ranges in python do not include the upper bound!
contrast = -1 #1 for white bars, -1 for black bars, 0.5 for grayish
jitter = 0.5 #If jitter > 0, bar will jitter on each frame of the animation. It will move by as much as (barWidth*jitter), randomly sampled.
orientation = 45 #0 is horizontal, 90 is vertical. 45 goes from up-left to down-right.

#Triggering type
#Can be either:
# "NoTrigger" - no triggering; stim will run freely
# "SerialDaqOut" - Triggering by serial port. Stim codes are written to the MCC DAQ.
triggerType = "NoTrigger" 
serialPortName = 'COM2' # ignored if triggerType is "None"

# ---------- Stimulus code begins here ---------- #


print "\nDisplaying bar positions: ",shifts, "(", len(shifts),"different positions)"
numStims = len(shifts)
if doBlank:
    numStims = numStims + 1
print numStims,"stimuli will be displayed for",numTrials,"trials.\n"

#make a window
mywin = visual.Window(monitor='StimMonitor',fullscr=True,screen=1)

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

#create bar texture and stim
barTexture = numpy.ones([256,256,3]);
barStim = visual.PatchStim(win=mywin,tex=barTexture,mask='none',units='deg',pos=centerPoint,size=stimSize,ori=orientation)

#run
for trial in range(0,numTrials):
    #determine stim order
    print "Beginning Trial",trial+1
    stimOrder = range(0,len(shifts)+doBlank)
    random.shuffle(stimOrder)
    
    for stimNumber in stimOrder:
        #display each stim
        trigger.preStim(stimNumber)
            
        if stimNumber == len(shifts):
            #do blank
            print "\tStim",stimNumber+1, "(blank)"
            clock = core.Clock()
            while clock.getTime()<stimDuration+isi:
                barStim.setContrast(0)
                trigger.preFlip(None)
                mywin.flip()
                trigger.postFlip(None)
        else:
            #display stim
            print "\tStim",stimNumber+1
            barPosX = shifts[stimNumber]*math.sin(orientation*math.pi/180) + centerPoint[0]
            barPosY = shifts[stimNumber]*math.cos(orientation*math.pi/180)  + centerPoint[1]
            barStim.setPos([barPosX,barPosY])
            barStim.setAutoDraw(True)
            clock = core.Clock()
            while clock.getTime()<stimDuration:
                if (clock.getTime()*flashFrequency) % (1.0) < dutyCycle:
                    barStim.setContrast(contrast)
                else:
                    barStim.setContrast(0)
                if jitter>0:
                    displacement = (random.random()*2-1)*jitter
                    barStim.setPos([barPosX+displacement*math.sin(orientation*math.pi/180),barPosY+displacement*math.cos(orientation*math.pi/180)])
                trigger.preFlip(None)
                mywin.flip()
                trigger.postFlip(None)
            #now do ISI
            clock = core.Clock()
            while clock.getTime()<isi:
                barStim.setContrast(0)
                trigger.preFlip(None)
                mywin.flip()
                trigger.postFlip(None)
        trigger.postStim(None)

trigger.wrapUp(None)