from psychopy import visual, filters, event, core
import numpy, time, random, sys
sys.path.append("../triggers") #path to trigger clases
import noTrigger, daqTrigger #trigger imports

# ---------- Stimulus Description ---------- #
'''
This is a grating stimulus that is projected onto the cortex in blue light via the spatial light modulator (SLM).
It demonstrates how to use a custom texture stimulus.
'''

# ---------- Stimulus Parameters ---------- #

#stim parameters
stimDuration = 2.5
changeDirectionAt=stimDuration/2
isi = 3 #ISI will be ignored if stim is triggered
stimContrast = 1.0
temporalFreq = 0.04
spatialFreq=0.005


#Triggering type
#Can be either:
# "NoTrigger" - no triggering; stim will run freely
# "DaqTrigger" - Triggering by MCC DAQ. Stimcodes arrive via DAQ and the appropriate stim is displayed.
triggerType = "NoTrigger" 
serialPortName = 'COM7' # ignored if triggerType is "None"

# ---------- Stimulus code begins here ---------- #

#set up window and stim
win=visual.Window(fullscr=True,screen=1)

#Set up the trigger behavior
trigger = None
if triggerType == "NoTrigger":
    trigger = noTrigger.noTrigger(None) 
elif triggerType == "DaqTrigger":
    trigger = daqTrigger.daqTrigger(None) 
else:
    print "Unknown trigger type", triggerType

grating = filters.makeGrating(256,cycles=1,gratType='sqr')#ranges-1 to 1 
texture = numpy.zeros([256,256,3]) 
#we need 1,-1,-1 at peak phase and 0,0,0 at trough phase 
texture[:,:,0] = grating*0.729-0.271#r 
texture[:,:,1] = grating*0.729-0.271#g 
texture[:,:,2] = grating*0.729-0.271#b 

blackTexture = -numpy.ones([256,256,3]) 

stim=visual.PatchStim(win, tex=texture,texRes=256,sf=spatialFreq, units='pix',size=(1280,1024),ori=45,mask='none') 
blankStim=visual.PatchStim(win, tex=blackTexture,texRes=256,sf=spatialFreq, units='pix',size=(1280,1024),ori=45,mask='none') 

#stim.autoLog=False#or we'll get many messages about phase change
#blankStim.autoLog=False#or we'll get many messages about phase change

stimcodes = range(1,10) #remember, ranges in python do not include the final number
random.shuffle(stimcodes)
stimpos = 0
trialNum = 1

while True:
    #get stimcode
    stimcode = trigger.preStim(None)
    
    if stimcode == None:
        #this means we're using some triggering method that doesn't tell us stimcodes, so we need to randomly generate them.
        if stimpos == len(stimcodes):
            #reshuffle stimcodes for the next trial
            stimpos = 0
            random.shuffle(stimcodes)
            trialNum += 1
        stimcode = stimcodes[stimpos]
        print 'Showing stimcode ',stimcode, " in trial ", trialNum
        stimpos += 1
    stim.contrast=stimContrast
    
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
        trigger.preFlip(None)
        win.flip()#flip the screen
        trigger.postFlip(None)

    #now a blank screen for ISI
    clock = core.Clock()
    while clock.getTime()<isi:
        stim.setAutoDraw(False)
        blankStim.setAutoDraw(True)
        stim.contrast = 0
        trigger.preFlip(None)
        win.flip()
        trigger.postFlip(None)
    trigger.postStim(None)
    
trigger.wrapUp()