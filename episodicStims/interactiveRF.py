#!/usr/bin/env python
from psychopy import visual, core, event, misc, logging, gui
import csv

# In GUI, use 1 for Gabor, 2 for noise, 3 for bar, 4 for checkerboard
info= {'stimType':1, 'logPath':'c:/users/fitzlab1', 'expName':'exp001.txt'}

# logging not implemented yet
infoDlg = gui.DlgFromDict(dictionary=info, title='Experiment Parameters')

#create a window to draw in; make sure this is a monitor of the proper size and one that is set up in your monitor center
myWin = visual.Window(monitor='laptop',
    size=(1366,768),
    fullscr=True,
    allowGUI = True,
    screen=0,
    units = 'deg')

#myWin = visual.Window(monitor='stimMonitor',l
#    size = (1920,1080),
#    fullscr=True,
#    allowGUI = True,
#    screen = 0,
#    units = 'deg')

#INITIALISE SOME STIMULI
# Gabor
if info['stimType'] ==1:
    stim = visual.PatchStim(myWin,pos=(0,0), units = 'deg',
                           tex="sin",mask="gauss",
                           size=(2.0,2.0), sf=(.4), ori=90,
                           autoLog=False)#this stim changes too much for autologging to work
# noise
elif info['stimType']==2:
    stim = visual.DotStim(myWin, color=(1.0,1.0,1.0), dir=270, units='deg',
        nDots=500, fieldShape='square',fieldSize=4,
        dotLife=4, #number of frames for each dot to be drawn
        signalDots='same', #are the signal dots the 'same' on each frame? (see Scase et al)
        noiseDots='walk', #do the noise dots follow random- 'walk', 'direction', or 'position'
        speed=1, coherence=0.1)
# Bar Stim
elif info['stimType']==3:
    stim = visual.Rect(myWin, ori=90, units='deg',
                                fillColor=(1,1,1), size = (2,.5))
# CheckerboardStim
elif info['stimType']==4:
    stim = visual.PatchStim(myWin, tex="sqrXsqr",texRes=64,
           size=[4,4], sf=.5, mask = 'none')
           
myMouse = event.Mouse(win=myWin)
message = visual.TextStim(myWin,pos=(-0.95,-0.9),alignHoriz='left',height=0.08,
    text='left-drag=Position,Up/down Keys=size,Left/Right Keys = SF, Scroll = orientation', units = 'norm',
    autoLog=False)


while True: #continue until keypress
    #handle key presses each frame
    for key in event.getKeys():
        if key in ['escape']:
            print "Path", str(info['logPath'])
            print "Experiment Name", str(info['expName'])
            print "Stim Type", str(info['stimType'])
            print "Position", str(stim.pos)
            print "Orientation", str(stim.ori-90)
            print "SF", str(stim.sf)
            print "Size", str(stim.size)
            core.quit()
        if info['stimType'] ==1:
            if key in ['q']:
                stim.setSF(0.05, '+')
            if key in ['a']:
                stim.setSF(0.05, '-')
        if info['stimType'] < 3:
            if key in ['p']:
                stim.setPhase(0.05,'+')
        if key in ['w']:
            stim.setSize(1, '+')
        if key in ['s']:
            stim.setSize(1,'-')
        if key in ['h']:
            message.draw()
        if key in ['up']:
            stim.setPos([0,0.5],'+')
        if key in ['down']:
            stim.setPos([0,0.5],'-')
        if key in ['left']:
            stim.setPos([0.5,0],'-')
        if key in ['right']:
            stim.setPos([0.5,0],'+')
        if key in ['o']:
            stim.setOri(11.25, '+')
        if key in ['l']:
            stim.setOri(11.25, '-')
        if key in ['p']:
            stim.setOri(90)
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

    event.clearEvents()#get rid of other, unprocessed events
    #do the drawi
    if info['stimType'] < 3:
        stim.setPhase(0.05, '+')#advance 0.05cycles per fram    
        stim.draw()
        myWin.flip()#redraw the buffer
    else:
        stim.draw()
        myWin.flip()
