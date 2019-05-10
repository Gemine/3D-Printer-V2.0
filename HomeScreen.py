import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFileDialog,QLabel,QGroupBox,QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import Qt,QtCore
import gcodesplit
import virtualPrinter
#from serialSendGcode import serialSendGcode
import threading
import time 
class App(QMainWindow,threading.Thread):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

        
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Main")
        self.tabs.addTab(self.tab2,"Config")
        
        # Create first tab
        self.tab1.layout = QGridLayout(self)
        
        # Create Load button
        self.loadButton = QPushButton("Load Gcode")
        self.loadButton.clicked.connect(self.loadGcode)
        self.tab1.layout.addWidget(self.loadButton,0,0)
        # Create process gcode button
        self.processGcodeButton = QPushButton("Process Gcode")
        self.tab1.layout.addWidget(self.processGcodeButton,0,1)
        self.processGcodeButton.clicked.connect(self.splitGcode)
        
        # Create Connect button
        self.connectButton = QPushButton("Connect")
        self.tab1.layout.addWidget(self.connectButton,1,0)
        self.connectButton.clicked.connect(self.connect)
        # Create Print button
        self.Print = QPushButton("Print")
        self.tab1.layout.addWidget(self.Print,1,1)
        self.Print.clicked.connect(self.machinePrint)
        
        #create pause button
        self.pauseButton = QPushButton("Pause")
        self.tab1.layout.addWidget(self.pauseButton,1,2)
        self.pauseButton.clicked.connect(self.pause)

        hBox = QHBoxLayout()
        groupBox = QGroupBox()
#create machine one label
        groupBox1 = QGroupBox("Machine One")
        hBox1 = QHBoxLayout()
        #create machine one port
        portOneButton = QLineEdit("COM7")
        self.portOne = "COM7"
        #create machine one baudrate
        baudrateOneButton = QLineEdit("115200")
        self.baudrateOne = 115200
        hBox1.addWidget(portOneButton)
        hBox1.addWidget(baudrateOneButton)
        groupBox1.setLayout(hBox1
        )
#create machine two label
        groupBox2 = QGroupBox("Machine Two")
        hBox2 = QHBoxLayout()
        #create machine two port
        portTwoButton = QLineEdit("COM8")
        self.portTwo = "COM8"
        #create machine two baudrate
        baudrateTwoButton = QLineEdit("115200")
        self.baudrateTwo = 115200

        hBox2.addWidget(portTwoButton)
        hBox2.addWidget(baudrateTwoButton)
        groupBox2.setLayout(hBox2)


        hBox.addWidget(groupBox1)
        hBox.addWidget(groupBox2)
        groupBox.setLayout(hBox)
        self.tab1.layout.addWidget(groupBox)
        #################
        self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
    @pyqtSlot()
    def loadGcode(self):
        print("load gcode file")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.gcode)", options=options)
        if fileName:
            print(fileName)
            self.gcodeDir = fileName
    @pyqtSlot()
    def connect(self):
        try:
            print("connect to machine")
            self.onePrinter = virtualPrinter.typeOnePrinter("nameOne","Gcode/one.gcode",self.portOne,self.baudrateOne)
            self.twoPrinter = virtualPrinter.typeTwoPrinter("nameTwo","Gcode/two.gcode",self.portTwo,self.baudrateTwo)

            # get gcode data 
            self.onePrinter.getGcodeData()
            self.twoPrinter.getGcodeData()


            # get friend printer
            self.onePrinter.getFirstFriendPrinter(self.twoPrinter)
            self.twoPrinter.getFirstFriendPrinter(self.onePrinter)

            # Connect One Printer
            self.onePrinter.connectToPrinter()
            #Connect Two Printer
            self.twoPrinter.connectToPrinter()

            print("Connect OK")
           
        except:
            print("can not connect to machine")
            print(Exception)

    def dowork(self):
        try:
            print("3D printer print")
            virtualPrinter.runningEvent.set()
            self.twoPrinter.start()
            self.onePrinter.start()
            self.twoPrinter.join()
            self.onePrinter.join()
            

        except:
            print("Connect before print")

    @pyqtSlot()
    def machinePrint(self):
        
        x = threading.Thread(target=self.dowork)
        x.start()

    @pyqtSlot()
    def splitGcode(self):
        try:
            gcodesplit.split(self.gcodeDir)
            print("Split OK")
        except:
            print("can not split gcode")
    @pyqtSlot()
    def pause(self):
        virtualPrinter.runningEvent.clear()
        print("pause")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())