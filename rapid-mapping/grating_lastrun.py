#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.73.05), March 26, 2012, at 15:37
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui
from psychopy.constants import * #things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os #handy system and path functions

#store info about the experiment session
expName='None'#from the Builder filename that created this script
expInfo={'participant':'s_001', 'ori':10}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#setup the Window
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

#Initialise components for routine:test
testClock=core.Clock()
patch=visual.PatchStim(win=win, name='patch',units=u'pix', 
    tex='sin', mask=None,
    ori=1.0, pos=[0, 0], size=[800, 600], sf=None, phase=trialClock.getTime()*2,
    color=[1,1,1], colorSpace=u'rgb', opacity=1,
    texRes=128, interpolate=False, depth=0.0)

#set up handler to look after randomisation of conditions etc
trials_2=data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath='C:\\PsychoPyExperiments\\grating.psyexp',
    trialList=[None],
    seed=None)
thisTrial_2=trials_2.trialList[0]#so we can initialise stimuli with some values
#abbreviate parameter names if possible (e.g. rgb=thisTrial_2.rgb)
if thisTrial_2!=None:
    for paramName in thisTrial_2.keys():
        exec(paramName+'=thisTrial_2.'+paramName)

for thisTrial_2 in trials_2:
    currentLoop = trials_2
    #abbrieviate parameter names if possible (e.g. rgb=thisTrial_2.rgb)
    if thisTrial_2!=None:
        for paramName in thisTrial_2.keys():
            exec(paramName+'=thisTrial_2.'+paramName)
    
    #Start of routine test
    t=0; testClock.reset()
    frameN=-1
    
    #update component parameters for each repeat
    patch.setOri([0])
    patch.setTex(u'sqr')
    #keep track of which have finished
    testComponents=[]#to keep track of which have finished
    testComponents.append(patch)
    for thisComponent in testComponents:
        if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
    #start the Routine
    continueRoutine=True
    while continueRoutine:
        #get current time
        t=testClock.getTime()
        frameN=frameN+1#number of completed frames (so 0 in first frame)
        #update/draw components on each frame
        
        #*patch* updates
        if t>=0.0 and patch.status==NOT_STARTED:
            #keep track of start time/frame for later
            patch.tStart=t#underestimates by a little under one frame
            patch.frameNStart=frameN#exact frame index
            patch.setAutoDraw(True)
        elif patch.status==STARTED and t>=(0.0+2.0):
            patch.setAutoDraw(False)
        
        #check if all components have finished
        if not continueRoutine:
            break # lets a component forceEndRoutine
        continueRoutine=False#will revert to True if at least one component still running
        for thisComponent in testComponents:
            if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                continueRoutine=True; break#at least one component has not yet finished
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #end of routine test
    for thisComponent in testComponents:
        if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#completed 5 repeats of 'trials_2'

#get names of stimulus parameters
if trials_2.trialList in ([], [None], None):  params=[]
else:  params = trials_2.trialList[0].keys()
#save data for this loop
trials_2.saveAsPickle(filename+'trials_2')
trials_2.saveAsExcel(filename+'.xlsx', sheetName='trials_2',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

#Shutting down:
win.close()
core.quit()
