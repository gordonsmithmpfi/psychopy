from psychopy import visual, logging, core, filters, event
import pylab, math, random, numpy, serial, time

#trials and timing
numTrials = 5 #Run all the stims this many times
doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDuration = 4
isi=3

#stim timing properties
flashFrequency = 4 #number of flashes per second
dutyCycle = 0.5 #Amount of time flash bar is "on" vs "off". 0.5 will be on 50% of the time.

#Stim properties. Numbers are in visual degrees. Check monitor center to make sure your screen distance is right.
shifts = [-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16] #bar position
contrast = -1 #1 for white bars, -1 for black bars, 0.5 for grayish
jitter = 0.5 #If jitter>0, bar will jitter on each frame of the animation. It will move by as much as (barWidth*jitter), randomly sampled.
orientation = 45 #0 is horizontal, 90 is vertical. 45 goes from up-left to down-right.

#aperture and position parameters
centerPoint = [20,0] 
stimSize = (1920,2) #Size of bar. First number is the longer dimension no matter what the orientation is.

#trigger properties
triggered = 1 #0 = display stims at will; 1 = display stims only when triggered
sendToCED = 1#0=don't send stimcodes to CED, 1=send stimcodes

#set up serial port
if triggered or sendToCED:
    arduino = serial.Serial('/dev/tty.usbmodem1a21', 9600, timeout=0)
    time.sleep(3) #need to sleep 3s to allow Arduino to initialize

#make a window
mywin = visual.Window(monitor='StimMonitor',size=(1920,1080),fullscr=True,screen=1)

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
        
        #wait for 2pt frame trigger
        if triggered:
            arduino.write('t')
            print "Waiting for trigger"
            while True:
                response = arduino.read()
                if len(response)>0:
                    break
            
        #send stimcode to CED via arduino on serial port
        if sendToCED:
            arduino.write('w' + str(stimNumber+1))
        
        if stimNumber == len(shifts):
            #do blank
            print "\tStim",stimNumber+1, "(blank)"
            clock = core.Clock()
            while clock.getTime()<stimDuration+isi:
                barStim.setContrast(0)
                mywin.flip()
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
                mywin.flip()
            #now do ISI
            clock = core.Clock()
            while clock.getTime()<isi:
                barStim.setContrast(0)
                mywin.flip()
