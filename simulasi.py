import random
import sys
from Queue import *


# Convert Seconds to Hour:Minute:Second Format
def timeFormatter(inputSecond):
	m, s = divmod(inputSecond, 60)
	h, m = divmod(m, 60)
	print "%d:%02d:%02d" % (h, m, s)

# Calculate Average of List
def avg(l):
	return reduce(lambda x, y: x + y, l) / len(l)


class Passanger:
	def __init__(self,id,originStation,arrivedTimeAtOriginStation):
		self.id = id
		self.originStation = originStation
		self.targetStation = 0
		self.arrivedTimeAtOriginStation = arrivedTimeAtOriginStation
		self.arrivedTimeAtTargetStation = 0
		self.timeEnteringTheBus = 0
		self.timeLeavingTheBus = 0
		self.delayTimeInQueue = 0
	def enteringTheBus(self, timeEnteringTheBus):
		self.timeEnteringTheBus = timeEnteringTheBus
		self.delayTimeInQueue = self.timeEnteringTheBus - self.arrivedTimeAtOriginStation
	def leavingTheBus(self, timeLeavingTheBus):
		self.timeLeavingTheBus = timeLeavingTheBus


class StationQueue:
	def __init__(self,passangerPerHour,originStation):
		self.allQueue = []
		self.currentQueue = []
		self.qtArea = 0
		self.localClock = 0
		self.firstStart = True
		self.topRecord = 0
		self.initializeAllFutureEvents(passangerPerHour,originStation)

	# Initialize All Future Passanger Using Expovariate Distribution
	# All Future Passanger Stored in allQueue
	def initializeAllFutureEvents(self,passangerPerHour,originStation):
		global_time = 0.0
		simulation_end = 81
		simulation_end = simulation_end * 3600
		n_passanger = 0
		stationList = []
		while global_time < simulation_end:
			passanger_arrival = random.expovariate(passangerPerHour) * 3600
			global_time += passanger_arrival
			if (global_time <= simulation_end):
				n_passanger += 1
				m, s = divmod(global_time, 60)
				h, m = divmod(m, 60)
				a = Passanger(n_passanger,originStation,global_time)
				self.allQueue.append(a)

	def progressTime(self,time):
		if (self.firstStart):
			self.localClock = 0
			self.firstStart = False
		else:
			while (self.allQueue[0].arrivedTimeAtOriginStation <= time):
				passanger = self.allQueue.pop(0)
				self.currentQueue.append(passanger)
			self.qtArea += len(self.currentQueue) * (time - self.localClock)
			self.localClock = time
			if (self.topRecord < len(self.currentQueue)):
				self.topRecord = len(self.currentQueue)
	def peekFuturePassanger(self):
		return self.allQueue[0]


