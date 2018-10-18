import sys, os
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import pyqtSignal, QStringListModel

sys.path.append("..")

from ext import *
from physicsGenerator import *

version = "0.1"


class Main(QtWidgets.QMainWindow):

    updateModelStat = pyqtSignal()

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self,parent)
        uic.loadUi('ui/mainWindow.ui', self)

        self.filename = ""
        self.compileTargetName=""

        self.changesSaved = True

        self.dict = ["param","mass", "massG","osc","ground",
                     "spring","nlSpring","nlPluck", "nlBow","detent",
                     "posInput","frcInput","posOutput","frcOutput"]

        # Set the initial count for module types
        self.occurences = []
        for type in self.dict:
            self.occurences.append(0)

        self.initUI()

    def initToolbar(self):

        self.newAction = QtWidgets.QAction(QtGui.QIcon("icons/new.png"),"New", self)
        self.newAction.setStatusTip("Create a new model description file.")
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtWidgets.QAction(QtGui.QIcon("icons/open.png"),"Open File", self)
        self.openAction.setStatusTip("Open an existing model description file.")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon("icons/save.png"),"Save File", self)
        self.saveAction.setStatusTip("Save model description file.")
        #self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.saveAsAction = QtWidgets.QAction(QtGui.QIcon("icons/save.png"),"Save File As", self)
        self.saveAsAction.setStatusTip("Save model description file As...")
        self.saveAsAction.setShortcut("Ctrl+S")
        self.saveAsAction.triggered.connect(self.saveAs)


        self.compileAction = QtWidgets.QAction(QtGui.QIcon("icons/count.png"),"Compile into Gen", self)
        self.compileAction.setStatusTip("Compile the model file into Gen DSP Code")
        self.compileAction.setShortcut("Ctrl+G")
        self.compileAction.triggered.connect(self.faustCompile)

        self.cutAction = QtWidgets.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard", self)
        self.cutAction.setStatusTip("Cut text into clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.textEdit.cut)

        self.copyAction = QtWidgets.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.textEdit.copy)

        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("icons/paste.png"), "Paste from clipboard", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.textEdit.paste)

        self.commentAction = QtWidgets.QAction(QtGui.QIcon("icons/indent.png"), "Comment Line / Selection", self)
        self.commentAction.setStatusTip("Comment line or selection")
        self.commentAction.setShortcut("Ctrl+/")
        self.commentAction.triggered.connect(self.comment)

        self.uncommentAction = QtWidgets.QAction(QtGui.QIcon("icons/dedent.png"), "Uncomment Line / Selection", self)
        self.uncommentAction.setStatusTip("Uncomment line or selection")
        self.uncommentAction.setShortcut("Ctrl+/")
        self.uncommentAction.triggered.connect(self.uncomment)

        self.undoAction = QtWidgets.QAction(QtGui.QIcon("icons/undo.png"), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.textEdit.undo)

        self.redoAction = QtWidgets.QAction(QtGui.QIcon("icons/redo.png"), "Redo last undone thing", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.textEdit.redo)

        self.findAction = QtWidgets.QAction(QtGui.QIcon("icons/find.png"), "Find/Replace", self)
        self.findAction.setStatusTip("Find and replace elements in model script")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        self.genAction = QtWidgets.QAction(QtGui.QIcon("icons/find.png"), "Generate Structure", self)
        self.genAction.setStatusTip("Generate a structure")
        self.genAction.setShortcut("Ctrl+U")
        self.genAction.triggered.connect(createTopology.createTopo(self).show)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.commentAction)
        self.toolbar.addAction(self.uncommentAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(self.genAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.compileAction)

        self.addToolBarBreak()

    def initFormatbar(self):
        self.formatbar = self.addToolBar("Format")

    def initMenubar(self):
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        comp = menubar.addMenu("Compile")

        edit.addAction(self.copyAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.findAction)
        edit.addSeparator()

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addSeparator()

        edit.addAction(self.commentAction)
        edit.addAction(self.uncommentAction)

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.saveAsAction)

        comp.addAction(self.compileAction)
        comp.addAction(self.genAction)


    def initUI(self):
        self.textEdit.setTabStopWidth(33)
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

        self.textEdit.cursorPositionChanged.connect(self.cursorPos)
        self.textEdit.textChanged.connect(self.modelStatistics)
        self.textEdit.setFont(QtGui.QFont('SansSerif', 10))

        self.textEdit.setAcceptRichText(False)
        self.textEdit.setPlaceholderText("This model is empty: start scripting!")

        self.highlight = highlighter.ModelHighlighter(self.textEdit.document())

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        self.statusbar = self.statusBar()

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,900,600)

        self.setWindowTitle("Mass Interaction Model Scripter - MIMS v" + version)

        self.textEdit.textChanged.connect(self.changed)

        self.updateModelStat.connect(self.displayModelStats)
        self.compileButton.clicked.connect(self.faustCompile)


    def cursorPos(self):
        cursor = self.textEdit.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))
        self.helpDisplay(cursor.block().text())


    def new(self):
        spawn = Main(self)
        spawn.show()

    def open(self):

        # TODO: check for unsaved modifications !!

        # PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self,
                                            'Open File', '.',"(*.mdl)")[0]
        if self.filename:
            with open(self.filename,"rt") as file:
                self.textEdit.setText(file.read())
                # self.textEdit.selectAll()
                self.textEdit.setFont(QtGui.QFont('SansSerif', 11))
                # self.textEdit.unsetCursor()

    def save(self):
        if not self.filename:
            # PYQT5 Returns a tuple in PyQt5, we only need the filename
            self.filename = QtWidgets.QFileDialog.getSaveFileName(self,
                                                'Save File')[0]
        if not self.filename.endswith(".mdl"):
            self.filename += ".mdl"

        with open(self.filename, "wt") as file:
            file.write(self.textEdit.toPlainText())

    # Factorise this with the regular save button !
    def saveAs(self):
        # PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.filename = QtWidgets.QFileDialog.getSaveFileName(self,
                                                'Save File')[0]
        if not self.filename.endswith(".mdl"):
            self.filename += ".mdl"
        with open(self.filename, "wt") as file:
            file.write(self.textEdit.toPlainText())

    def compile(self):
        # PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.compileTargetName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              'Compile Model')[0]
        if not self.compileTargetName.endswith(".gendsp"):
            self.compileTargetName += ".gendsp"

        phyGen = physicsGen.PhysicsGenParser()
        phyGen.parseModel(self.textEdit.toPlainText(),True)
        phyGen.createDspObj(self.compileTargetName)
        print("This is where the model should be compiled.")

    def faustCompile(self):
        print("Compile into Faust Code")

        # PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.compileTargetName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              'Compile Model')[0]
        if not self.compileTargetName.endswith(".dsp"):
            self.compileTargetName += ".dsp"

        phyGen = physics2Faust.Physics2Faust()
        s = phyGen.parseModel(self.textEdit.toPlainText())

        with open(self.compileTargetName, "wt") as file:
            file.write(s)
        # phyGen.createDspObj(self.compileTargetName)

    def comment(self):
        cursor = self.textEdit.textCursor()

        if cursor.hasSelection():
            # store current line and block number
            temp = cursor.blockNumber()
            # move to end of selection
            cursor.setPosition(cursor.selectionEnd())
            # calculate range of selection
            diff = cursor.blockNumber() - temp

            # Iterate over lines
            for n in range(diff + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                # Insert comment sign and move back up
                cursor.insertText("## ")
                cursor.movePosition(QtGui.QTextCursor.Up)
        else:
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.insertText("## ")

    def uncomment(self):
        cursor = self.textEdit.textCursor()

        if cursor.hasSelection():
            # store current line and block number
            temp = cursor.blockNumber()
            # move to end of selection
            cursor.setPosition(cursor.selectionEnd())
            # calculate range of selection
            diff = cursor.blockNumber() - temp

            # Iterate over lines
            for n in range(diff + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                # Insert comment sign and move back up
                self.handleUncomment(cursor)
                cursor.movePosition(QtGui.QTextCursor.Up)
        else:
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            self.handleUncomment(cursor)

    def handleUncomment(self, cursor):
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        # Grab the current line
        line = cursor.block().text()
        # Otherwise, delete all spaces until a non-space character is met
        for char in line[:20]:
            if (char != " ") and (char != "#"):
                break
            cursor.deleteChar()

    def modelStatistics(self):
        text = self.textEdit.toPlainText()
        # Reset module counters
        for i in range (0,len(self.occurences)):
            self.occurences[i] = 0

        for line in text.splitlines():
            index = self.parseLine(line)
            if index != -1:
                self.occurences[index] += 1
        self.updateModelStat.emit()

    def parseLine(self,currentLine):
        index = -1
        if (len(currentLine.split(' ')) < 2):
            self.helpLabel.setText('')
            return index
        type = currentLine.split(' ')[1]
        if type in self.dict:
            index = self.dict.index(type)
        else:
            index = -1
        return index


    def helpDisplay(self, currentLine):
        typeIndex = self.parseLine(currentLine)
        # print('Type index: ' + str(typeIndex))
        if typeIndex >= 0:
            try:
                helpfile = 'html/'+ self.dict[typeIndex] +'-doc.html'
                # print(helpfile)
                with open(helpfile, "rt") as file:
                    self.helpLabel.setText(file.read())
            except Exception as e:
                # print("Couldn't open help file.")
                self.helpLabel.setText("")
        else:
            return

    def displayModelStats(self):
        s = ""
        for i, occ in enumerate(self.occurences):
            if occ > 0:
                s += "<b>" + self.dict[i] + "</b> : " + str(occ) + "<br>"
        self.mdlLabel.setText(s)

    def changed(self):
        self.changesSaved = False

    def closeEvent(self, event):
        if self.changesSaved:
            event.accept()
        else:
            popup = QtWidgets.QMessageBox(self)
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("The document has been modified")
            popup.setInformativeText("Do you want to save your changes?")
            popup.setStandardButtons(QtWidgets.QMessageBox.Save |
                                     QtWidgets.QMessageBox.Cancel |
                                     QtWidgets.QMessageBox.Discard)
            popup.setDefaultButton(QtWidgets.QMessageBox.Save)
            answer = popup.exec_()
            if answer == QtWidgets.QMessageBox.Save:
                self.save()
            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

def main():

    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
