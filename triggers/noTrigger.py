# No Triggering - A trigger class for when you want your stim to run freely, neither 
# sending information nor receiving it.
from abstractTrigger import trigger

#abstractTriggerCode = '../triggers/abstractTrigger.py'
#imp.load_source('', abstractTriggerCode)

class noTrigger(trigger):
    def __init__(self, args):  
        pass

    def preStim(self, args):
        pass

    def postStim(self, args):
        pass

    def preFlip(self, args):
        pass

    def postFlip(self, args):
        pass

    def wrapUp(self, args):
        pass
