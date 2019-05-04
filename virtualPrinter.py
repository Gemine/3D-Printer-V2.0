import threading
import re
import math
import os
import sys
import time

from serialSendGcode import serialSendGcode
try:
	import serial	# Import the pySerial modules.
except:
	print('You do not have pySerial installed, which is needed to control the serial port.')
	print('Information on pySerial is at:\nhttp://pyserial.wiki.sourceforge.net/pySerial')

################# ALL EVENT HERE ########################
priorityEvent = threading.Event()
comeBackEvent = threading.Event()
reachPriorityPosition = threading.Event()

priorityEvent.clear()
comeBackEvent.clear()
reachPriorityPosition.clear()
#########################################################

################# ALL LOCK HERE ########################
lockOne = threading.Lock()
lockTwo = threading.Lock()
#########################################################

class virtualPrinter(threading.Thread):
	"""docstring for virtualPrinter
	Mainly function:
	- Read Gcode file
	- Get Gcode from file
	- Get position from Gcode
	- Caculate distance from point to point
	- Check whether collision will happen
	- Update current position of machine
	- Increase number Gcode Line
	- Pause
	- Parking and come back nozzle
	- Connect to real machine
	- Send Gcode	
	"""
	################### virtualPrinter Variable ######################
	dirGcodeFile = ""
	gcodeData = []
	gcodeDataLen = 0
	numberOfGcodeLine = 0
	orderGcodeLine = 0
	gCodeRecive = ""
	gCodeSend = ""
	PositionFromGcodeRecive = [0,0]
	currentPosition = [0,0]
	numberOfLayer = 1
	zPosition = 0
	connection = None
	port = "COM1"
	baudrate = 115200
	###################################################################
	def __init__(self,name,gcodeFileDir,serialPort,baudrate):
		threading.Thread.__init__(self)
		self.name = name
		self.dirGcodeFile = gcodeFileDir
		self.port = serialPort
		self.baudrate = baudrate
		pass
	
	def run(self):
		#run the machine
		pass


	#def getGcodeFileDir(self,filedir):
		#self.dirGcodeFile = filedir
		#print("Gcode file is in: " + self.dirGcodeFile)
	def getGcodeData(self):
		try:
			file = open(self.dirGcodeFile)
			self.gcodeData = file.readlines()
			self.gcodeDataLen = len(self.gcodeData)-1
			file.close()
		except:
			print("Some thing went wrong with read file")
	def getGcodeLine(self):
		self.gCodeRecive = self.gcodeData[self.orderGcodeLine]


	def num(self,s):
		try:
			return int(s)
		except ValueError:
			return float(s)

	def getNumberOfGcodeLine(self):
		self.gcodeDataLen = len(self.gcodeData)
		pass
	
	def getZPosition(self,Gcode):
		a = re.search(r"\bZ(\d*.\d*)",Gcode)
		return a[1]
	def getPositionFromGcodeRecive(self):
		try:
			Gcode = re.split(r"\s",self.gCodeRecive)
		except:
			print("Dont have Gcode")
		if len(Gcode) > 3 and (Gcode[0] == "G1" or Gcode[0] == "G0"):
			if Gcode[1][0] == 'X':
				self.PositionFromGcodeRecive[0] = self.num(Gcode[1][1:])
			if Gcode[2][0] == 'Y':
				self.PositionFromGcodeRecive[1] = self.num(Gcode[2][1:])
		if 'Z' in Gcode:
			#get Z variale
			zData = self.getZPosition(self.gCodeRecive)
			#compare to current z
			if float(zData[1]) > self.zPosition:
				self.numberOfLayer = self.numberOfLayer + 1
				self.zPosition = float(zData[1])
			elif float(zData[1]) < self.zPosition:
				self.numberOfLayer = self.numberOfLayer - 1
				self.zPosition = float(zData[1])
			else:
				self.zPosition = float(zData[1])
		return self.PositionFromGcodeRecive

	def caculateDistanceToPoint(self,point):
		X_distance = math.fabs(self.PositionFromGcodeRecive[0] - point[0])
		Y_distance = math.fabs(self.PositionFromGcodeRecive[1] - point[1])
		#distance = math.sqrt((X_distance*X_distance+Y_distance*Y_distance))
		return [X_distance,Y_distance]
	def checkCollision(self,distanceXY):
		result = False
		if distanceXY[1] < 100:
    			result = True
		return result
	def updateCurrentPosition(self,position):
			self.currentPosition = position
	
	def getCurrentPosition(self):
		return self.currentPosition

	def increaseOrderGcodeLine(self):
		self.orderGcodeLine = self.orderGcodeLine + 1
	def pause(self):
		#send Gcode pause
		pass
	def parking(self):
		# M125 or M27
		self.sendGcode("G1 X200 Y220")
		self.sendGcode("M400")
	
	def comeBack(self):
		self.sendGcode("G0 ")
	def connectToPrinter(self):
		self.connection = serialSendGcode(self.port,self.baudrate,True)
		#wait for 5 second
		time.sleep(1)
		self.connection.read('M301')
	
	def sendGcode(self,Gcode):
		# Write Gcode to machine
		self.connection.write(Gcode)

	def isPrioritysitutation(self):
		pass

	def goToPriorityPosition(self):
		pass
	
	def emitGoneToPriorityPosition(self):
		pass
	
	def isComeBackSituation(self):
		pass

	def wait(self):
		#send Stop Gcode
		pass
	
	def emitPriorityEvent(self):
		pass

	def isMachineReachPriorityPosition(self):
		pass
