from psychopy import visual, logging, core
import pylab, math, serial, numpy

#Write down your input parameters someplace! Right now there's no automated logging or anything. 

#input parameters 

#time parameters
duration = 60*2; #how long to run the stim for (seconds)
movementPeriod = 10; #how long it takes for a bar to move from startPoint to endPoint

#bar parameters
orientation = 0 #0 is horizontal, 90 is vertical. 45 goes from up-left to down-right.
barColor = 1 #1 for white, -1 for black, 0.5 for low contrast white, etc.

#position parameters
centerPoint = [0,-10] #center of screen is [0,0] (degrees).
startPoint = -25; #bar starts this far from centerPoint (in degrees)
endPoint = 25; #bar moves to this far from centerPoint (in degrees)
stimSize = (180,2) #First number is longer dimension no matter what the orientation is.

#flashing parameters
flashPeriod = 0.2 #amount of time it takes for a full cycle (on + off)
dutyCycle = 0.5 #Amount of time flash bar is "on" vs "off". 0.5 will be 50% of the time.

useSerialTrigger = 0 #0=run now, 1=wait for serial port trigger

#serial port info
#ser = serial.Serial('/dev/tty.pci-serial1', 9600, timeout=1) 
#if useSerialTrigger==1:
#    bytes = "1" 
#    while bytes: #burn up any old bits that might be lying around in the serial buffer
#        bytes = ser.read() 

#/dev/tty.pci-serial0, /dev/cu.pci-serial0, /dev/tty.pci-serial1, /dev/cu.pci-serial1, /dev/tty.Bluetooth-PDA-Sync, /dev/cu.Bluetooth-PDA-Sync, /dev/tty.Bluetooth-Modem,
#/dev/cu.Bluetooth-Modem.

#make a window
mywin = visual.Window(monitor='StimMonitor',size=(1920,1080),fullscr=True,screen=0)

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