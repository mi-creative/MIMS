from PyQt5 import QtWidgets
from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt

import re

import physicsGenerator.topologyGenerator
import ext.topoTab

class createTopo(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        # uic.loadUi('ui/topoGenerator.ui', self)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.tabWidget = QtWidgets.QTabWidget()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tabWidget)
        self.setLayout(self.layout)

        self.stringTab = ext.topoTab.StringGenTab()
        self.tabWidget.addTab(self.stringTab, "String")

        self.stringTab.genScript.connect(self.onGeneratedStruct)

        self.meshTab = ext.topoTab.SquareMeshGenTab()
        self.tabWidget.addTab(self.meshTab, "Square Mesh")
        self.meshTab.genScript.connect(self.onGeneratedStruct)

        self.triTab = ext.topoTab.TriangleMeshGenTab()
        self.tabWidget.addTab(self.triTab, "Triangle Mesh")
        self.triTab.genScript.connect(self.onGeneratedStruct)

    def onGeneratedStruct(self, genString):
        # Grab the text cursor
        cursor = self.parent.textEdit.textCursor()
        cursor.insertText(genString)
        self.parent.textEdit.setTextCursor(cursor)
        self.close()