class Bus:
	def __init__(self):
		self.timeArrivedAtStation = 0
		self.carRentalDepartureTime = 0
		self.currentTime = 0.0
		self.passangers = []
		self.currentPosition = 3
		self.busSpeed = 30 #Miles Per Hour
		self.nOfTermixesePeople = 0
		self.nOfCarexesePeople = 0
		self.nOfTerminal1Target = 0
		self.nOfTerminal2Target = 0
		self.nPenumpangMauTurun = 0
		self.ngetemTimeStatistics = []
		self.loopTimeStatistics = []
		self.isFreshStart = True
		self.areaUnderQt = 0
		self.maxNPassangers = 0
		self.StationQueue = dict()
		self.StationQueue[1] = StationQueue(14,1)
		self.StationQueue[2] = StationQueue(10,2)
		self.StationQueue[3] = StationQueue(24,3)
		self.arrivedPenumpang =[]


	# Return Uniform Random Variable (15-25)
	def loadPassangerDuration(self):
		rand_var = random.uniform(0,1)
		processed_var = (rand_var * 10) + 15
		return processed_var

	# Return Uniform Random Variable (16 - 24)
	def unloadPassangerDuration(self):
		rand_var = random.uniform(0,1)
		processed_var = (rand_var * 8) + 16
		return processed_var


	def getNumberPersonQueueStatistics(self):
		print "Average Number Queue"
		print "	Station1 :",
		print self.StationQueue[1].qtArea / self.currentTime
		print "	Station2 :",
		print self.StationQueue[2].qtArea / self.currentTime
		print "	Station3 :",
		print self.StationQueue[3].qtArea / self.currentTime
		print "Max Number Queue"
		print "	Station1 :",
		print self.StationQueue[1].topRecord 
		print "	Station2 :",
		print self.StationQueue[2].topRecord 
		print "	Station3 :",
		print self.StationQueue[3].topRecord 

	def addNgetemTimeStatistics(self,ngetemTime):
		self.ngetemTimeStatistics.append(ngetemTime)
	def addLoopTimeStatistics(self,loopTime):
		self.loopTimeStatistics.append(loopTime)
	def getNgetemTimeStatistics(self):
		l = self.ngetemTimeStatistics
		avgBusWaitTime = avg(l)
		maxBusWaitTime = max(l)
		minBusWaitTime = min(l)
		print "Bus Waiting Time"
		print "	Max : ",
		timeFormatter(maxBusWaitTime)
		print "	Avg : ",
		timeFormatter(avgBusWaitTime)		
		print "	Min : ",
		timeFormatter(minBusWaitTime)
	def getLoopTimeStatistics(self):
		l = self.loopTimeStatistics
		avgLoopTime = avg(l)
		maxLoopTime = max(l)
		minLoopTime = min(l)
		print "Loop Time"
		print "	Max: ",
		timeFormatter(maxLoopTime)
		print "	Avg: ",
		timeFormatter(avgLoopTime)			
		print "	Min: ",
		timeFormatter(minLoopTime)
	def refreshQueue(self):
		self.StationQueue[1].progressTime(self.currentTime)
		self.StationQueue[2].progressTime(self.currentTime)
		self.StationQueue[3].progressTime(self.currentTime)
	
	def getNumberPeopleOnBusStatistics(self):
		#Calculate Area Under Qt Based On Remaining Passanger in The Bus
		for x in range(len(self.passangers)):
			self.areaUnderQt = self.areaUnderQt + (self.currentTime - self.passangers[x].timeEnteringTheBus)
		#Calculate Avg Number of People on The Bus
		avgNumberOfPeopleOnTheBus = self.areaUnderQt / self.currentTime
		print "Number of People On The Bus"
		print "	Max : ",
		print self.maxNPassangers
		print "	Avg : ",
		print avgNumberOfPeopleOnTheBus	



	# Calculate "Time Spent In System" Statistics by Using List of Arrived Passanger
	def personInSystemStatistics(self):
		penumpangInSystemTime = []
		for x in range(len(self.arrivedPenumpang)):
			penumpangInSystemTime.append(self.arrivedPenumpang[x].timeLeavingTheBus - self.arrivedPenumpang[x].arrivedTimeAtOriginStation)
		l = penumpangInSystemTime
		avgInSystemTime = avg(l)
		maxInSystemTime = max(l)
		minInSystemTime = min(l)
		print "Passanger In System Duration"
		print "	Max : ",
		timeFormatter(maxInSystemTime)
		print "	Avg : ",
		timeFormatter(avgInSystemTime)
		print "	Min : ",
		timeFormatter(minInSystemTime)


	# Calculate "Delay Time In Queue" Statistics by Using List of Arrived Passanger
	def delayTimeInQueueStatistics(self):
		max_delayTime = [-1,-1,-1]
		sum_delayTime = [0,0,0]
		avg_delayTime = [0,0,0]
		n_passangerInStation  = [0,0,0]
		for x in range(len(self.arrivedPenumpang)):
			station_type = self.arrivedPenumpang[x].originStation - 1
			n_passangerInStation[station_type] += 1
			sum_delayTime[station_type] += self.arrivedPenumpang[x].delayTimeInQueue
			if (self.arrivedPenumpang[x].delayTimeInQueue > max_delayTime[station_type]):
				max_delayTime[station_type] = self.arrivedPenumpang[x].delayTimeInQueue
		print "Max Delay Time"
		for x in range(0,3):
			avg_delayTime[x] = sum_delayTime[x] / n_passangerInStation[x]		
			print "	Queue " + str(x+1) + " : ",
			timeFormatter(max_delayTime[x])
		print "Avg Delay Time"
		for x in range(0,3):	
			print "	Queue " + str(x+1) + " : ",
			timeFormatter(avg_delayTime[x])



	def printStatistics(self):
		print "Total Passanger Served : " + str(len(self.arrivedPenumpang))
		self.getNgetemTimeStatistics()
		self.getLoopTimeStatistics()
		self.getNumberPeopleOnBusStatistics()					
		self.getNumberPersonQueueStatistics()
		self.delayTimeInQueueStatistics()
		self.personInSystemStatistics()


	def timeoutCheck(self):
		self.refreshQueue()
		if self.currentTime >= (80 *3600):
			timeFormatter(self.currentTime)
			print "Time Is Over - Simulation Halted!"
			self.printStatistics()
			sys.exit()

	def whichTerminalSir(self):
		for x in range(self.nOfCarexesePeople):
			if (random.uniform(0,1) <= 0.583):
				self.nOfTerminal1Target += 1
			else:
				self.nOfTerminal2Target += 1
	def movePlace(self):
		self.isFreshStart = False	
		#Check if Current Number of People in The Bus Breaks Record :D
		if (self.maxNPassangers < len(self.passangers)):
			self.maxNPassangers = len(self.passangers)
		if (self.currentPosition == 3):
			self.currentPosition = 1
			self.currentTime = self.currentTime + (4.5 / self.busSpeed * 3600)
			self.whichTerminalSir()
			self.nPenumpangMauTurun = self.nOfTerminal1Target
			self.nOfTermixesePeople = 0
		elif (self.currentPosition == 1):
			self.currentPosition = 2
			self.currentTime = self.currentTime + (1 / self.busSpeed * 3600)
			self.nPenumpangMauTurun = self.nOfTerminal2Target
			self.nOfTerminal1Target = 0
		else:
			self.currentPosition = 3
			self.currentTime = self.currentTime + (4.5 / self.busSpeed * 3600)
			self.nPenumpangMauTurun = self.nOfTermixesePeople
			self.nOfTerminal2Target = 0
		self.timeArrivedAtStation = self.currentTime
		self.timeoutCheck()
		print "Angkot Sampai Di Terminal "+ str(self.currentPosition) + " pada ",
		timeFormatter(self.currentTime)

	def getMaxNgetemTime(self):
		return self.currentTime + (5 * 60)
	def loadPassanger(self,passanger):
		loadTime = self.loadPassangerDuration()
		passanger.enteringTheBus(self.currentTime + loadTime)
		self.passangers.append(passanger)
		self.currentTime = passanger.timeEnteringTheBus
		if (passanger.originStation == 3):
			self.nOfCarexesePeople += 1
		else:
			self.nOfTermixesePeople +=1
		self.timeoutCheck()
	def setCurrentTime(self,newtime):
		self.currentTime = newtime
		self.timeoutCheck()
	def isFull(self):
		return len(self.passangers) >= 20
	def getNPassanger(self):
		return len(self.passangers)
	def unloadPassanger(self):
		if (self.nPenumpangMauTurun == 0):
			print "Tidak Ada Penumpang Mau Turun Di Terminal Ini..."
		else:
			print "Ada " + str(self.nPenumpangMauTurun) + " Penumpang Mau Turun Disini"
			for x in range(self.nPenumpangMauTurun):
				unloadTime = self.unloadPassangerDuration()
				penumpangTurun = self.passangers.pop(0)
				penumpangTurun.timeArrivedAtStation = self.currentTime
				self.currentTime += unloadTime
				penumpangTurun.timeLeavingTheBus = self.currentTime
				penumpangTurun.targetStation = self.currentPosition
				self.arrivedPenumpang.append(penumpangTurun)	
				if (penumpangTurun.originStation == 3):
					self.nOfCarexesePeople -= 1
				else:
					self.nOfTermixesePeople -= 1
				self.areaUnderQt = self.areaUnderQt + (self.currentTime - penumpangTurun.timeEnteringTheBus)
				self.timeoutCheck()
	def loadPassangers(self):
		currentSessionNgetemTime = self.getMaxNgetemTime()
		currentStationQueue = self.StationQueue[self.currentPosition]
		isWaitingPhase = True
		while (self.currentTime <= currentSessionNgetemTime) and (not self.isFull()) and (isWaitingPhase):
			while (len(currentStationQueue.currentQueue) > 0) and (not self.isFull()):
				passanger = currentStationQueue.currentQueue.pop(0)
				self.loadPassanger(passanger)
				# Additional Waiting Time Due People Loading
				if (self.currentTime > currentSessionNgetemTime):
					currentSessionNgetemTime = self.currentTime
			if (currentStationQueue.peekFuturePassanger().arrivedTimeAtOriginStation <= currentSessionNgetemTime):
				self.setCurrentTime(currentStationQueue.peekFuturePassanger().arrivedTimeAtOriginStation)
			else:
				isWaitingPhase = False
				# Force Wait Until 5 Minutes (Even Is Predicted There Is No Passanger Will Come Anyway)
				if (self.currentTime < currentSessionNgetemTime):
					self.setCurrentTime(currentSessionNgetemTime)

				# Collect The Statistics Data (Waiting Time Duration)	
				ngetemTime = self.currentTime - self.timeArrivedAtStation
				self.addNgetemTimeStatistics(ngetemTime)

				#Collect The Statistics Data (Loop Time)
				if ((self.currentPosition == 3) and (self.isFreshStart)):
					self.carRentalDepartureTime = self.currentTime
				if ((self.currentPosition == 3) and (not self.isFreshStart)):
					loopTime = self.currentTime - self.carRentalDepartureTime
					self.carRentalDepartureTime = self.currentTime
					#print "Loop Time : ",
					timeFormatter(loopTime)
					self.addLoopTimeStatistics(loopTime)		




bus = Bus()
while True:
	bus.unloadPassanger()
	bus.loadPassangers()
	bus.movePlace()




