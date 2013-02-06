from psychopy import visual, logging, core
import pylab, math, serial

#input parameters
duration=120 #in seconds
temporalFreq=4
spatialFreq=0.5
spinPeriodInSeconds = 30

#serial port info
useSerialTrigger = 0 #set to 1 to enable serial port triggering
#ser = serial.Serial('COM10', 9600, timeout=1) 

#calculated parameters
spinDegreesPerSecond = 360 / spinPeriodInSeconds

#make a window
mywin = visual.Window(monitor='StimMonitor',size=(1920,1080),fullscr=False,screen=1)

#create grating
stim1 = visual.PatchStim(win=mywin,tex='sqr',mask='gauss',units='deg',pos=(0,0),size=(10,10), sf=spatialFreq)
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
        newOri = clock.getTime()*spinDegreesPerSecond
        stim1.setPhase(newPhase)
        stim1.setOri(newOri)
        mywin.flip()
