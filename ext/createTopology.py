from PyQt5 import QtWidgets
from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt

import re

import physicsGenerator.topologyGenerator

class createTopo(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        uic.loadUi('ui/topoGenerator.ui', self)

        self.parent = parent

        # state values for string generation
        self.indexMassParam = False
        self.indexStiffnessParam = False
        self.indexDampingParam = False
        self.indexZoscParam = False


        self.hasInternalDamping = False

        self.initUI()

        self.name.textChanged.connect(self.onNameChanged)

    def initUI(self):
        print("stuff")

        self.name.setText("str")

        self.mParamN.setEnabled(False)
        self.kParamN.setEnabled(False)
        self.zParamN.setEnabled(False)
        self.zoscParamN.setEnabled(False)
        self.paramZosc.setEnabled(False)

        self.mCB.stateChanged.connect(self.onMassParamState)
        self.kCB.stateChanged.connect(self.onStiffnessParamState)
        self.zCB.stateChanged.connect(self.onDampingParamState)
        self.zoscCB.stateChanged.connect(self.onIntDampingParamState)

        self.intDmp.stateChanged.connect(self.onIntDampingState)

        self.genString.clicked.connect(self.generateStructure)

    def onNameChanged(self, name):
        self.mParamN.setText(name+"_M")
        self.kParamN.setText(name + "_K")
        self.zParamN.setText(name + "_Z")
        self.zoscParamN.setText(name + "_Zosc")

    def onMassParamState(self, state):
        self.mParamN.setEnabled(state)
        self.indexMassParam = state

    def onStiffnessParamState(self, state):
        self.kParamN.setEnabled(state)
        self.indexStiffnessParam = state

    def onDampingParamState(self, state):
        self.zParamN.setEnabled(state)
        self.indexDampingParam = state

    def onIntDampingParamState(self, state):
        self.zoscParamN.setEnabled(state)
        self.indexZoscParam = state

    def onIntDampingState(self, state):
        self.paramZosc.setEnabled(state)
        self.hasInternalDamping = state

    def generateStructure(self):
        mName = None
        kName = None
        zName = None
        zoscName = None

        if self.indexMassParam:
            mName = self.mParamN.text()
        if self.indexStiffnessParam:
            kName = self.kParamN.text()
        if self.indexDampingParam:
            zName = self.zParamN.text()
        if self.indexZoscParam:
            zoscName = self.zoscParamN.text()


        genString = physicsGenerator.topologyGenerator.createString(self.strLength.value(),
                                      self.name.text(),
                                      self.paramM.value(),
                                      self.paramK.value(),
                                      self.paramZ.value(),
                                      self.hasInternalDamping,
                                      self.paramZosc.value(),
                                      mName,
                                      kName,
                                      zName,
                                      zoscName)

        # Grab the text cursor
        cursor = self.parent.textEdit.textCursor()
        cursor.insertText(genString)
        self.parent.textEdit.setTextCursor(cursor)

        self.close()

# def createString(size, name, M, K, Z, hasZosc, Zosc,
#                  mParamName=None, kParamName=None, zParamName=None, zoscParamName=None):
#