#########################################################



class typeOnePrinter(virtualPrinter):
	
	################### typeOnePrinter Variable ######################
	priority = False
	currentPosition = [200,220]
	dirGcodeFile = ""
	gcodeData = []
	gcodeDataLen = 0
	orderGcodeLine = 0
	gCodeRecive = ""
	gCodeSend = ""
	PositionFromGcodeRecive = currentPosition
	numberOfLayer = 1
	zPosition = 0
	connection = None
	port = "COM7"
	baudrate = 115200

	##################################################################

	def __init__(self,name,gcodeFileDir,serialPort,baudrate):
		virtualPrinter.__init__(self,name,gcodeFileDir,serialPort,baudrate)
		pass

	def getFirstFriendPrinter(self,printer):
		self.firstFriendPrinter = printer

	def isPrioritysitutation(self,priority):
		self.priority = priority
		if self.priority == True:
			return True
		else:
			return False

	def goToPriorityPosition(self):
		#increase Z
		#go to parking
		pass

	def emitGoneToPriorityPosition(self,goneToPriority):
		# emit gone to priority position event

		pass
	def run(self):
		# check priority situation
		while self.orderGcodeLine < self.gcodeDataLen:
			#start lock
			lockOne.acquire()
			if self.isPrioritysitutation(priorityEvent.is_set()):
				#if priority situation is true
				#Run in priority process
				print("Run in priority process")
				self.parking()
				#emit gone to priority envent
				reachPriorityPosition.set()
				lockOne.release()
				comeBackEvent.wait()
				#lockOne.acquire()
				#Comeback
				print("1 ---machine 1 comeback")
				self.sendGcode("G0 X{} Y{}".format(self.currentPosition[0],self.currentPosition[1]))
				self.sendGcode("M400")
				#clear comeback event
				comeBackEvent.clear()
				#lockOne.release()

			else:
				#if NOT priority situation
				#Run in normal process
				print("1 ---Not priority process")
				#read n-th Gcode Line in file
				self.getGcodeLine()
				#get position from gcode recive
				self.getPositionFromGcodeRecive()
				#caculate distance to current other machine position
				print("1 ---position from Gcode",self.PositionFromGcodeRecive)
				print("1 ---Two position",self.firstFriendPrinter.getCurrentPosition())
				D1 = self.caculateDistanceToPoint(self.firstFriendPrinter.getCurrentPosition())
				print("1 ---distance: ",D1)
				#check collision
				if self.checkCollision(D1):
					
					# release lock
					lockOne.release()
					# send Gcode Pause
					print("1 ---DWell pause")
					self.sendGcode("G4")
					
					
				else:
					#update current position machine one
					self.updateCurrentPosition(self.getPositionFromGcodeRecive())
					#release lock
					lockOne.release()
					#run normal process
					print("1 ---Running in normal process")

					
					#send Gocde to machine
					self.sendGcode(self.gCodeRecive)
					self.sendGcode("M400")
					#increase Gcode line number
					self.increaseOrderGcodeLine()

#########################################################


