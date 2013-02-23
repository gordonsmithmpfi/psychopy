import csv
# define path, empty trigger time matrices
# must be run in admin mode to have read/write access in Windows

triggerTimes = []

# GUI for logging
# This wants to be shown on only 1 screen i.e. not the stim screen
info= {'logPath':'c:/users/fitzlab1/documents/', 'expNum':'exp001.txt'}
infoDlg = gui.DlgFromDict(dictionary=info, title='Experiment Parameters')

# python's string concatenation is a bit awkward
# this just concatenates path and file name obtained from dialog box
p = []
p.append(info['logPath'])
p.append(info['expNum'])
path = ''.join(p)

# when psychopy receives a trigger, log the time
triggerTimes.append([timer2.getTime()])

# This goes at the end of stimulus code, can be used to dump triggerTimes, n
with open(path, "a") as csvfile:
  expWrite = csv.writer(csvfile, dialect = 'excel')
  i = 0
  expWrite = writerows('path')
  while i<triggerTimes.size:
    expWrite = writerows(tiggerTimes[i,1])
    i+=1
