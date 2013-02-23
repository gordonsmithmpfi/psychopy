# Daq Triggering - triggers when stimcodes arrive via a Measurement Computing DAQ
# used in intrinsic imaging experiments in the SLM room
import UniversalLibrary as UL
from abstractTrigger import trigger

class daqTrigger(trigger):
    def __init__(self, args):  
        #DAQ setup
        self.boardNum = 0
        UL.cbDConfigPort(self.boardNum,UL.FIRSTPORTA, UL.DIGITALIN)

    def preStim(self, args):
        print 'Waiting for stimcode to arrive on DAQ...'
        stimcode = 0;
        while stimcode > 64 or stimcode == 0:
            #keep trying until a valid stimcode appears
            stimcode = UL.cbDIn(self.boardNum, UL.FIRSTPORTA, stimcode)
        print 'Got stimcode ',stimcode

    def postStim(self, args):
        pass

    def preFlip(self, args):
        pass

    def postFlip(self, args):
        pass

    def wrapUp(self, args):
        pass