class typeTwoPrinter(virtualPrinter):
	################### typeOnePrinter Variable ######################
	currentPosition = [0,0]
	dirGcodeFile = ""
	gcodeData = []
	gcodeDataLen = 0
	orderGcodeLine = 0
	gCodeRecive = ""
	gCodeSend = ""
	PositionFromGcodeRecive = currentPosition
	numberOfLayer = 1
	zPosition = 0
	connection = None
	port = "COM8"
	baudrate = 115200
	##################################################################

	def __init__(self,name,gcodeFileDir,serialPort,baudrate):
		virtualPrinter.__init__(self,name,gcodeFileDir,serialPort,baudrate)
		pass
	
	def getFirstFriendPrinter(self,printer):
			self.firstFriendPrinter = printer
		
	def run(self):
		#read n-th Gcode Line in file
			while self.orderGcodeLine < self.gcodeDataLen:
				#start lock
				print("a1")
				lockOne.acquire()
				self.getGcodeLine()
				#get position from gcode recive
				self.getPositionFromGcodeRecive()
				print("a2")
				#z synchronous
				if ((self.numberOfLayer - self.firstFriendPrinter.numberOfLayer) > 1):
					print('a3')
					while(self.numberOfLayer - self.firstFriendPrinter.numberOfLayer) > 1:
						# goto X0Y0
						self.sendGcode("G0 X0 Y0")
						saveposition = self.currentPosition
						self.updateCurrentPosition([0,0])
						self.sendGcode("M400")
						lockOne.release()
						print("a1")
					#comeback
					print("2 ---machine 2 comeback")
					self.sendGcode("G0 X{} Y{}".format(saveposition[0],saveposition[1]))
					self.sendGcode("M400")
					self.updateCurrentPosition(saveposition)
					lockOne.acquire()
				#caculate distance to current other machine position
				print("2 ---position from Gcode",self.PositionFromGcodeRecive)
				print("2 ---One position",self.firstFriendPrinter.getCurrentPosition())
				D = self.caculateDistanceToPoint(self.firstFriendPrinter.getCurrentPosition())
				print("2 ---distance: ",D)
				#check collision
				if self.checkCollision(D):
					while self.checkCollision(D) and (self.orderGcodeLine < self.gcodeDataLen):
						# Emit priority event
						print("2 ---Emit priority event")
						priorityEvent.set()
						lockOne.release()
						# check whether machine one gone to priority position
						reachPriorityPosition.wait()
						
						self.updateCurrentPosition(self.PositionFromGcodeRecive)
						print("2 ---Two gcode Sended",self.PositionFromGcodeRecive)
						#send gcode
						self.sendGcode(self.gCodeRecive)
						self.sendGcode("M400")
						#increase order gcode line
						self.increaseOrderGcodeLine()
						
						#start lock
						lockOne.acquire()
						self.getGcodeLine()
						#get position from gcode recive
						self.getPositionFromGcodeRecive()
						#z synchronous
						if ((self.numberOfLayer - self.firstFriendPrinter.numberOfLayer) > 1):
							print("a")
							while((self.numberOfLayer - self.firstFriendPrinter.numberOfLayer) > 1):
								# goto X0Y0
								self.sendGcode("G0 X0 Y0")
								saveposition = self.currentPosition
								self.updateCurrentPosition([0,0])
								self.sendGcode("M400")
								lockOne.release()
								print("a1")
							#comeback
							print("2 ---machine 2 comeback")
							self.sendGcode("G0 X{} Y{}".format(saveposition[0],saveposition[1]))
							self.sendGcode("M400")
							self.updateCurrentPosition(saveposition)
							lockOne.acquire()
						#caculate distance to current other machine position
						print("2 ---position from Gcode",self.PositionFromGcodeRecive)
						print("2 ---One position",self.firstFriendPrinter.getCurrentPosition())
						D = self.caculateDistanceToPoint(self.firstFriendPrinter.getCurrentPosition())
						print("2 ---distance: ",D)
					# update curent position machine 2
					self.updateCurrentPosition(self.PositionFromGcodeRecive)
					priorityEvent.clear()
					#realease lock
					lockOne.release()
					#send Gcode
					print("2 ---Machine 2 is running to ",self.currentPosition)
					self.sendGcode(self.gCodeRecive)
					self.sendGcode("M400")
					#increase Gcode number line
					self.increaseOrderGcodeLine()
					#emit comeback event
					comeBackEvent.set()
					

				else:
					#update current position machine one
					self.updateCurrentPosition(self.getPositionFromGcodeRecive())
					#release lock
					lockOne.release()
					#run normal process
					print("2 ---Running in normal process")
					#send Gocde to machine
					self.sendGcode(self.gCodeRecive)
					self.sendGcode("M400")
					#increase Gcode line number
					self.increaseOrderGcodeLine()
