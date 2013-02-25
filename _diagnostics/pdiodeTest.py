from psychopy import visual, logging, core
import pylab, math, numpy

# If you are having frame drops, try running this on a set of monitors that are
# *exactly* the same hardware. Mixing different monitor brands, even stuff with the same specs,
# caused frame drops in my testing. Once all the monitors were identical, frame drops went 
# down to 0.

mywin = visual.Window([1920,1080], fullscr=True,screen=1)
mywin.setRecordFrameIntervals(True)
mywin._refreshThreshold=1/120.0+0.004 #i've got 120Hz monitor and want to allow 4ms tolerance

#set the log module to report warnings to the std output window (default is errors only)
logging.console.setLevel(logging.WARNING)

#create some stimuli
barTexture = numpy.ones([256,256,3]);
stim1 =visual.PatchStim(win=mywin,tex=barTexture,mask='none',units='pix',pos=[-920,500],size=(100,100))
stim1.setAutoDraw(True)

clock = core.Clock()
while clock.getTime()<100:
    #stim1.setContrast(-1)
    stim1.setPos([-920,500])
    mywin.flip()#flip the screen. This will block until the monitor is ready for the flip.
    #stim1.setContrast(1)
    stim1.setPos([-920,0])
    mywin.flip()#flip the screen. This will block until the monitor is ready for the flip.

pylab.plot(mywin.frameIntervals)
pylab.show()
