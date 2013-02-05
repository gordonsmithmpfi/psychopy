from psychopy import visual, logging, core
import pylab, math

#make a window
mywin = visual.Window(monitor='StimMonitor',size=(1920,1080),fullscr=False,screen=1)

#create two gratings
stim1 = visual.PatchStim(win=mywin,tex='sin',mask='none',units='deg',pos=(0,0),size=(4,4), sf=2)
stim2 = visual.PatchStim(win=mywin,tex='sqr',mask='gauss',units='deg',pos=(6,0),size=(5,5), sf=1, ori=90)
stim1.setAutoDraw(True)
stim2.setAutoDraw(True)

#run for 6 seconds at temporal frequency 4
duration=6
temporalFreq=4

clock = core.Clock()
while clock.getTime()<duration:
        stim1.setPhase(clock.getTime()*temporalFreq)
        stim2.setPhase(clock.getTime()*temporalFreq)
        mywin.flip()
