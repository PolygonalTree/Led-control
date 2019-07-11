from model import *
import pickle
from PySide2 import QtCore, QtGui, QtSql
actualTime = QtCore.QDateTime.currentDateTime()

import PySide2
import sys
sys.modules["PySide"] = PySide2
import os
p="/run/media/luis/food/experiments_saved/"
exp_to_save = []
for file in os.listdir(p):
    print(file)
    f = open(os.path.join(p,file), "rb")
    exp = pickle.load(f)
    for e in exp.experiment:
        e.dateStartTime = actualTime.date().addDays(1)
        e.dateEndTime = actualTime.date().addDays(1)
    exp_to_save.append((file,e))
    f.close()

from model import *
import pickle
from PySide2 import QtCore, QtGui, QtSql
sys.modules["PySide"] = ""
import json

for p,e in exp_to_save:
    with open("../../experiments_saved/{}".format(p), "wb") as f:
        json.dumps(e)