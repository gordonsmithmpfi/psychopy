import UniversalLibrary as UL #The Measurement Computing DAQ library

class MccDaq:
    """
    Initializes a Measurement Computing DAQ
    Can read digital input from first port ("A")
    Can put digital output to second port ("B").
    
    Digital input reads will block until data is received.
    """
    
    isTriggered=False
    def __init__(self, isTriggered_):
        isTriggered = isTriggered_
        if isTriggered:
            BoardNumA = 0
            PortNumA = UL.FIRSTPORTA
            DirectionA = UL.DIGITALIN
            UL.cbDConfigPort(BoardNumA, PortNumA, DirectionA)
        else:
            BoardNumA = 0
            PortNumA = UL.FIRSTPORTA
            DirectionA = UL.DIGITALOUT
            UL.cbDConfigPort(BoardNumA, PortNumA, DirectionA)
            
        BoardNumB = 0
        PortNumB = UL.FIRSTPORTB
        DirectionB = UL.DIGITALOUT
        UL.cbDConfigPort(BoardNumB, PortNumB, DirectionB)
        
    def readStimcode(self):
        
        return 



# This data will exist in all
    # BaseClasses (even uninstantiated ones)
    Name = "BaseClass"
    # __init__ is a class constructor
    # __****__ is usually a special class method.

    # Self is used as an argument to
    # pretty much all class functions.
    # However, you do NOT need to pass
    # the argument self if you call this method
    # from a Class, because the class provides
    # the value of itself.
    def display(self):
        print self.Name
        print self.value1
        print self.value2




