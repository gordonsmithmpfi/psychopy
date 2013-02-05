from psychopy import visual, filters, event, core
import numpy 
import UniversalLibrary as UL #DAQ stuff

#stim parameters
changeDirectionAt=1
stimDuration = 2
isi = 3
stimContrast = 1.0
temporalFreq = 0.01

#DAQ setup
BoardNum = 0
PortNum = UL.FIRSTPORTA
Direction = UL.DIGITALIN
UL.cbDConfigPort(BoardNum, PortNum, Direction)

#set up window and stim
win=visual.Window(size=(1920,1080),units="pix",screen=1, fullscr=True)

grating = filters.makeGrating(256,cycles=1,gratType='sqr')#ranges-1 to 1 
texture = numpy.zeros([256,256,3]) 
#we need 1,-1,-1 at peak phase and 0,0,0 at trough phase 
texture[:,:,0] = grating*0.729-0.271#r 
texture[:,:,1] = grating*0.729-0.271#g 
texture[:,:,2] = grating*0.729-0.271#b 

blackTexture = -numpy.ones([256,256,3]) 

stim=visual.PatchStim(win, tex=texture,texRes=256,sf=0.005, units='pix',size=(1280,1024),ori=45,mask='none') 
blankStim=visual.PatchStim(win, tex=blackTexture,texRes=256,sf=0.005, units='pix',size=(1280,1024),ori=45,mask='none') 
