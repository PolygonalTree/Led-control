from model import *
import pickle
from PySide2 import QtCore, QtGui, QtSql
actualTime = QtCore.QDateTime.currentDateTime()

f = open("../../experiments_saved/text3.exp", "rb")
exp = pickle.load(f)
exp.experiment[0].dateStartTime = actualTime.date().addDays(-5)
print(exp.experiment[0].dateStartTime)
print(exp.experiment[0].dateEndTime)
f.close()

with open("../../experiments_saved/text2.exp", "wb") as f:
    pickle.dump(exp, f, -1)