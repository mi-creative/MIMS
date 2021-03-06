import sys, os
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import pyqtSignal, QStringListModel

sys.path.append("..")

from ext import highlighter, createTopology, find
from physicsGenerator import physics2Faust,physicsGen
import physicsGenerator.phyDict as phyDict

version = "0.2"

if getattr(sys, 'frozen', False):
    # if you are running in a |PyInstaller| bundle
    uiDir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    uiDir = os.getcwd()

htmlDir = os.path.join(uiDir, 'html/')
iconDir = os.path.join(uiDir, 'icons/')
styleDir = os.path.join(uiDir, 'style/')
uiDir = os.path.join(uiDir, 'ui/')


class Main(QtWidgets.QMainWindow):

    updateModelStat = pyqtSignal()

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self,parent)
        uic.loadUi(uiDir+'mainWindow.ui', self)

        sshFile = styleDir + "darkstyle.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

        self.filename = ""
        self.compileTargetName=""

        self.changesSaved = True

        self.dict = ["none","param", "audioParam", "mass", "massG","osc","ground", "springDamper", "damper",
                     "spring", "nlSpring", "nlSpring2", "nlSpring3","nlPluck", "nlBow","contact",
                     "posInput","frcInput","posOutput","frcOutput"]

        # Set the initial count for module types
        self.occurences = []

        for type in phyDict.all_modules:
            self.occurences.append(0)

        self.initUI()

    def initToolbar(self):

        self.newAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "new.png"),"New", self)
        self.newAction.setStatusTip("Create a new model description file.")
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "open.png"),"Open File", self)
        self.openAction.setStatusTip("Open an existing model description file.")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "save.png"),"Save File", self)
        self.saveAction.setStatusTip("Save model description file.")
        #self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.saveAsAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "save.png"),"Save File As", self)
        self.saveAsAction.setStatusTip("Save model description file As...")
        self.saveAsAction.setShortcut("Ctrl+S")
        self.saveAsAction.triggered.connect(self.saveAs)

        self.quitAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "icon.png"),"Quit", self)
        self.quitAction.setStatusTip("Leave the application.")
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.triggered.connect(self.quit)


        self.compileAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "2gen.png"),"Compile into Gen", self)
        self.compileAction.setStatusTip("Compile the model file into Gen DSP Code")
        self.compileAction.setShortcut("Ctrl+G")
        self.compileAction.triggered.connect(self.compile)

        self.faustCompileAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "2faust.png"),"Compile into Faust DSP", self)
        self.faustCompileAction.setStatusTip("Compile the model file into Faust DSP Code")
        self.faustCompileAction.setShortcut("Ctrl+D")
        self.faustCompileAction.triggered.connect(self.faustCompile)

        self.cutAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "cut.png"),"Cut to clipboard", self)
        self.cutAction.setStatusTip("Cut text into clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.textEdit.cut)

        self.copyAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "copy.png"),"Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.textEdit.copy)

        self.pasteAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "paste.png"), "Paste from clipboard", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.textEdit.paste)

        self.commentAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "comment.png"), "Comment Line / Selection", self)
        self.commentAction.setStatusTip("Comment line or selection")
        self.commentAction.setShortcut("Ctrl+/")
        self.commentAction.triggered.connect(self.comment)

        self.uncommentAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "uncomment.png"), "Uncomment Line / Selection", self)
        self.uncommentAction.setStatusTip("Uncomment line or selection")
        self.uncommentAction.setShortcut("Ctrl+/")
        self.uncommentAction.triggered.connect(self.uncomment)

        self.undoAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "undo.png"), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.textEdit.undo)

        self.redoAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "redo.png"), "Redo last undone thing", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.textEdit.redo)

        self.findAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "find.png"), "Find/Replace", self)
        self.findAction.setStatusTip("Find and replace elements in model script")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        self.genAction = QtWidgets.QAction(QtGui.QIcon(iconDir + "generate.png"), "Generate Structure", self)
        self.genAction.setStatusTip("Generate a structure")
        self.genAction.setShortcut("Ctrl+U")
        self.genAction.triggered.connect(createTopology.createTopo(self).show)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.commentAction)
        self.toolbar.addAction(self.uncommentAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(self.genAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.compileAction)
        self.toolbar.addAction(self.faustCompileAction)

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
        file.addAction(self.quitAction)

        comp.addAction(self.compileAction)
        comp.addAction(self.faustCompileAction)
        comp.addAction(self.genAction)


    def initUI(self):
        self.textEdit.setTabStopWidth(33)
        self.setWindowIcon(QtGui.QIcon(iconDir + "icon.png"))

        self.textEdit.cursorPositionChanged.connect(self.cursorPos)
        self.textEdit.textChanged.connect(self.modelStatistics)
        self.textEdit.setFont(QtGui.QFont('SansSerif', 14))

        self.textEdit.setAcceptRichText(False)
        self.textEdit.setPlaceholderText("This model is empty: start scripting!")

        self.highlight = highlighter.ModelHighlighter(self.textEdit.document())

        self.initToolbar()
        # self.initFormatbar()
        self.initMenubar()

        self.statusbar = self.statusBar()

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1000,700)

        self.setWindowTitle("Mass Interaction Model Scripter - MIMS v" + version)

        self.textEdit.textChanged.connect(self.changed)

        self.updateModelStat.connect(self.displayModelStats)

        self.compileButton.clicked.connect(self.compile)
        self.faustButton.clicked.connect(self.faustCompile)


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

        if self.filename == "":
            return

        if not self.filename.endswith(".mdl"):
            self.filename += ".mdl"

        with open(self.filename, "wt") as file:
            file.write(self.textEdit.toPlainText())

        self.changesSaved = True

    # Factorise this with the regular save button !
    def saveAs(self):
        # PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.filename = QtWidgets.QFileDialog.getSaveFileName(self,
                                                'Save File')[0]
        if not self.filename.endswith(".mdl"):
            self.filename += ".mdl"
        with open(self.filename, "wt") as file:
            file.write(self.textEdit.toPlainText())

        self.changesSaved = True

    def quit(self):
        self.close()

    def compile(self):
        # PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.compileTargetName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              'Compile Model')[0]

        if self.compileTargetName == "":
            self.statusbar.showMessage("The gen~ code was not not generated.")
            return

        if not self.compileTargetName.endswith(".gendsp"):
            self.compileTargetName += ".gendsp"

        phyGen = physicsGen.PhysicsGenParser()
        err, s = phyGen.parseModel(self.textEdit.toPlainText(),True)


        if err:
            popup = QtWidgets.QMessageBox(self)
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("Error during model compilation: " + str(err))
            popup.setInformativeText(s + '\n' + 'Aborting compilation.')
            popup.setStandardButtons(QtWidgets.QMessageBox.Ok)
            popup.setDefaultButton(QtWidgets.QMessageBox.Ok)
            answer = popup.exec_()
            return


        phyGen.createDspObj(self.compileTargetName)


    def faustCompile(self):
        # PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.compileTargetName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                              'Compile Model')[0]

        if self.compileTargetName == "":
            self.statusbar.showMessage("The FAUST code was not not generated.")
            return

        if not self.compileTargetName.endswith(".dsp"):
            self.compileTargetName += ".dsp"

        phyGen = physics2Faust.Physics2Faust()
        err, s = phyGen.parseModel(self.textEdit.toPlainText())

        if err:
            popup = QtWidgets.QMessageBox(self)
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("Error during model compilation: " + str(err))
            popup.setInformativeText(s + '\n' + 'Aborting compilation.')
            popup.setStandardButtons(QtWidgets.QMessageBox.Ok)
            popup.setDefaultButton(QtWidgets.QMessageBox.Ok)
            answer = popup.exec_()
            return

        with open(self.compileTargetName, "wt") as file:
            file.write(s)

        self.statusbar.showMessage("Created the following FAUST file: " + self.compileTargetName)

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
        if type in phyDict.all_modules:
            index = phyDict.all_modules.index(type)
        #if type in self.dict:
        #    index = self.dict.index(type)
        else:
            index = -1
        return index


    def helpDisplay(self, currentLine):
        typeIndex = self.parseLine(currentLine)
        # print('Type index: ' + str(typeIndex))
        if typeIndex >= 0:
            try:
                helpfile = htmlDir + phyDict.all_modules[typeIndex] + '-doc.html'
                #helpfile = htmlDir + self.dict[typeIndex] +'-doc.html'
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
                s += "<b>" + phyDict.all_modules[i] + "</b> : " + str(occ) + "<br>"
                #s += "<b>" + self.dict[i] + "</b> : " + str(occ) + "<br>"
        self.mdlLabel.setText(s)

    def changed(self):
        self.changesSaved = False

    def closeEvent(self, event):
        if self.changesSaved:
            event.accept()
        else:
            if (self.textEdit.toPlainText() == ""):
                return
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
                self.saveAs()
            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

    # def dragEnterEvent(self, e):
    #     print(e)
    #     if e.mimeData().hasText():
    #         e.accept()
    #     else:
    #         e.ignore()
    #
    # def dropEvent(self, e):
    #     self.textEdit.setText(e.mimeData().text())


def main():

    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
