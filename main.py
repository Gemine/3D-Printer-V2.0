import virtualPrinter
import threading
import time 
"""printerOne = virtualPrinter.typeOnePrinter()
printerOne.connectToPrinter()
printerOne.run()
for i in range(0):
    printerOne.getGcodeFileDir("Gcode/one")
    printerOne.getGcodeLine()
    printerOne.getPositionFromGcodeRecive()
    print(printerOne.PositionFromGcodeRecive)
    a = printerOne.caculateDistanceToPoint([0,0]) 
    b = printerOne.checkCollision(a)
    if not b :
        printerOne.updateCurrentPosition(printerOne.PositionFromGcodeRecive)
        print("current")
        print(printerOne.currentPosition)
    printerOne.increaseOrderGcodeLine()"""
#################### Config for Printer One #############
# Name for Printer 1
nameOne = "onePrinter"
# Gcode file direction
gcodeOneDir = "Gcode/one.gcode"
# Serial connection port and baudrate
portOne = 'COM7'
baudrateOne = 115200
#=========================================================


##################### Config for printer two  ################
#Name for Printer 2
nameTwo = "twoPrinter"
# Gcode file direction
gcodeTwoDir = "Gcode/two.gcode"
# Serial connection port and baudrate
portTwo = 'COM8'
baudrateTwo = 115200

#=========================================================

onePrinter = virtualPrinter.typeOnePrinter(nameOne,gcodeOneDir,portOne,baudrateOne)
twoPrinter = virtualPrinter.typeTwoPrinter(nameTwo,gcodeTwoDir,portTwo,baudrateTwo)

#get gcode data 
onePrinter.getGcodeData()
twoPrinter.getGcodeData()



onePrinter.getFirstFriendPrinter(twoPrinter)
twoPrinter.getFirstFriendPrinter(onePrinter)

#Connect One Printer
onePrinter.connectToPrinter()
#Connect Two Printer
twoPrinter.connectToPrinter()

#onePrinter.sendGcode('G28')
#twoPrinter.sendGcode('G28')
#time.sleep(5)
twoPrinter.start()
onePrinter.start()


twoPrinter.join()
onePrinter.join()


print(threading.enumerate())
