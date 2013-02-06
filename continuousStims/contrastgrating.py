from psychopy import visual, logging, core
import pylab, math, serial

#Write down your input parameters someplace! Right now there's no automated logging or anything. 

#input parameters
duration=60*10  #in seconds
temporalFreq=2
spatialFreq=0.08
spinPeriodInSeconds = 9999999
spinDirection = 1;

contrastPeriod = 10 #seconds

useSerialTrigger = 0 #0=run now, 1=wait for serial port trigger

#serial port info
ser = None
if useSerialTrigger==1:
    ser = serial.Serial('/dev/tty.pci-serial1', 9600, timeout=1) 
    bytes = "1" #burn up any old bits that might be lying around in the serial buffer
    while bytes:
        bytes = ser.read() 

#calculated parameters
spinDegreesPerSecond = 360 / spinPeriodInSeconds

#make a window
mywin = visual.Window(monitor='StimMonitor',fullscr=True,screen=1)

#create grating
stim1 = visual.PatchStim(win=mywin,tex='sin',mask='none',units='deg',pos=(0,0),size=(200,200), sf=spatialFreq)
stim1.setAutoDraw(True)

#wait for serial
if useSerialTrigger==1:
    bytes = ""
    while(bytes == ""):
        bytes = ser.read(1)
        

#run
clock = core.Clock()
while clock.getTime()<duration:        
        newPhase = clock.getTime()*temporalFreq
        newOri = spinDirection*clock.getTime()*spinDegreesPerSecond-90
        stim1.setPhase(newPhase)
        stim1.setOri(newOri)
        contrastPhase = math.sin(clock.getTime() *3.14159 / 10) /2 + 0.5
        stim1.setContrast(contrastPhase)
        mywin.flip()

print clock.getTime()
        