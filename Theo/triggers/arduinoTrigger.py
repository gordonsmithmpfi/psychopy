# Arduino Triggering - uses an Arduino to send and receive messages
# See the Arduino DAQ project in the repository to configure an Arduino for this

# This will probably be deprecated by the DaqFlex library, which will allow us to use
# the MCC DAQs on OSX computers.

from abstractTrigger import trigger

class arduinoTrigger(trigger):
    def __init__(self, args):  
        arduino = serial.Serial('/dev/tty.usbmodem1a21', 9600, timeout=0)
        time.sleep(3) #need to sleep 3s to allow Arduino to initialize

    def preStim(self, args):
        stimNumber = args
        arduino.write('t')
        print "Waiting for trigger"
        while True:
            response = arduino.read()
            if len(response)>0:
                break
        #send stimcode
        arduino.write('w' + str(stimNumber+1))

    def postStim(self, args):
        pass

    def preFlip(self, args):
        pass

    def postFlip(self, args):
        pass

    def wrapUp(self, args):
        pass
