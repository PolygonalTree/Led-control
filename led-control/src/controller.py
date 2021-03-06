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
from PySide2 import QtCore
from model import *

from time import sleep
from threading import Thread
import serial
import serial.tools.list_ports
import pickle
import logging


class Controller(Thread):

    def __init__(self, exp=[], incubator=None):
        Thread.__init__(self)
        self.experiment = exp
        self.pastLightHistory=[]
        self.futureLightHistory=[]
        self.incubator = incubator
        self.ser = None
        self.previousLightState = None
        self.isExperimentRunning = False
        self.currentPeriod = None
        self.startExperimentTime = None
        self.endExperimentTime = None
        self.prevData = None
        self.prevport = None

    def run(self):
        try:
            time = QtCore.QDateTime.currentDateTime()
            #self.debugTime = time
            self.startExperimentTime = time
            timer = QtCore.QElapsedTimer()
            isSerialOpen = self.openSerial(self.incubator)

            if isSerialOpen:
                logging.info("Experiment started at:{}".format(self.startExperimentTime.toString("dd.MM.yy hh:mm")))
                self.mainController()
                # timer to only call the function every minute.
                logging.debug("Simulation started")
                self.simulateExperiment(time, hours=(time.daysTo(
                                                        QtCore.QDateTime(self.experiment[-1].dateEndTime))+1)*24)
                logging.debug("Simulation ended")
                self.isExperimentRunning = True
                self.previousLightState = None
                timer.start()
                while self.isExperimentRunning:
                    if timer.elapsed() > 60000:
                        # check serial is open
                        #self.checkArduinoAlive()
                        #sleep(0.2)
                        self.mainController()
                        timer.restart()
                        # sleep to save cpu, if more than 0.2 it becomes apparently
                        # unresponsive for the user.
                    sleep(0.2)
                self.closeSerial()
                print("serial closed")
            else:
                logging.debug("stopping experiment, serial not open")
                self.isExperimentRunning = False

        except Exception as e:
            print(e)
            logging.error(f"something happened in run, error:{e}")
            self.closeSerial()
            self.isExperimentRunning = False

    def mainController(self, isSimulation=False, startExperimentTime=None, futureTime=None):
        if isSimulation:
            actualTime = futureTime
        else:
            # Get the actual period
            actualTime = QtCore.QDateTime.currentDateTime()
            # time since start in min
            startExperimentTime = self.startExperimentTime
        if self.isExperimentRunning:
            timeSinceStart = self.startExperimentTime.secsTo(actualTime) / 60.
        else:
            timeSinceStart = startExperimentTime.secsTo(actualTime) / 60.
        #currentDate = actualTime.date()
        currentPeriod = self.periodActive(actualTime)

        try:
            if currentPeriod is None:
                if isSimulation:
                    self.futureLightHistory.append([-1,0,0,0,0,0,timeSinceStart])
                    self.endExperimentTime = actualTime
                else:
                    logging.debug("Stopped, current period is None and is not simulation")
                    self.isExperimentRunning = False

            else:
                period = self.experiment[currentPeriod]
                # check if it is the last period.
                isLightsOn = False
                colour = period.lightColour
                isRampingOn = period.isRampingOn
                rampPercent = 1
                # Decide if the lights needs to be on or off
                if period.isLL:
                        # ramping on first day:
                        endsRamping = period.switchOnTime.addSecs(period.rampingTime*3600)

                        if (period.dateStartTime.__eq__(actualTime.date())
                            and period.switchOnTime.__gt__(actualTime.time())):
                            isLightsOn = False

                        elif (period.dateStartTime.__eq__(actualTime.date())
                            and endsRamping.__gt__(actualTime.time())):

                            colour, rampPercent = self.rampingProccesing(actualTime.time(), isRampingOn, period)
                            isLightsOn = True

                        else:
                            colour, rampPercent = self.rampingProccesing(actualTime.time(), False, period)
                            isLightsOn = True

                elif period.isDD:
                    if (period.dateStartTime.__eq__(actualTime.date())
                            and period.switchOnTime.__gt__(actualTime.time())):
                        isLightsOn = False

                    else:
                        isLightsOn = False

                elif self.isHourInIntervalSim(currentPeriod,
                                              period.switchOnTime,
                                              period.switchOffTime,
                                              actualTime):
                    colour, rampPercent = self.rampingProccesing(actualTime.time(), isRampingOn, period)
                    isLightsOn = True

                else:
                    # LM moon light this need to be checked.
                    if period.isLM:
                        # white soft colour, minimum intensity
                        colour = [0,0,0,2]
                        isLightsOn = True
                    else:
                        isLightsOn = False

                if isSimulation:
                    self.futureLightHistory.append([int(isLightsOn),
                                                    colour[0],
                                                    colour[1],
                                                    colour[2],
                                                    colour[3],
                                                    rampPercent,
                                                    timeSinceStart])
                else:
                    logging.info("past_light:{},{},{},{},{},{},{},{},{},{}".format(
                                 actualTime.toString("dd.MM.yy hh:mm"),
                                 isLightsOn,
                                 colour[0],
                                 colour[1],
                                 colour[2],
                                 colour[3],
                                 rampPercent,
                                 period.isPulseOn,
				                 period.pulse[0],
				                 period.pulse[1],
                                 timeSinceStart))
                    self.currentPeriod = currentPeriod
                    #print("period {}".format(period))
                    self.writeDataToArduino(isLightsOn, colour, period)
                    self.pastLightHistory.append([int(isLightsOn),
                                                  colour[0],
                                                  colour[1],
                                                  colour[2],
                                                  colour[3],
                                                  rampPercent,
                                                  timeSinceStart])
        except Exception as e:
            print(e)
            logging.error(f"Error on main controller: {e}")
            self.closeSerial()
            self.isExperimentRunning = False

    ##Gets the period that is active
    def periodActive(self, actualTime):
        currentDate = actualTime.date()
        NextItem = 1
        last = False
        first = True
        for period in self.experiment:
            # ADD the hour of starting for the next period, just in case they are coincident,
            # i.e. for periods shorter than 24h.
            currentPeriod = None
            try:
                index = self.experiment.index(period)+1
                nextPeriod = self.experiment[index]
            except:
                last = True

            # check if logic inverted, logic will be inverted when switch off time happens
            # before in time than switch on time.
            if period.switchOffTime.__le__(period.switchOnTime):
                #logich inverted
                if (period.dateStartTime.__le__(currentDate)
                        and period.dateEndTime.__ge__(currentDate)):
                    if (not last
                            and period.dateEndTime.__eq__(nextPeriod.dateStartTime)
                            and period.dateEndTime.__eq__(actualTime.date())
                            and nextPeriod.switchOnTime.__le__(actualTime.time())):
                        if last:
                            currentPeriod = None
                        else:
                            currentPeriod = self.experiment.index(period)+1
                    else:
                        # if this is the last period, return None
                        currentPeriod = self.experiment.index(period)
                        break
            else:
                # normal logic
                if (period.dateStartTime.__le__(currentDate)
                        and period.dateEndTime.__ge__(currentDate)):
                    if (not last
                            and period.dateEndTime.__eq__(nextPeriod.dateStartTime)
                            and period.dateEndTime.__eq__(actualTime.date())
                            and nextPeriod.switchOnTime.__le__(actualTime.time())):
                        if last:
                            currentPeriod = None
                        else:
                            currentPeriod = self.experiment.index(period)+1
                    else:
                        currentPeriod = self.experiment.index(period)
                        break  # catch only the first ocurrence

            NextItem += 1
            first=False
        return currentPeriod

    ##Decide if the lights needs to be on or off
    def isHourInInterval(self):
        period = currentPeriod
        on = self.experiment[period].switchOnTime
        off = self.experiment[period].switchOffTime
        currentTime = QtCore.QTime.currentTime()
        if  off.__le__(on):
            # logic inverted
            if on.__ge__(currentTime) and off.__le__(currentTime):
                # inverted logic, lights off!
                actualLightState = self.previousLightState
            else:
                # lights on!
                actualLightState = True
        elif off.__ge__(on):
            # standart logic
            if  on.__le__(currentTime) and off.__ge__(currentTime):
                # lights on!
                actualLightState = self.previousLightState
            else:
                # lights Off!
                actualLightState = False

        return actualLightState

    # TODO refactor to merge the sim functions and normal functions.
    def isHourInIntervalSim(self, period, on, off, actualTime):
        p = self.experiment[period]
        hour = actualTime.time()
        date = actualTime.date()

        if off.__le__(on):
            # logic inverted
            if p.dateStartTime.__eq__(date) and on.__ge__(hour):
                # inverted logic
                #is this the first day, not info about previos light state
                if self.experiment[0].dateStartTime.__eq__(date):
                    actualLightState = False
                else:
                    # we get the info from previous state,
                    actualLightState = self.previousLightState
            elif on.__ge__(hour) and off.__le__(hour):
                # check if it is the first day of the period to avoid odd behaviour
                 actualLightState = False
            else:
                # lights on!
                 actualLightState = True

        elif off.__ge__(on):
            # standart logic
            if p.dateStartTime.__eq__(date) and on.__ge__(hour):
                # inverted logic, lights off!
                actualLightState = self.previousLightState
            elif  on.__le__(hour) and off.__ge__(hour):
                # lights on!
                actualLightState = True
            else:
                # lights Off!
                actualLightState = False

        self.previousLightState = actualLightState

        #print("lisght on?:",actualLightState)

        return actualLightState

    def simulateExperiment(self, startTime, hours = None):
        if hours is None:
            hours = 1200  #45 days of simulation if nothing given!

        timeToSimulate = hours*60*60*1000
        futureTime = startTime
        self.futureLightHistory = []
        timeSimulationEnds = startTime.addMSecs(timeToSimulate)
        #print("simulation started")
        while futureTime < timeSimulationEnds:
            self.mainController(True, startTime, futureTime)
            # security control:
            if self.futureLightHistory[-1][0] < 0:
                break

            futureTime = futureTime.addMSecs(60000)  # add 1min
        #print("simulation ended")
        self.previousLightState = None


    def openSerial(self, incubator):
        SNR = 0
        for port in serial.tools.list_ports.comports():
            SNR = self.getSNR(port)

            if SNR != None:
                if incubator['SN'] == SNR:
                    logging.debug("port {}".format(port[0]))
                    self.ser = serial.Serial(port[0], 9600, timeout=30)
                    self.ser.write(b'C\r')
                    sleep(0.5)
                    res = self.ser.readline()
                    if res.find(b'Led controller')>=0 :
                        logging.debug("Arduino connected")
                        self.prevport = self.ser.port
                        # block the arduino during experimnent to prevent errors
                        f = open('config.cfg','rb')
                        incubators= pickle.load(f)
                        for i in incubators:
                            if i['SN'] == incubator['SN']:
                                i.update(isRunning=True)
                        # print (incubators)
                        f.close()
                        with open('config.cfg', 'wb') as f:
                            pickle.dump(incubators,f, pickle.HIGHEST_PROTOCOL)
                        return True
                    else:
                        logging.debug("error, Not a Led controller")
                        self.ser.__del__()
                        self.isExperimentRunning = False
                        return False

    def checkArduinoAlive(self, period = None):
        logging.debug("serial open: {}".format(self.ser.is_open))
        isconnected = True
        if not self.ser.is_open:
            log_time = QtCore.QDateTime.currentDateTime()
            logging.warning("something, happend with arduino at {}".format(log_time.toString("dd.MM.yy hh:mm")))
            self.closeSerial()
            sleep(1)
            isconnected = self.openSerial(self.incubator)
        else:
            # try to connect
            try:
                #warning, this will not check if pulses are active, work around for error
                #when frequency for pulses is bigger than 1 min, correct this to something better
                # If arduino is running a period with pulses the check will fail because the response will not arrive on time.
                # So if the period running has pulses on it, lets wait until a response arrives, this does not make sense
                # when the period does not have pulses active
                if period.isPulseOn:
                    count = 0
                    #ask once every second.
                    while count < period.pulse[0]/1000:
                        self.ser.flushInput()
                        self.ser.write(b'C\r')
                        sleep(1)
                        res = self.ser.readline()
                        if res.find(b'Led controller') >= 0:
                            isconnected = True
                            break
                        count += 1
                    if res.find(b'Led controller') < 0:
                        logging.warning("error while checking arduino with pulses. restarting serial")
                        self.closeSerial()
                        isconnected = self.openSerial(self.incubator)
                else:
                    self.ser.flushInput()
                    self.ser.write(b'C\r')
                    sleep(0.5)
                    res = self.ser.readline()
                    if res.find(b'Led controller') < 0:
                        self.closeSerial()
                        isconnected = self.openSerial(self.incubator)

            except IOError as e:
                logging.error("Error on connecting to arduino {}".format(e))
                for port in serial.tools.list_ports.comports():
                    SNR = self.getSNR(port)

                    if SNR != None:
                        if self.incubator['SN'] == SNR:
                            logging.debug("port {}".format(port[0]))
                            self.ser.close()
                            self.ser.port = port[0]
                            self.ser.open()
                            self.ser.write(b'C\r')
                            sleep(0.5)
                            res = self.ser.readline()
                            if res.find(b'Led controller') >= 0:
                                isconnected = True
                            else:
                                isconnected = False
                    else:
                        isconnected = False
        return isconnected


    def closeSerial(self):
        try:
            if self.ser.is_open:
                self.writeDataToArduino(False,[0,0,0,0])
                self.ser.__del__()
        except Exception as e:
            self.ser.__del__()
            logging.error(e)
        with open('config.cfg','rb') as f:
            incubators= pickle.load(f)
            for i in incubators:
                if i['SN'] == self.incubator['SN']:
                    i.update(isRunning=False)
        with open('config.cfg', 'wb') as f:
            pickle.dump(incubators,f, pickle.HIGHEST_PROTOCOL)

    def serialPorts():
        """
        Returns a generator for all available serial ports
        """
        if os.name == 'nt':
            # windows
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    s.close()
                    yield 'COM' + str(i + 1)
                except serial.SerialException:
                    pass
        else:
            # unix
            for port in list_ports.comports():
                yield port[0]

    def listSerialPorts():
        """
        """
        return list(serialPorts())

    def detectIncubators(self, isRunning = False):
        # load saved incubators
        f = open('config.cfg', 'rb')
        incubatorDisplayList = []
        incubatorList = pickle.load(f)
        for port in serial.tools.list_ports.comports():
            SNR = self.getSNR(port)
            if SNR != None:
                for incubator in incubatorList:
                    if incubator['SN'] == SNR and incubator['isRunning'] == isRunning:
                        incubatorDisplayList.append(incubator)

        return incubatorDisplayList

    def getSNR(self, port):
        if port[2].find('SNR=') >= 0:
            SNR = port[2][port[2].find('SNR=') + 4:].split(" ")[0]
        elif port[2].find('SER=') >= 0:
            SNR = port[2][port[2].find('SER=') + 4:].split(" ")[0]
        elif port[2].find('PID') >= 0:
            SNR = port[2][port[2].find('PID=') + 4:].split(" ")[0]
        else:
            SNR = None
        return SNR

    def addIncubator(self):
        newIncubator = None
        try:
            f = open('config.cfg', 'rb')
            incubatorList = pickle.load(f)
        except:
            f = open('config.cfg', 'wb')
            incubatorList = []
            pass

        for port in serial.tools.list_ports.comports():
            SNR = self.getSNR(port)
            if SNR != None:
                new = True
                try:
                    for incubator in incubatorList:
                        if incubator['SN'] == SNR:
                            new = False
                except Exception as e:
                    logging.error('error in add. {}'.format(e))
                    pass

                if new:
                #is it an arduino?
                    try:
                        logging.info("new incubator detected")
                        s = serial.Serial(port[0],9600, timeout=10)
                        s.write(b'C\r')
                        res = s.readline()
                        if res.find(b'Led controller')>=0:
                            newIncubator = SNR#
                        sleep(1)
                        s.close()
                    except:
                        #it is not an arduino
                        try:
                            s.close()
                        except:
                            #TODO, again exception handling needs to be improved
                            pass
                        pass

        return newIncubator


    def unlockIncubator(self, incubator):
        try:
            with open('config.cfg', 'rb') as f:
                incubatorList = pickle.load(f)
        except:
            incubatorList = []
            logging.warning("Open config file failed")
            pass

        for inc in incubatorList:
            if incubator["SN"] == inc["SN"]:
                inc["isRunning"] = False
                with open('config.cfg','wb') as f:
                    pickle.dump(incubatorList, f, pickle.HIGHEST_PROTOCOL)
        return True


    def writeDataToArduino(self, on, colour, period=None):
        #colourIntensity = self.rampingProccesing(self.experiment[self.currentPeriod].isRampingOn)


        if not period:
            #there is no period because the experiment is finished
            data = "R{0}G{1}B{2}W{3}N\r".format(0,0,0,0)
        if on:
            if period.isPulseOn:
                data = "R{0}G{1}B{2}W{3}F{4}/{5}\r".format(colour[0],
                                                            colour[1],
                                                            colour[2],
                                                            colour[3],
                                                            period.pulse[0],
                                                            period.pulse[1])
            else:
                data = "R{0}G{1}B{2}W{3}N\r".format(colour[0],
                                                    colour[1],
                                                    colour[2],
                                                    colour[3])
        else:
            data = "R{0}G{1}B{2}W{3}N\r".format(0,0,0,0)

        # if data does not change avoid communication
        if data != self.prevData or self.ser.port != self.prevport :
            print("sending data to", self.ser.port)
            try:
                self.ser.write(bytes(data,'utf-8'))
            except Exception as e:
                logging.error("error while writing data to Arduino: {}".format(e))
                #try to reconnect
                self.ser.close()
                self.checkArduinoAlive(period)
            self.prevData = data
            self.prevport = self.ser.port
        else:
            logging.info("Same data, not sending it to arduino.")

    def rampingProccesing(self, actualTime, on, period):
        rampPercent = 1
        if on:
            try:
                onTime = period.switchOnTime
            except:
                onTime = QtCore.QTime(0,0,0,0)

            try:
                offTime = period.switchOffTime
            except:
                offTime = QtCore.QTime(0,0,0,0)

            rampTime = period.rampingTime
            endsRamping = onTime.addSecs(rampTime*3600)
            startsRamping = offTime.addSecs(-rampTime*3600)
            Intensity = list(period.lightColour)
            if onTime == QtCore.QTime(0,0,0,0):
                onTime = QtCore.QTime(0,0,0,1)
            if offTime == QtCore.QTime(0,0,0,0):
                offTime = QtCore.QTime(23,59,59,59)

            if actualTime.__ge__(onTime) and actualTime.__le__(endsRamping):
                #switching on
                x0 = onTime.hour()+onTime.minute()/60+onTime.second()/3600
                x1 = endsRamping.hour()+endsRamping.minute()/60+endsRamping.second()/3600
                y0 = 0
                y1 = 1
                x = (actualTime.hour()+actualTime.minute()/60+actualTime.second()/3600)
                y = self.lineEcuation(x0, x1, y0, y1, x)
                rampPercent = y
                i=0
                for colourIntensity in Intensity:
                    Intensity[i] = int(y*colourIntensity)
                    i+=1

            elif actualTime.__ge__(startsRamping) and actualTime.__le__(offTime):
                #switching off
                x0 = startsRamping.hour()+startsRamping.minute()/60+startsRamping.second()/3600
                x1 = offTime.hour()+offTime.minute()/60+offTime.second()/3600
                y0 = 1
                y1 = 0
                x = (actualTime.hour()+actualTime.minute()/60+actualTime.second()/3600)
                y = self.lineEcuation(x0, x1, y0, y1, x)
                rampPercent  = y
                i=0
                for colourIntensity in Intensity:
                    Intensity[i] = int(y*colourIntensity)
                    i+=1
            return Intensity, rampPercent
        else:
            return period.lightColour, rampPercent


    def lineEcuation(self,x0,x1,y0,y1,x):
        #used for ramping
        #Todo Implement a logaritmic function or other models
        m = (y1-y0)/(x1-x0)
        y = m * (x - x0) + y0
        return y

    def getRunningPeriod(self):
        return self.currentPeriod

    def getPastLightHistory(self):
        return self.pastLightHistory

    def getFutureLightHistory(self):
        return self.futureLightHistory

    def getStartExperimentTime(self):
        return self.startExperimentTime

    def getEndExperimentTime(self):
        return self.endExperimentTime

    def getIsExperimentRunning(self):
        return self.isExperimentRunning

    def setIsExperimentRunning(self, flag):
        self.isExperimentRunning = flag
        logging.info('running: {}'.format(self.isExperimentRunning))
        return self.isExperimentRunning
