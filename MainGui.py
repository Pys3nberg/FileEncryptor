from PyQt4 import QtCore, QtGui, uic
import sys, encryption

class MainGui(QtGui.QMainWindow):


    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        uic.loadUi('BaseGUI.ui', self)
        self.statusBar()
        self.EncBut.clicked.connect(self.encrypt)
        self.DecBut.clicked.connect(self.decrypt)
        self.show()

    def select_files(self, message):

        return QtGui.QFileDialog.getOpenFileNames(self, message)

    def encrypt(self):

        if len(self.passEdit.text()) > 0:
            fileNames = self.select_files('Hello please select files to encrypt')
            inc = 100//len(fileNames)
            completed = 0
            self.setStatusTip('Encrypting files...')
            for f in fileNames:
                encryption.encrypt_file(self.passEdit.text(), f)
                completed += inc
                self.statusLabel.setText('Encryption ' + f+'...')
                self.progressBar.setValue(completed)
            self.progressBar.setValue(100)
            self.setStatusTip('Encryption complete')

        else:
            print('please enter a password')
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You must enter a password')
            msgBox.exec_()

    def decrypt(self):
        if len(self.passEdit.text()) > 0:
            fileNames = self.select_files('Hello please select files to decrypt')
            inc = 100//len(fileNames)
            completed = 0
            self.setStatusTip('Decrypting files...')
            for f in fileNames:
                encryption.decrypt_file(self.passEdit.text(), f)
                completed += inc
                self.statusLabel.setText('Decrypting ' + f+'...')
                self.progressBar.setValue(completed)
            self.progressBar.setValue(100)
            self.setStatusTip('Decryption complete')



if __name__ == '__main__':

    app  = QtGui.QApplication(sys.argv)
    window = MainGui()
    sys.exit(app.exec_())
