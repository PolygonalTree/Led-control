#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Add Licence
"""
from PySide import QtCore, QtGui, QtSql
from GuiCode import Ui_MainWindow
from controller import *
from model import *
from addIncubatorGui import *
from selectIncubatorGui import *
import pickle
import sys, threading, os
from time import sleep


class ControlMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        #self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.dateTimeEdit.setMinimumDate(QtCore.QDate.currentDate())
        self.dateTimeEdit_2.setMinimumDate(QtCore.QDate.currentDate())
        self.buttonAddPeriod.clicked.connect(self.addPeriod)
        self.buttonUpdate.clicked.connect(self.updatePeriod)
        self.buttonUpdate.hide()
        self.buttonDel.clicked.connect(self.deletePeriods)
        self.buttonSave.clicked.connect(self.saveExperiment)
        self.buttonLoad.clicked.connect(self.loadExperiment)
        self.buttonStart.clicked.connect(self.startExperiment)
        self.buttonStop.clicked.connect(self.stopExperiment)
        self.buttonSim.clicked.connect(self.simulation)
        self.tableWidget.itemSelectionChanged.connect(self.selectPeriod)
        self.tableWidget.setColumnWidth(0,120)
        self.graph = QtGui.QGraphicsScene()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateDrawCurrentPeriod)
        #self.graph.update(0,0,800,200)
        #self.graphicsView.resetCachedContent()
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft)
        self.actionAdd_new_incubator.triggered.connect(self.addIncubator)
        self.periodUpdated = False
        
        
    
    @QtCore.Slot()
    def addIncubator(self):
        addD = DialogAddIncubator(self)
        control = Controller()
        snr = control.addIncubator()
        if snr == None:
            addD.addDialog.label_3.setText("""There is no new inubator detected,
            please check the cable.""")
            addD.addDialog.lineEdit.setDisabled(True)
        else:
            addD.addDialog.label_3.setText(snr)
            
        r = addD.exec_()
        if r == QtGui.QDialog.Accepted:
            try:
                f = open('config.cfg', 'rb')
                old_list = pickle.load(f)
                f.close()
            except:
                f= open('config.cfg','wb')
                old_list = []
            name = addD.addDialog.lineEdit.text()
            
            if name != '':
                newIncubator = {'SN':snr, 'name':name, 'isRunning':False}
                old_list.append(newIncubator)
                f = open('config.cfg','wb')
                pickle.dump(old_list, f, pickle.HIGHEST_PROTOCOL)
                #print (old_list)
                f.close()
    

            
    @QtCore.Slot()
    def addPeriod(self):
        try:
            self.exp
        except:
            self.exp = Experiment()
            
        period = Period()
        period.lightColour[0] = self.spinBox.value() 
        period.lightColour[1] = self.spinBox_2.value() 
        period.lightColour[2] = self.spinBox_3.value() 
        period.lightColour[3] = self.spinBox_4.value() 
        
        period.switchOnTime = self.timeEdit.time()
        period.switchOffTime = self.timeEdit_2.time()
        period.dateStartTime = self.dateTimeEdit.date()
        period.dateEndTime = self.dateTimeEdit_2.date()
        
        period.isDD = self.radioButton_3.isChecked() 
        period.isLL = self.radioButton_2.isChecked() 
        period.isLM = self.radioButton_6.isChecked()
        period.isRampingOn = self.radioButton_4.isChecked()
        period.rampingTime = self.doubleSpinBox.value()
        
        period.isPulseOn = self.radioButton_5.isChecked()
        period.pulse = [self.spinBox_5.value(),self.spinBox_6.value()]
        print (period.pulse)
        #print (period.dateStartTime)
        #print (period.switchOnTime)
        self.exp.experiment.append(period)
        self.printTable()
        
    ## Draw the periods on the tableWidget
    def printTable(self):
        self.tableWidget.setColumnCount(len(self.exp.header))
        self.tableWidget.setHorizontalHeaderLabels(self.exp.header)
        self.tableWidget.setRowCount(len(self.exp.experiment))
        
        i=0
        for period in self.exp.experiment:
            itemLight = QtGui.QTableWidgetItem("R:{0}/G:{1}/B:{2}/W:{3}".format(period.lightColour[0],
                                                                                period.lightColour[1],
                                                                                period.lightColour[2],
                                                                                period.lightColour[3]))
            itemLight.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,0,itemLight)
            
            itemStartDay = QtGui.QTableWidgetItem("{0}/{1}/{2}".format(period.dateStartTime.day(),
                                                                       period.dateStartTime.month(),
                                                                       period.dateStartTime.year()))
            itemStartDay.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,1,itemStartDay)
            
            itemEndDay = QtGui.QTableWidgetItem("{0}/{1}/{2}".format(period.dateEndTime.day(),
                                                                       period.dateEndTime.month(),
                                                                       period.dateEndTime.year()))
            itemEndDay.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,2,itemEndDay)
            
            itemSOn = QtGui.QTableWidgetItem("{0:0=2d}:{1:0=2d}".format(period.switchOnTime.hour(),
                                                                        period.switchOnTime.minute()))
            itemSOn.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,3,itemSOn)
            
            itemSOff = QtGui.QTableWidgetItem("{0:0=2d}:{1:0=2d}".format(period.switchOffTime.hour(),
                                                                         period.switchOffTime.minute()))
            itemSOff.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,4,itemSOff)
            
            
            itemLL = QtGui.QTableWidgetItem("{0}".format("yes" if period.isLL  else "no"))
            itemLL.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,5,itemLL)
            
            itemDD = QtGui.QTableWidgetItem("{0}".format("yes" if period.isDD  else "no"))
            itemDD.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,6,itemDD)
            
            itemRamp = QtGui.QTableWidgetItem("{0}".format("yes" if period.isRampingOn else "no"))
            itemRamp.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,7,itemRamp)
            
            itemPulse = QtGui.QTableWidgetItem("{0}".format("yes" if period.isPulseOn else "no"))
            itemPulse.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,8,itemPulse)
            
            
            i += 1
            
            
    @QtCore.Slot()
    def selectPeriod(self):
        try:
            items = self.tableWidget.selectedItems()
            periodToUptade = []
            for item in items:
                periodToUptade.append(item.row()) 
        
            periodToUptade = list(set(periodToUptade))
            #print (periodToUptade)
        except:
           pass
        
        if len(periodToUptade) == 1 :
        
            self.buttonUpdate.show()
            self.buttonAddPeriod.setText("Copy Period")

            self.selectedPeriod = periodToUptade[0]
            
            period = self.exp.experiment[self.selectedPeriod]

            self.spinBox.setValue(period.lightColour[0])
            self.spinBox_2.setValue(period.lightColour[1])  
            self.spinBox_3.setValue(period.lightColour[2]) 
            self.spinBox_4.setValue(period.lightColour[3])   

            self.timeEdit.setTime(period.switchOnTime)  
            self.timeEdit_2.setTime(period.switchOffTime)
            self.dateTimeEdit.setDate(period.dateStartTime) 
            self.dateTimeEdit_2.setDate(period.dateEndTime)  
            self.radioButton_4.setChecked(period.isRampingOn)
            self.doubleSpinBox.setValue(period.rampingTime)
            if period.isDD or period.isLL:
                self.radioButton_3.setChecked(period.isDD) 
                self.radioButton_2.setChecked(period.isLL)
            else:
                self.radioButton.setChecked(True)   
            
            
        else:
            self.buttonUpdate.hide()
            self.buttonAddPeriod.setText("Add Period")
        

    ##Delete selected periods from the experiment list
    @QtCore.Slot()
    def deletePeriods(self):
        periodsToDelete=[]
        for idx in self.tableWidget.selectedIndexes():
            periodsToDelete.append(idx.row()) 
        
        periodsToDelete = list(set(periodsToDelete))
        #print (periodsToDelete)
        for period in reversed(periodsToDelete):
            #print (period)
            self.exp.delete(period)
        self.printTable()
     
    @QtCore.Slot()
    def updatePeriod(self):
        
        period = self.exp.experiment[self.selectedPeriod]
        period.lightColour[0] = self.spinBox.value() 
        period.lightColour[1] = self.spinBox_2.value() 
        period.lightColour[2] = self.spinBox_3.value() 
        period.lightColour[3] = self.spinBox_4.value() 
        
        period.switchOnTime = self.timeEdit.time()
        period.switchOffTime = self.timeEdit_2.time()
        period.dateStartTime = self.dateTimeEdit.date()
        period.dateEndTime = self.dateTimeEdit_2.date()
        
        period.isDD = self.radioButton_3.isChecked() 
        period.isLL = self.radioButton_2.isChecked() 
        period.isRampingOn = self.radioButton_4.isChecked()
        period.rampingTime = self.doubleSpinBox.value()
                
        period.isPulseOn = self.radioButton_5.isChecked()
        period.pulse = [self.spinBox_5.value(),self.spinBox_6.value()]
        self.periodUpdated = True
        self.printTable()
        
    @QtCore.Slot()
    def saveExperiment(self):
        directory = "./experiments_saved"
        if not os.path.exists(directory):
            os.makedirs(directory)
        fileName = QtGui.QFileDialog.getSaveFileName(self,
    "Save Experiment", directory, filter ="Experiment Files (*.exp *.);;All Files (*)")
#        f = open("./experiments_saved/Experiment_{0}_{1}_{2}.exp"
#                .format(self.exp.experiment[0].dateStartTime.year(),
#                        self.exp.experiment[0].dateStartTime.month(),
#                        self.exp.experiment[0].dateStartTime.day())
#                ,'wb')
        try:
            f = open(fileName[0],'wb')
            pickle.dump(self.exp,f,-1)
            f.close()
        except:
            pass
            

    
    @QtCore.Slot()
    def loadExperiment(self):
        directory = "./experiments_saved"
        fileName = QtGui.QFileDialog.getOpenFileName(self,
    "Open Experiment", directory, "Experiment Files (*.exp);;All Files(*)")
        try:
            f = open(fileName[0], 'rb')
            self.exp = pickle.load(f)
            f.close()
        except:
            pass

        self.printTable()
        
        
    @QtCore.Slot()
    def startExperiment(self):
        #Dialog to select incubator
        #check attached incubators, generate list
    
        self.control = Controller(self.exp.experiment)
        incubators = self.control.detectIncubators()
        d = DialogSelectIncubator(self)
        
        for incubator in incubators:
            d.dialog.listWidget.addItem(str(incubator['name']))
        
        if len(incubators)==0:
            d.dialog.listWidget.addItem("""There is no incubators available,
