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
myWin = visual.Window(monitor='laptop',
    size=(1366,768),
    fullscr=True,
    allowGUI = False,
    screen=0,
    units = 'deg')
#INITIALISE SOME STIMULI
phaseShift = 0.05
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
           size=[4,4], sf=.5, mask = 'none')
           
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
        if info['stimType'] ==1 or info['stimType'] == 4:
            if key in ['q']:
                stim.setSF(0.02, '+')
                print "SF = ", str(stim.sf)
            if key in ['a']:
                stim.setSF(0.02, '-')
                print "SF = ", str(stim.sf)
            if key in ['1']:
                stim.setSF(.08)
                print "SF = ", str(stim.sf)
        if info['stimType'] != 3:
            if key in ['w']:
                stim.setSize(1, '+')
                print "Size = ", str(stim.size)
            if key in ['s']:
                stim.setSize(1,'-')
                print "Size = ", str(stim.size)
            if key in ['x']:
                stim.setSize(500)
                print "Size = ", str(stim.size)
            if key in ['2']:
                stim.setSize(2)
                print "Size = ", str(stim.size)
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
                phaseShift = phaseShift+0.02
                print "Phaseshift per frame=", str(phaseShift)
            if key in ['f']:
                phaseShift = phaseShift - 0.02
                print "Phaseshift per frame=", str(phaseShift)
            if key in ['v']:
                phaseShift = phaseShift * -1
                print "Phaseshift per frame=", str(phaseShift)
            if key in ['4']:
                phaseShift = 0.05
                print "Phaseshift per frame=", str(phaseShift)
            if key in ['t']:
                increment = increment + 0.5
                print "Position increment=", str(increment)
            if key in ['g']:
                increment = increment  - 0.5
                print "Position increment=", str(increment)
            if key in ['5']:
                increment = 0.5
                print "Position increment=", str(increment)
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
        stim.setPhase(phaseShift, '+')#advance 0.05cycles per fram    
        stim.draw()
        myWin.flip()#redraw the buffer
    elif info['stimType'] ==4:
#        stim.setContrast(-1, '*')
        if count % 60 == 0:
            stim.setContrast(-1, '*')
            stim.draw()
            myWin.flip()
            count +=1
        else:
            stim.draw()
            myWin.flip()
            count +=1
    elif info['stimType'] == 3:
        if count %17 == 0:
            stim.setPos([-1,0],'+')
            stim.draw()
            myWin.flip()
            count += 1
        if count % 7 == 0:
            stim.setPos([1,0],'+')
            stim.draw()
            myWin.flip()
            count += 1
        else:
            stim.draw()
            myWin.flip()
            count += 1
    else:
        stim.draw()
        myWin.flip()
        count += 1

