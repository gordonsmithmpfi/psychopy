from psychopy import visual, logging, core
import pylab, math, serial

#input parameters
duration=120 #in seconds
temporalFreq=4
spatialFreq=0.05
spinPeriodInSeconds = 30

#serial port info
useSerialTrigger = 0 #set to 1 to enable serial port triggering

#calculated parameters
spinDegreesPerSecond = 360 / spinPeriodInSeconds

#make a window
mywin = visual.Window(monitor='StimMonitor',size=(1920,1080),fullscr=True,screen=0)

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
        newOri = clock.getTime()*spinDegreesPerSecond
        stim1.setPhase(newPhase)
        stim1.setOri(newOri)
        mywin.flip()
