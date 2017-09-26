"""
Copyright (C) 2014  Luis Garcia Rodriguez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Email: luis.garcia@uni-muenster.de

"""
class Experiment():
    """
    An Object containing a list of periods.
    """

    header = ['Light', ' Start Day', ' End Day', ' Switch on', 'Switch off', 'LL', 'DD', 'Ramping', 'Pulse']

    def __init__(self):
        self.experiment = []

    def delete(self, periodToDelete):
        self.experiment.pop(periodToDelete)

class Period():
    """
    Main object that storages the data from the GUI input.
    It defines several parameters to be able to work with the arduino.
    """
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
