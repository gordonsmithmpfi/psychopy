#!/usr/bin/env python
from psychopy import visual, core, event, misc, logging, gui
import csv
count = 0
# In GUI, use 1 for Gabor, 2 for noise, 3 for bar
info= {'stimType':1, 'logPath':'c:/users/fitzlab1/documents/', 'expName':'exp001.txt'}
# logging not implemented yet
infoDlg = gui.DlgFromDict(dictionary=info, title='Experiment Parameters')
increment = 0.5
#create a window to draw in
myWin = visual.Window(monitor='stimMonitor',
    size=(1920,1080),
    fullscr=True,
    allowGUI = False,
    screen=1,
    units = 'deg')
#INITIALISE SOME STIMULI
temporalFreq = 4
phaseShiftPeriod = 1
increment = 0.5
#Gabor Stim
if info['stimType'] ==1:
    stim = visual.PatchStim(myWin,pos=(0,0), units = 'deg',
                           tex="sin",mask="gauss",
                           size=(2.0,2.0), sf=(.08), ori=-90,
                           autoLog=False)#this stim changes too much for autologging to work
#Noise stim
elif info['stimType']==2:
    stim = visual.DotStim(myWin, color=(1.0,1.0,1.0), dir=270, units='deg',
        nDots=500, fieldShape='square',fieldSize=4,
        dotLife=4, #number of frames for each dot to be drawn
        signalDots='same', #are the signal dots the 'same' on each frame? (see Scase et al)
        noiseDots='walk', #do the noise dots follow random- 'walk', 'direction', or 'position'
        speed=1, coherence=0.1)
#bar stim
elif info['stimType']==3:
    stim = visual.Rect(myWin, ori=-90, units='deg',
                                fillColor=(1,1,1), size = (2,.8))
# checkerboard
elif info['stimType']==4:
    stim = visual.PatchStim(myWin, tex="sqrXsqr",texRes=64,
           size=[4,4], sf=.5, mask = 'none', pos=(1,1))
           
myMouse = event.Mouse(win=myWin)
message = visual.TextStim(myWin,pos=(-0.95,-0.9),alignHoriz='left',height=0.08,
    text='left-drag=Position,Up/down Keys=size,Left/Right Keys = SF, Scroll = orientation', units = 'norm',
    autoLog=False)

while True: #continue until keypress
    #handle key presses each frame
    for key in event.getKeys():
        if key in ['escape']:
            print "Stim Type", str(info['stimType'])
            print "Position", str(stim.pos)
            print "Orientation", str(stim.ori)
            print "SF", str(stim.sf)
            print "Size", str(stim.size)
            print count
            core.quit()
        if info['stimType'] ==1:
            if key in ['q']:
                stim.setSF(0.02, '+')
                print "SF = ", str(stim.sf)
            if key in ['a']:
                stim.setSF(0.02, '-')
                print "SF = ", str(stim.sf)
            if key in ['1']:
                stim.setSF(.08)
                print "SF = ", str(stim.sf)
        if info['stimType'] !=3:
            if key in ['up']:
                stim.setPos([0,increment],'+')
                print "Position = ", str(stim.pos)
            if key in ['down']:
                stim.setPos([0,increment],'-')
                print "Position = ", str(stim.pos)
            if key in ['left']:
                stim.setPos([increment,0],'-')
                print "Position = ", str(stim.pos)
            if key in ['right']:
                stim.setPos([increment,0],'+')
                print "Position = ", str(stim.pos)
            if key in['/']:
                stim.setPos([0,0])
                print "Position=", str(stim.pos)
            if key in ['r']:
                temporalFreq += 1
                print "TF=", str(temporalFreq)
            if key in ['f']:
                temporalFreq -= 1
                print "TF=", str(temporalFreq)
            if key in ['4']:
                temporalFreq = 4
                print "TF=", str(temporalFreq)
            if key in ['t']:
                increment = increment + 0.5
                print "Position increment=", str(increment)
            if key in ['g']:
                increment = increment  - 0.5
                print "Position increment=", str(increment)
            if key in ['5']:
                increment = 0.5
                print "Position increment=", str(increment)
            if key in ['y']:
                phaseShiftPeriod = phaseShiftPeriod + 0.1
                print "Phase reverse period=", str(phaseShiftPeriod)
            if key in ['h']:
                phaseShiftPeriod = phaseShiftPeriod - 0.1
                print "Phase reverse period=", str(phaseShiftPeriod)
            if key in ['6']:
                phaseShiftPeriod = 1
        if info['stimType'] != 2:
            if key in ['e']:
                stim.setOri(11.25, '+')
                print "Orientation=", str(stim.ori+90)
            if key in ['d']:
                stim.setOri(11.25, '-')
                print "Orientation=", str(stim.ori+90)
            if key in['c']:
                stim.setOri(90,'-')
                print "Orientation=", str(stim.ori+90)
            if key in ['3']:
                stim.setOri(-90)
                print "Orientation=", str(stim.ori+90)
        if info['stimType']<3:
            if key in ['s']:
                stim.setSize(1,'-')
                print "Size = ", str(stim.size)
            if key in ['x']:
                stim.setSize(500)
                print "Size = ", str(stim.size)
            if key in ['2']:
                stim.setSize(2)
                print "Size = ", str(stim.size)
            if key in ['w']:
                stim.setSize(1, '+')
                print "Size = ", str(stim.size)
        if info['stimType'] == 4:
            if key in ['q']:
                stim.setSF(0.5, '/')
                print "SF = ", str(stim.sf)
            if key in ['a']:
                stim.setSF(0.5, '*')
                print "SF = ", str(stim.sf)
            if key in ['1']:
                stim.setSF(0.5)
                print "SF = ", str(stim.sf)
            cSizeInc = 1/stim.sf
            if key in ['x']:
                stim.setSize(500)
                print "Size = ", str(stim.size)
            if key in ['w']:
                stim.setSize(cSizeInc,'+')
                print "Size = ", str(stim.size)
            if key in ['s']:
                stim.setSize(cSizeInc,'-')
                print "Size = ", str(stim.size)
                
    #get mouse events
    #Handle the wheel(s):
    # Y is the normal mouse wheel, but some (e.g. mighty mouse) have an x as well
    mouse_dX,mouse_dY = myMouse.getRel()
    mouse1, mouse2, mouse3 = myMouse.getPressed()
    if (mouse3):
        stim.setSize(mouse_dX, '+',1)
    elif (mouse1):
        stim.setPos([mouse_dX, mouse_dY], '+', 20)        
    wheel_dX, wheel_dY = myMouse.getWheelRel()
    stim.setOri(wheel_dY*5, '+')
    clock = core.Clock()
    event.clearEvents()#get rid of other, unprocessed events
    #do the draw
    if info['stimType'] == 1:
        stim.setPhase(.001*temporalFreq,'+')
        stim.draw()
        myWin.flip()#redraw the buffer
    elif info['stimType'] ==4:
        clock4 = core.Clock()
        while clock4.getTime()<phaseShiftPeriod:
            stim.draw()
            myWin.flip()
        else: 
            stim.setContrast(-1,'*')
            stim.draw()
            myWin.flip()
            clock4.reset()
    else:
        stim.draw()
        myWin.flip()
        count += 1
