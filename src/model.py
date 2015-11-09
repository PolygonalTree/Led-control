class Experiment():
    # a group (list) of periods
    
    header = ['Light', ' Start Day', ' End Day', ' Switch on', 'Switch off', 'LL', 'DD', 'Ramping', 'Pulse']
    
    def __init__(self):
        self.experiment = []
    
    def delete(self, periodToDelete):
        self.experiment.pop(periodToDelete)
    
class Period():
    
    def __init__(self):
        self.lightColour = [0,0,0,0] #RGBW list, values from 0 to 255
        self.dateStartTime = [] ### PySide.QtCore.QDate object.  
        self.dateEndtime = [] ## PySide.QtCore.QDate object. 
        self.switchOnTime = [9,0] #tupla hour-minutes
        self.switchOffTime = [21,0]
        #self.isIntervalHours = True
        self.isLL = False
        self.isDD = False
        self.isLM = False
        self.isRampingOn = False
        self.rampingTime = 0
        self.isPulseOn = False
        self.pulse = [0,0]
