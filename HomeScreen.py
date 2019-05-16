import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFileDialog,QLabel,QGroupBox,QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,QSize
from PyQt5 import Qt,QtCore
import gcodesplit
import virtualPrinter
#from serialSendGcode import serialSendGcode
import threading
import time 
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'M3 - 3D Printer Control'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        
        self.setIconSize(QSize(1,1))
        self.setWindowIcon(QIcon("Media/icon/1024px-M3_icon.svg.png"))
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
        # Create Gcode File Dir textbox
        self.gcodeDirTextBox = QLabel("Load Gcode file")
        self.gcodeDirTextBox.setAlignment(Qt.Qt.AlignCenter)
        self.tab1.layout.addWidget(self.gcodeDirTextBox,0,1,1,2)
        
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
#create machine group box
        hBox = QGridLayout()
        groupBox = QGroupBox()
#create input command for both machine
        #both input group box
        generalInputGroupBox = QGroupBox("Send To Both")
        generalInputGroupBoxLayout = QGridLayout()
        #command input box
        self.generalInputCommandBox = QLineEdit("SEND TO BOTH")
        #Send button
        generalInputSendButton = QPushButton("SEND")
        generalInputSendButton.clicked.connect(self.sendToALL)

        generalInputGroupBoxLayout.addWidget(self.generalInputCommandBox,0,0,1,2)
        generalInputGroupBoxLayout.addWidget(generalInputSendButton,0,2)
        generalInputGroupBox.setLayout(generalInputGroupBoxLayout)

#create machine one group
        groupBox1 = QGroupBox("Machine One")
        hBox1 = QGridLayout()
        #create machine one port8
        self.portOneButton = QLineEdit("COM7")
        self.portOne = "COM7"
        self.portOneButton.textChanged.connect(self.updatePortName)
        #create machine one baudrate
        baudrateOneButton = QLineEdit("115200")
        self.baudrateOne = 115200
        #create machine one send comman box
        self.oneInputCommanBox = QLineEdit("SEND TO ONE")
        oneInputSendButton = QPushButton("SEND")
        oneInputSendButton.clicked.connect(self.sendToOne)

        hBox1.addWidget(self.portOneButton,0,0)
        hBox1.addWidget(baudrateOneButton,0,1)
        hBox1.addWidget(self.oneInputCommanBox,1,0,1,2)
        hBox1.addWidget(oneInputSendButton,1,3)
        groupBox1.setLayout(hBox1)
#create machine two group
        groupBox2 = QGroupBox("Machine Two")
        hBox2 = QGridLayout()
        #create machine two port
        self.portTwoButton = QLineEdit("COM8")
        self.portTwo = "COM8"
        self.portTwoButton.textChanged.connect(self.updatePortName)
        
        #create machine two baudrate
        baudrateTwoButton = QLineEdit("115200")
        self.baudrateTwo = 115200
        #create machine one send comman box
        self.twoInputCommanBox = QLineEdit("SEND TO TWO")
        twoInputSendButton = QPushButton("SEND")
        twoInputSendButton.clicked.connect(self.sendToTwo)


        hBox2.addWidget(self.portTwoButton,0,0)
        hBox2.addWidget(baudrateTwoButton,0,1)
        hBox2.addWidget(self.twoInputCommanBox,1,0,1,2)
        hBox2.addWidget(twoInputSendButton,1,3)
        groupBox2.setLayout(hBox2)


        hBox.addWidget(generalInputGroupBox,0,0,1,2)
        hBox.addWidget(groupBox1,1,0)
        hBox.addWidget(groupBox2,1,1)
        groupBox.setLayout(hBox)
        self.tab1.layout.addWidget(groupBox,2,0,1,3)
        #################
        self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)




################################## ALL SLOT HERE ####################################################

    @pyqtSlot()
    def loadGcode(self):
        print("load gcode file")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.gcode)", options=options)
        if fileName:
            print(fileName)
            self.gcodeDir = fileName
            self.gcodeDirTextBox.setText(fileName)
        self.splitGcode()
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
    def updatePortName(self):
        self.portOne = str(self.portOneButton.text())
        self.portTwo = str(self.portTwoButton.text())
        print(self.portOne,self.portTwo)

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

<<<<<<< HEAD
    def doSendToAll(self):
=======
    def sendToALL(self):
>>>>>>> db13ff960a5b7efd2ec70ec76de2352535f6d75e
        try:
            self.twoPrinter.sendGcode(str(self.generalInputCommandBox.text()))
            self.onePrinter.sendGcode(str(self.generalInputCommandBox.text()))
        except:
            print("Can not send to all")
<<<<<<< HEAD
    
    def sendToALL(self):
        threading.Thread(target=self.doSendToAll).start()
=======
>>>>>>> db13ff960a5b7efd2ec70ec76de2352535f6d75e

    def sendToOne(self):
        try:
            self.onePrinter.sendGcode(str(self.oneInputCommandBox.text()))
        except:
            print("Can not send to one")
<<<<<<< HEAD
=======
            App.statusBar().showMessage('Message in statusbar.')
>>>>>>> db13ff960a5b7efd2ec70ec76de2352535f6d75e
    def sendToTwo(self):
        try:
            self.twoPrinter.sendGcode(str(self.twoInputCommandBox.text()))
        except:
            print("Can not send to two")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())