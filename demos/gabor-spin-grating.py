from psychopy import visual, logging, core
import pylab, math, serial

#input parameters
duration=10 #in seconds
temporalFreq=4
spatialFreq=0.5
spinPeriodInSeconds = 30

#calculated parameters
spinDegreesPerSecond = 360 / spinPeriodInSeconds

#make a window
mywin = visual.Window(monitor='StimMonitor',fullscr=True,screen=1)

#create grating
stim1 = visual.PatchStim(win=mywin,tex='sqr',mask='gauss',units='deg',pos=(0,0),size=(10,10), sf=spatialFreq)
stim1.setAutoDraw(True)

#run
clock = core.Clock()
while clock.getTime()<duration:
        newPhase = clock.getTime()*temporalFreq
        newOri = clock.getTime()*spinDegreesPerSecond
        stim1.setPhase(newPhase)
        stim1.setOri(newOri)
        mywin.flip()
