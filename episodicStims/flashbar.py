from psychopy import visual, logging, core
import pylab, math, random, numpy, serial, imp
import UniversalLibrary as UL #The Measurement Computing DAQ library

#import the triggering class we'll be using
triggeringCode = '../triggers/examples/importTest.py' 
trigger = getattr(imp.load_source('', triggeringCode),  'trigger')() 


#trials and timing
stimDuration = 1
isi=1
flashFrequency = 2 #number of flashes per second
numTrials = 5
sendStimcodes = 0 #do we want to send stimcodes via the MCC DAQ?

#position etc. Numbers are in degrees.
orientation = 0 #0 is horizontal, 90 is vertical. 45 goes from up-left to down-right.
barColor = 1 #1 for white, 0 for black, 0.5 for gray
shifts = [-8,-4,0,4,8]
dutyCycle = 0.5 #Amount of time flash bar is "on" vs "off". 0.5 will be 50% of the time.
centerPoint = [0,0] 
stimSize = (60,0.5) #First number is longer dimension no matter what the orientation is.

#code starts here
#make a window
mywin = visual.Window(monitor='StimMonitor',fullscr=True,screen=1)

#create bar and ISI textures
barTexture = numpy.ones([256,256,3]);
barStim = visual.PatchStim(win=mywin,tex=barTexture,mask='none',units='deg',pos=centerPoint,size=stimSize,ori=orientation)

#Set up DAQ to send messages through its first port
if sendStimcodes:
    BoardNum = 0
    PortNum = UL.FIRSTPORTA
    Direction = UL.DIGITALOUT
    UL.cbDConfigPort(BoardNum, PortNum, Direction)


#run
for trial in range(0,numTrials):
    #determine stim order
    print "Beginning Trial",trial+1
    stimOrder = range(0,len(shifts))
    random.shuffle(stimOrder)
    for stimNumber in stimOrder:
        #display each stim
        print "\tStim",stimNumber+1
        trigger.preStim()
        
        #write stimcode to MCC-DAQ
        if sendStimcodes:
            UL.cbDOut(BoardNum, PortNum, stimNumber+1)
        
        barStim.setPos([shifts[stimNumber]*math.sin(orientation*math.pi/180) + centerPoint[0] ,shifts[stimNumber]*math.cos(orientation*math.pi/180)  + centerPoint[1]])
        barStim.setAutoDraw(True)
        clock = core.Clock()
        while clock.getTime()<stimDuration:
            if (clock.getTime()*flashFrequency) % (1.0) < dutyCycle:
                barStim.setContrast(1)
            else:
                barStim.setContrast(0)
            trigger.preFlip()
            mywin.flip()
            trigger.postFlip()
        #now do ISI
        clock = core.Clock()
        while clock.getTime()<isi:
            barStim.setContrast(0)
            mywin.flip()
            
        trigger.postStim()
trigger.wrapUp()