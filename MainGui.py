from PyQt4 import QtCore, QtGui, uic
import sys, functools

class MainGui(QtGui.QMainWindow):


    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        uic.loadUi('BaseGUI.ui', self)
        self.statusBar()
        self.EncBut.clicked.connect(self.encrypt)
        self.DecBut.clicked.connect(self.decrypt)
        self.show()

    def select_files(self, message):

        fileNames = QtGui.QFileDialog.getOpenFileNames(self, message)
        print(fileNames)

    def encrypt(self):

        if len(self.passEdit.text()) > 0:
            self.select_files('Hello please select files to encrypt')
        else:
            print('please enter a password')
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You must enter a password')
            msgBox.exec_()

    def decrypt(self):

        self.select_files('Hello please select files to decrypt')



if __name__ == '__main__':

    app  = QtGui.QApplication(sys.argv)
    window = MainGui()
    sys.exit(app.exec_())