add a new one or stop some experiment""")
        
        r=d.exec_()

        if r==QtGui.QDialog.Accepted:
            #takes the selected incubator
            incubatorName = d.dialog.listWidget.currentItem()
            
            for incubator in incubators:
            
                if str(incubatorName.text()) == str(incubator['name']):
                    
                    self.control = Controller(self.exp.experiment, incubator)
                    
                    self.control.start()
                    print("started")
                    i=0
                    while True:
                        test = self.control.getIsExperimentRunning()
                        if test == True:
                            print(test)
                            break
                        elif test == False:
                            break
                        else:
                            sleep(0.5)

                      
                    if self.control.getIsExperimentRunning() == True:
                        self.incubatorName = incubatorName.text()
                        self.buttonStart.setEnabled(False)
                        self.buttonSim.setEnabled(False)
                        self.buttonStop.setEnabled(True)
                        self.drawCurrentPeriod()
                        self.timer.start(60000)
                    else:
                        self.stopExperiment()
                        print("stopped")

            
        else:
            #print("cancelled")
            pass
    
    @QtCore.Slot()
    def stopExperiment(self):
        if hasattr(self, 'control'):
            self.control.setIsExperimentRunning(False)
            self.control.join()
            if not self.control.isAlive():
                self.buttonStart.setEnabled(True)
                self.buttonSim.setEnabled(True)
                self.buttonStop.setEnabled(False)
                self.timer.stop()
        else:
            try:
                self.buttonStart.setEnabled(True)
                self.buttonSim.setEnabled(True)
                self.buttonStop.setEnabled(False)
                self.timer.stop()
            except Exception as e:
                print (e)
        
    def drawCurrentPeriod(self):

        period=self.control.getRunningPeriod()
        pastLightHistory = self.control.getPastLightHistory()
        futureLightHistory = self.control.getFutureLightHistory()
        actualTime = QtCore.QDateTime.currentDateTime()

        
        self.graph.clear()
        try:
            self.label.setText("{0}->Period Running = {1}".format(self.incubatorName,period+1))
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)

        except:
            self.label.setText("Experiment Ended")
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)

                    
        
        
        i=0
        heigh = 20
        for item in pastLightHistory:  
            x = i
            y = 0
            
            if item[0] == 0:
                self.graph.addLine(i,y,i,heigh)
            elif item[0] == 1:
                R = 255 if item[1] > 0 else 0
                G = 255 if item[2] > 0 else 0
                B = 255 if item[3] > 0 else 0
                W = 0 if item[4] > 0 else 255
                colourPen = QtGui.QColor(R,G,B,W)
                pen.setColor(colourPen)
                self.graph.addLine(i,y,i,heigh,pen)
                self.graph.addLine(i,y,i,y)
                self.graph.addLine(i,heigh,i,heigh)
                if item[5]>0:
                    self.graph.addLine(i,y,i,(1-item[5])*heigh)
            elif item[0] == -1:
                self.graph.addLine(i,y,i,heigh)
                endTime = self.control.getEndExperimentTime()
                endTime = endTime.toString("dd.MM.yy hh:mm")
                text = self.graph.addText("Ends on {0}".format(endTime))
                text.setPos(i,-22)
                break
            ##initialize prevItem
            if i == 0:
                prevItem = item[0]
                self.graph.addLine(i,y,i,heigh)
                startedTime = actualTime.toString("dd.MM.yy hh:mm")
                self.updatedText = self.graph.addText("Updated on {0}".format(startedTime))
                self.updatedText.setPos(-170, 0)
            ##add the hour when the condition change
            if prevItem != item[0]:
                self.graph.addLine(i,-20,i,heigh)
                hour = actualTime.addSecs(i*60)
                hour = hour.toString("dd.MM.yy hh:mm")
                text = self.graph.addText("{0}".format(hour))
                text.setPos(i,0)
                
            prevItem = item[0]
            i += 1
            
  
        self.nowLine = self.graph.addLine(i,-20,i,heigh)
        self.nowText = self.graph.addText("Now")
        self.nowText.setPos(i,-22)
        now_counter = i
        for item in futureLightHistory:
            x = i
            y = 0
            heigh = 20

            if item[0] == 0:
                self.graph.addLine(i,y,i,heigh)
            elif item[0] == 1:
                R = 255 if item[1] > 0 else 0
                G = 255 if item[2] > 0 else 0
                B = 255 if item[3] > 0 else 0
                W = 0 if item[4] > 0 else 255
                colourPen = QtGui.QColor(R,G,B,W)
                pen.setColor(colourPen)
                self.graph.addLine(i,y,i,heigh,pen)
                self.graph.addLine(i,y,i,y)
                self.graph.addLine(i,heigh,i,heigh)
                if item[5]>0:
                    self.graph.addLine(i,y,i,(1-item[5])*heigh)
            elif item[0] == -1:
                self.graph.addLine(i,y,i,heigh)
                endTime = self.control.getEndExperimentTime()
                endTime = endTime.toString("dd.MM.yy hh:mm")
                text = self.graph.addText("Ends on {0}".format(endTime))
                text.setPos(i,0)
                break
            ##initialize prevItem
#            if i == 0:
#                prevItem = item[0]
#                self.graph.addLine(i,-20,i,heigh)
#                startTime = startTime.toString("dd.MM.yy hh:mm")
#                text = self.graph.addText("Starts on {0}".format(startTime))
#                text.setPos(i,-22)
            ##add the hour when the condition change
            if prevItem != item[0]:
                self.graph.addLine(i,-20,i,heigh)
                hour = actualTime.addSecs((i-now_counter)*60)
                hour = hour.toString("dd.MM.yy hh:mm")
                text = self.graph.addText("{0}".format(hour))
                text.setPos(i,-22)
                
            prevItem = item[0]
            i += 1
            
        self.graphicsView.setScene(self.graph)
        self.graphicsView.show()
        
        if self.control.getIsExperimentRunning() == False:
            self.stopExperiment()
            
    
    def updateDrawCurrentPeriod(self):
        if self.periodUpdated == True:
            print("updated")
            self.control.simulateExperiment(QtCore.QDateTime.currentDateTime())
            self.drawCurrentPeriod()
            self.periodUpdated = False
        else:    
            period=self.control.getRunningPeriod()
            pastLightHistory = self.control.getPastLightHistory()
            futureLightHistory = self.control.getFutureLightHistory()
            actualTime = QtCore.QDateTime.currentDateTime()

            
           # self.graph.clear()
            try:
                self.label.setText("{0}->Period Running = {1}".format(self.incubatorName,period+1))
                pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
                nowLine = None
            except:
                self.label.setText("Experiment Ended")
                pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
                nowLine = None
                    
            
            i=0
            heigh = 20
            for item in pastLightHistory:  
                x = i
                y = 0
                
                ##initialize prevItem
                if i == 0:
                    prevItem = item[0]
                    self.graph.removeItem(self.updatedText)
                    #self.graph.addLine(i,y,i,heigh)
                    startedTime = actualTime.toString("dd.MM.yy hh:mm")
                    self.updatedText = self.graph.addText("Updated on {0}".format(startedTime))
                    self.updatedText.setPos(-170, 0)
                i += 1    
            
            self.graph.removeItem(self.nowLine)
            self.graph.removeItem(self.nowText)
            self.nowLine = self.graph.addLine(i,-20,i,heigh)
            self.nowText = self.graph.addText("Now")
            self.nowText.setPos(i,-22)
            now_counter = i
            for item in futureLightHistory:
                x = i
                y = 0
                i += 1
                
            self.graphicsView.setScene(self.graph)
            self.graphicsView.show()
            
        if self.control.getIsExperimentRunning() == False:
            self.stopExperiment()
        
    def simulation(self):
        if hasattr(self, 'exp') and len(self.exp.experiment)>0:
            self.control = Controller(self.exp.experiment)
            simStartTime = QtCore.QDateTime()
            simStartTime.setDate(self.exp.experiment[0].dateStartTime)
            
            simEndTime = QtCore.QDateTime()
            simEndTime.setDate(self.exp.experiment[-1].dateEndTime)
            simEndTime = simEndTime.addDays(2)
            
            interval = simStartTime.secsTo(simEndTime)/3600.
            if interval == 0:
                interval = 24 #simulate at least 24 hours
            
            self.control.simulateExperiment(simStartTime,interval)
            futureLightHistory = self.control.getFutureLightHistory()
            
            f = open('daylight','w')
            f.write('{0}\r'.format(simStartTime.toString('dd.MM.yyyy hh:mm')))
            l = int(len(futureLightHistory)/30)
            for i in range (0,l):
                t = simStartTime.addSecs(1800*i)
                f.write("{1} 00000{0}\r".format(futureLightHistory[30*i][0],t.toString('yyyyMMdd hhmm')))
            f.close

            
            self.graph.clear()
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
            
            self.label.setText("Simulation")
            
            i = 0
            for item in futureLightHistory:
                x = i
                y = 0
                heigh = 20

                if item[0] == 0:
                    self.graph.addLine(i,y,i,heigh)
                elif item[0] == 1:
                    R = 255 if item[1] > 0 else 0
                    G = 255 if item[2] > 0 else 0
                    B = 255 if item[3] > 0 else 0
                    W = 0 if item[4] > 0 else 255
                    colourPen = QtGui.QColor(R,G,B,W)
                    pen.setColor(colourPen)
                    self.graph.addLine(i,y,i,heigh,pen)
                    self.graph.addLine(i,y,i,y)
                    self.graph.addLine(i,heigh,i,heigh)
                    if item[5]>0:
                        self.graph.addLine(i,y,i,(1-item[5])*heigh)
                elif item[0] == -1:
                    self.graph.addLine(i,-20,i,heigh)
                    endTime = self.control.getEndExperimentTime()
                    endTime = endTime.toString("dd.MM.yy hh:mm")
                    text = self.graph.addText("Ends on {0}".format(endTime))
                    text.setPos(i,-22)
                    break
                ##initialize prevItem
                if i == 0:
                    prevItem = item[0]
                    self.graph.addLine(i,y,i,heigh)
                    startTime = simStartTime.toString("dd.MM.yy hh:mm")
                    text = self.graph.addText("Starts on {0}".format(startTime))
                    text.setPos(-160,0)
                ##add the hour when the condition change
                if prevItem != item[0]:
                    self.graph.addLine(i,y,i,heigh)
                    hour = simStartTime.addSecs(i*60)
                    hour = hour.toString("dd.MM.yy hh:mm")
                    text = self.graph.addText("{0}".format(hour))
                    text.setPos(i,-22)
                    
                prevItem = item[0]
                i += 1
                
                
            self.graphicsView.setScene(self.graph)
            self.graphicsView.show()
            #print("Sim ended")
            
            
            def closeEvent(self,event):
                #print (self.exp.getIsExperimentRunning())
                if self.exp.getIsExperimentRunning() == True:
                    #print("ignore")
                    event.ignore()
                else:
                    event.accept()
        else:
            self.label.setText("No Periods, please add one.")
                    
        
class DialogSelectIncubator(QtGui.QDialog):
     def __init__(self,parent=None):
        super(DialogSelectIncubator, self).__init__(parent)
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        
class DialogAddIncubator(QtGui.QDialog):
     def __init__(self,parent=None):
        super(DialogAddIncubator, self).__init__(parent)
        self.addDialog = Ui_AddDialog()
        self.addDialog.setupUi(self)

def main():
    app = QtGui.QApplication(sys.argv)
    LedController = ControlMainWindow()
    LedController.show()
    app.aboutToQuit.connect(LedController.stopExperiment)
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()