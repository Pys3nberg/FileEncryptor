from PyQt4 import QtCore, QtGui, uic
import sys

class MainGui(QtGui.QMainWindow):


    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        uic.loadUi('BaseGUI.ui', self)
        self.show()












if __name__ == '__main__':

    app  = QtGui.QApplication(sys.argv)
    window = MainGui()
    sys.exit(app.exec_())
