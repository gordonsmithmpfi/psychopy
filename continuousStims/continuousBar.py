from psychopy import visual, logging, core
import pylab, math, serial, numpy

#Write down your input parameters someplace! Right now there's no automated logging or anything. 

#input parameters 

#time parameters
duration = 60*20; #how long to run the stim for (seconds)
movementPeriod = 30; #how long it takes for a bar to move from startPoint to endPoint

#bar parameters
orientation = 90 #0 is horizontal, 90 is vertical. 45 goes from up-left to down-right.
barColor = -1 #1 for white, -1 for black, 0.5 for low contrast white, etc.

#position parameters
centerPoint = [0,0] #center of screen is [0,0] (degrees).
startPoint = -45; #bar starts this far from centerPoint (in degrees)
endPoint = 45; #bar moves to this far from centerPoint (in degrees)
stimSize = (180,4) #First number is longer dimension no matter what the orientation is.

#flashing parameters
flashPeriod = 0.2 #amount of time it takes for a full cycle (on + off)
dutyCycle = 0.8 #Amount of time flash bar is "on" vs "off". 0.5 will be 50% of the time.

useSerialTrigger = 0 #0=run now, 1=wait for serial port trigger

#serial port info
ser = None
if useSerialTrigger==1:
    ser = serial.Serial('/dev/tty.pci-serial1', 9600, timeout=1) 
    bytes = "1" 
    while bytes: #burn up any old bits that might be lying around in the serial buffer
        bytes = ser.read() 

#make a window
mywin = visual.Window(monitor='StimMonitor',fullscr=True,screen=1)

#create bar stim
barTexture = numpy.ones([256,256,3])*barColor;
barStim = visual.PatchStim(win=mywin,tex=barTexture,mask='none',units='deg',pos=centerPoint,size=stimSize,ori=orientation)
barStim.setAutoDraw(True)


#wait for serial
if useSerialTrigger==1:
    bytes = ""
    while(bytes == ""):
        bytes = ser.read(1)
        

#run
clock = core.Clock()
while clock.getTime()<duration:
    posLinear = (clock.getTime() % movementPeriod) / movementPeriod * (endPoint-startPoint) + startPoint; #what pos we are at in degrees
    if (clock.getTime()/flashPeriod) % (1.0) < dutyCycle:
        barStim.setContrast(1)
    else:
        barStim.setContrast(0)
    posX = posLinear*math.sin(orientation*math.pi/180)+centerPoint[0]
    posY = posLinear*math.cos(orientation*math.pi/180)+centerPoint[1]
    barStim.setPos([posX,posY])
    mywin.flip()