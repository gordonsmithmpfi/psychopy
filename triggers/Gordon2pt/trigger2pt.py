# Accepts serial port triggers from the 2-photon acquisition system
# Sends stimcodes to the CED via the Measurement Computing DAQ

class importTest:
    def __init__(self, serialPortName):        
        

    def preStim(self)
        print "This code runs before each stim is displayed"

    def postStim(self)
        print "This code runs after each stim is displayed"


    def preFlip(self)
        print "This code runs before each stimulus frame is displayed"

    def postFlip(self)
        print "This code runs after each stimulus frame is displayed"


    def wrapUp(self)
        print "This code is run after all stimuli have run."