from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

import physicsGenerator.topologyGenerator

# should probably make this an abstract class!
class genericTopoWidget( QtWidgets.QWidget):
    genScript = pyqtSignal("QString")
    def __init__(self, name = "", parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.parent = parent
        self.strName = name

        # state values for string generation
        self.indexMassParam = False
        self.indexStiffnessParam = False
        self.indexDampingParam = False
        self.indexZoscParam = False
        self.hasInternalDamping = False

        self.initUI()


    def initUI(self):

        self.vLayout = QtWidgets.QVBoxLayout()
        self.hLayout = QtWidgets.QHBoxLayout()

        self.layout = QtWidgets.QGridLayout()

        self.type = QtWidgets.QLabel(self.strName)
        self.name = QtWidgets.QLineEdit()

        self.hLayout.addWidget(self.type,0)
        self.hLayout.addWidget(self.name,1)

        self.nameWidget = QtWidgets.QWidget()
        self.nameWidget.setLayout(self.hLayout)
        self.vLayout.addWidget(self.nameWidget, 0)

        # self.vLayout.addWidget(QtWidgets.QSplitter())

        self.layout.addWidget(QtWidgets.QLabel("Masses:"), 2, 0)
        self.layout.addWidget(QtWidgets.QLabel("Stiffness:"), 3, 0)
        self.layout.addWidget(QtWidgets.QLabel("Damping:"), 4, 0)

        self.zoscCB = QtWidgets.QCheckBox("Internal Damping?")
        self.layout.addWidget(self.zoscCB, 5, 0)

        self.mParam = QtWidgets.QDoubleSpinBox()
        self.mParam.setMinimum(0.000000000001)
        self.mParam.setDecimals(8)
        self.mParam.setValue(1.0)

        self.kParam = QtWidgets.QDoubleSpinBox()
        self.kParam.setMinimum(0.)
        self.kParam.setDecimals(8)
        self.kParam.setValue(0.1)

        self.zParam = QtWidgets.QDoubleSpinBox()
        self.zParam.setDecimals(8)
        self.zParam.setValue(0.01)

        self.zoscParam = QtWidgets.QDoubleSpinBox()
        self.zoscParam.setDecimals(8)
        self.zoscParam.setValue(0.0)
        self.zoscParam.setEnabled(False)

        self.layout.addWidget(self.mParam, 2, 1)
        self.layout.addWidget(self.kParam, 3, 1)
        self.layout.addWidget(self.zParam, 4, 1)
        self.layout.addWidget(self.zoscParam, 5, 1)

        self.mIndexed = QtWidgets.QCheckBox("indexed param")
        self.kIndexed = QtWidgets.QCheckBox("indexed param")
        self.zIndexed = QtWidgets.QCheckBox("indexed param")
        self.zoscIndexed = QtWidgets.QCheckBox("indexed param")

        self.layout.addWidget(self.mIndexed, 2, 2)
        self.layout.addWidget(self.kIndexed, 3, 2)
        self.layout.addWidget(self.zIndexed, 4, 2)
        self.layout.addWidget(self.zoscIndexed, 5, 2)

        self.mIndexName = QtWidgets.QLineEdit()
        self.kIndexName = QtWidgets.QLineEdit()
        self.zIndexName = QtWidgets.QLineEdit()
        self.zoscIndexName = QtWidgets.QLineEdit()
        self.mIndexName.setEnabled(False)
        self.kIndexName.setEnabled(False)
        self.zIndexName.setEnabled(False)
        self.zoscIndexName.setEnabled(False)

        self.layout.addWidget(self.mIndexName, 2, 3)
        self.layout.addWidget(self.kIndexName, 3, 3)
        self.layout.addWidget(self.zIndexName, 4, 3)
        self.layout.addWidget(self.zoscIndexName, 5, 3)

        self.gen = QtWidgets.QPushButton("Generate !")

        self.layout.addWidget(self.gen, 6, 3)

        gridWidget = QtWidgets.QWidget()
        gridWidget.setLayout(self.layout)
        self.vLayout.addWidget(gridWidget, 2)

        self.setLayout(self.vLayout)

        self.mIndexed.stateChanged.connect(self.onMassParamState)
        self.kIndexed.stateChanged.connect(self.onStiffnessParamState)
        self.zIndexed.stateChanged.connect(self.onDampingParamState)
        self.zoscIndexed.stateChanged.connect(self.onIntDampingParamState)

        self.name.textChanged.connect(self.onNameChanged)
        self.zoscCB.stateChanged.connect(self.onIntDampingState)
        self.gen.clicked.connect(self.generateStructure)

    def onNameChanged(self, name):
        self.mIndexName.setText(name+"_M")
        self.kIndexName.setText(name + "_K")
        self.zIndexName.setText(name + "_Z")
        self.zoscIndexName.setText(name + "_Zosc")

    def onMassParamState(self, state):
        self.mIndexName.setEnabled(state)
        self.indexMassParam = state

    def onStiffnessParamState(self, state):
        self.kIndexName.setEnabled(state)
        self.indexStiffnessParam = state

    def onDampingParamState(self, state):
        self.zIndexName.setEnabled(state)
        self.indexDampingParam = state

    def onIntDampingParamState(self, state):
        self.zoscIndexName.setEnabled(state)
        self.indexZoscParam = state

    def onIntDampingState(self, state):
        self.zoscParam.setEnabled(state)
        self.hasInternalDamping = state

    def generateStructure(self):
        print("Nothing here yet")


class StringGenTab(genericTopoWidget):
    def __init__(self, parent=None):
        genericTopoWidget.__init__(self, "String", parent)
        self.initSpecificUI()

    def initSpecificUI(self):
        self.name.setText("str")

        self.specWidget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout()
        self.specWidget.setLayout(hLayout)

        self.strLen = QtWidgets.QSpinBox()
        self.strLen.setMinimum(1)
        self.strLen.setMaximum(1000)
        self.strLen.setValue(10)

        hLayout.addWidget(QtWidgets.QLabel("Length:"),0)
        hLayout.addWidget(self.strLen, 1)
        self.vLayout.addWidget(self.specWidget)

    def generateStructure(self):
        mName = None
        kName = None
        zName = None
        zoscName = None

        if self.indexMassParam:
            mName = self.mIndexName.text()
        if self.indexStiffnessParam:
            kName = self.kIndexName.text()
        if self.indexDampingParam:
            zName = self.zIndexName.text()
        if self.indexZoscParam:
            zoscName = self.zoscIndexName.text()

        genString = physicsGenerator.topologyGenerator.createString(self.strLen.value(),
                                      self.name.text(),
                                      self.mParam.value(),
                                      self.kParam.value(),
                                      self.zParam.value(),
                                      self.hasInternalDamping,
                                      self.zoscParam.value(),
                                      mName,
                                      kName,
                                      zName,
                                      zoscName)

        self.genScript.emit(genString)



class StiffStringGenTab(genericTopoWidget):
    def __init__(self, parent=None):
        genericTopoWidget.__init__(self, "StiffString", parent)
        self.initSpecificUI()

    def initSpecificUI(self):
        self.name.setText("stiff")

        self.specWidget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout()
        self.specWidget.setLayout(hLayout)

        self.strLen = QtWidgets.QSpinBox()
        self.strLen.setMinimum(1)
        self.strLen.setMaximum(1000)
        self.strLen.setValue(10)

        self.stiffParam = QtWidgets.QDoubleSpinBox()
        self.stiffParam.setMinimum(0.)
        self.stiffParam.setDecimals(10)
        self.stiffParam.setValue(0.1)

        self.stiffIndexName = QtWidgets.QLineEdit()
        self.stiffIndexed = QtWidgets.QCheckBox("indexed param")
        self.stiffIndexName.setEnabled(False)


        hLayout.addWidget(QtWidgets.QLabel("Length:"),0)
        hLayout.addWidget(self.strLen, 1)
        self.layout.addWidget(QtWidgets.QLabel("2nd order stiff:"))
        self.layout.addWidget(self.stiffParam)
        self.layout.addWidget(self.stiffIndexed)
        self.layout.addWidget(self.stiffIndexName)

        self.stiffIndexed.stateChanged.connect(self.onStiff2ParamState)

        self.name.textChanged.connect(self.extraOnNameChanged)


        self.vLayout.addWidget(self.specWidget)

    def extraOnNameChanged(self, name):
        self.stiffIndexName.setText(name + "_K2")

    def onStiff2ParamState(self, state):
        self.stiffIndexName.setEnabled(state)
        self.stiffIndexed = state

    def generateStructure(self):
        mName = None
        kName = None
        zName = None
        zoscName = None
        stiffName = None

        if self.indexMassParam:
            mName = self.mIndexName.text()
        if self.indexStiffnessParam:
            kName = self.kIndexName.text()
        if self.indexDampingParam:
            zName = self.zIndexName.text()
        if self.indexZoscParam:
            zoscName = self.zoscIndexName.text()
        #if self.indexZoscParam:
        stiffName = self.stiffIndexName.text()

        genString = physicsGenerator.topologyGenerator.createStiffString(self.strLen.value(),
                                      self.name.text(),
                                      self.mParam.value(),
                                      self.kParam.value(),
                                      self.zParam.value(),
                                      self.stiffParam.value(),
                                      self.hasInternalDamping,
                                      self.zoscParam.value(),
                                      mName,
                                      kName,
                                      zName,
                                      stiffName,
                                      zoscName)

        self.genScript.emit(genString)



class SquareMeshGenTab(genericTopoWidget):
    def __init__(self, parent=None):
        genericTopoWidget.__init__(self, "Square Mesh", parent)
        self.initSpecificUI()

    def initSpecificUI(self):
        self.name.setText("mesh")

        self.specWidget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout()
        self.specWidget.setLayout(hLayout)

        self.meshX = QtWidgets.QSpinBox()
        self.meshX.setMinimum(1)

        self.meshY = QtWidgets.QSpinBox()
        self.meshY.setMinimum(1)

        hLayout.addWidget(QtWidgets.QLabel("Length:"),0)
        hLayout.addWidget(self.meshX, 1)
        hLayout.addWidget(QtWidgets.QLabel("Width:"), 2)
        hLayout.addWidget(self.meshY, 3)
        self.vLayout.addWidget(self.specWidget)

    def generateStructure(self):
        mName = None
        kName = None
        zName = None
        zoscName = None

        if self.indexMassParam:
            mName = self.mIndexName.text()
        if self.indexStiffnessParam:
            kName = self.kIndexName.text()
        if self.indexDampingParam:
            zName = self.zIndexName.text()
        if self.indexZoscParam:
            zoscName = self.zoscIndexName.text()

        genMesh = physicsGenerator.topologyGenerator.createMembrane(self.meshX.value(),
                                                                    self.meshY.value(),
                                      self.name.text(),
                                      self.mParam.value(),
                                      self.kParam.value(),
                                      self.zParam.value(),
                                      self.hasInternalDamping,
                                      self.zoscParam.value(),
                                      mName,
                                      kName,
                                      zName,
                                      zoscName)

        self.genScript.emit(genMesh)



class TriangleMeshGenTab(genericTopoWidget):
    def __init__(self, parent=None):
        genericTopoWidget.__init__(self, "TriangleMesh", parent)
        self.initSpecificUI()

    def initSpecificUI(self):
        self.name.setText("tri")

        self.specWidget = QtWidgets.QWidget()
        hLayout = QtWidgets.QHBoxLayout()
        self.specWidget.setLayout(hLayout)

        self.strLen = QtWidgets.QSpinBox()
        self.strLen.setMinimum(1)
        self.strLen.setValue(10)

        hLayout.addWidget(QtWidgets.QLabel("Length:"),0)
        hLayout.addWidget(self.strLen, 1)
        self.vLayout.addWidget(self.specWidget)

    def generateStructure(self):
        mName = None
        kName = None
        zName = None
        zoscName = None

        if self.indexMassParam:
            mName = self.mIndexName.text()
        if self.indexStiffnessParam:
            kName = self.kIndexName.text()
        if self.indexDampingParam:
            zName = self.zIndexName.text()
        if self.indexZoscParam:
            zoscName = self.zoscIndexName.text()

        genTriangle = physicsGenerator.topologyGenerator.createTriangleMembrane(self.strLen.value(),
                                      self.name.text(),
                                      self.mParam.value(),
                                      self.kParam.value(),
                                      self.zParam.value(),
                                      self.hasInternalDamping,
                                      self.zoscParam.value(),
                                      mName,
                                      kName,
                                      zName,
                                      zoscName)

        self.genScript.emit(genTriangle)