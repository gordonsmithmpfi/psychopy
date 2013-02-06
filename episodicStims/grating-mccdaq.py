from psychopy import visual, filters, event, core
import numpy, time
import UniversalLibrary as UL #DAQ stuff

#stim parameters
changeDirectionAt=1.1
stimDuration = 2.5
isi = 0.01 #not actually this short! ISI Controlled by triggering really.
stimContrast = 1.0
temporalFreq = 0.1
spatialFreq=0.005

#DAQ setup
BoardNum = 0
PortNum = UL.FIRSTPORTA
Direction = UL.DIGITALIN
UL.cbDConfigPort(BoardNum, PortNum, Direction)

#set up window and stim
win=visual.Window(size=(800,600),units="pix",screen=1)

grating = filters.makeGrating(256,cycles=1,gratType='sqr')#ranges-1 to 1 
texture = numpy.zeros([256,256,3]) 
#we need 1,-1,-1 at peak phase and 0,0,0 at trough phase 
texture[:,:,0] = grating*0.729-0.271#r 
texture[:,:,1] = grating*0.729-0.271#g 
texture[:,:,2] = grating*0.729-0.271#b 

blackTexture = -numpy.ones([256,256,3]) 

stim=visual.PatchStim(win, tex=texture,texRes=256,sf=spatialFreq, units='pix',size=(1280,1024),ori=45,mask='none') 
blankStim=visual.PatchStim(win, tex=blackTexture,texRes=256,sf=spatialFreq, units='pix',size=(1280,1024),ori=45,mask='none') 

stim.autoLog=False#or we'll get many messages about phase change
blankStim.autoLog=False#or we'll get many messages about phase change


while True:
    stim.contrast=stimContrast
    #read from DAQ to get stimcode for orientation
    
    stimcode = 0;
#    while stimcode > 128 or stimcode == 0:
    while stimcode > 64 or stimcode == 0:
        #keep trying until a valid stimcode appears
        stimcode = UL.cbDIn(BoardNum, PortNum, stimcode)
        
        #useful for debugging triggering
        #print 'Got stimcode ',stimcode
        #time.sleep(1)
        
    print 'Got stimcode ',stimcode

    if stimcode==9:
        stim.setAutoDraw(False)
        blankStim.setAutoDraw(True)
        print 'blank'
    else:
        stim.ori = -122.5+22.5*stimcode #change to lab standard coordinates
        blankStim.setAutoDraw(False)
        stim.setAutoDraw(True)
    
    clock = core.Clock()
    #draw a drifting grating
    while clock.getTime()<stimDuration:#clock times are in seconds
        if clock.getTime()>changeDirectionAt:
            stim.setPhase(temporalFreq, '-')#decrement by 10th of cycle
        else:
            stim.setPhase(temporalFreq, '+')#increment by 10th of cycle
        win.flip()#flip the screen

    #now a blank screen for ISI
    clock = core.Clock()
    while clock.getTime()<isi:
        stim.setAutoDraw(False)
        blankStim.setAutoDraw(True)
        stim.contrast = 0
        win.flip()
