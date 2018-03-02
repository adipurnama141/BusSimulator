import random,sys

def timeFormatter(inputSecond):
	m, s = divmod(inputSecond, 60)
	h, m = divmod(m, 60)
	print "%d:%02d:%02d" % (h, m, s)

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
		self.futurePassangerQueue = []
		self.currentQueue = []
		self.simulationTime = 0
		self.isFirstStart = True
		self.maxNumberQueue = 0
		self.qtArea_nPeopleOnQueue = 0
		self.initializeAllFutureEvents(passangerPerHour,originStation)
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
				a = Passanger(n_passanger,originStation,global_time)
				self.futurePassangerQueue.append(a)
	def updateStationQueue(self,time):
		if (self.isFirstStart):
			self.simulationTime = 0
			self.isFirstStart = False
		else:
			while (self.futurePassangerQueue[0].arrivedTimeAtOriginStation <= time):
				passanger = self.futurePassangerQueue.pop(0)
				self.currentQueue.append(passanger)
			self.qtArea_nPeopleOnQueue += len(self.currentQueue) * (time - self.simulationTime)
			self.simulationTime = time
			if (self.maxNumberQueue < len(self.currentQueue)):
				self.maxNumberQueue = len(self.currentQueue)
	def peekFuturePassanger(self):
		return self.futurePassangerQueue[0]


class Bus:
	def __init__(self):
		# Time Related
		self.timeArrivedAtStation = 0
		self.carRentalDepartureTime = 0
		self.simulationTime = 0.0
		# Passangers
		self.passangersInsideBus = []
		self.arrivedPassangers =[]
		self.nOfPassangerFromTerminal = 0
		self.nOfPassangerFromCarRental = 0
		self.nOfPassangerToTerminal1 = 0
		self.nOfPassangerToTerminal2 = 0
		self.nOfPassangerWantToUnloadHere = 0
		# Station Related
		self.StationQueue = dict()
		self.StationQueue[1] = StationQueue(14,1)
		self.StationQueue[2] = StationQueue(10,2)
		self.StationQueue[3] = StationQueue(24,3)
		self.currentPosition = 3
		self.busSpeed = 30 #Miles Per Hour
		#Statistics
		self.busWaitingTimeStatistics = []
		self.loopTimeStatistics = []
		self.qtArea_nPassangerInsideBus = 0
		self.maxNPassangers = 0
		self.isFreshStart = True

	def unloadPassangers(self):
		if (self.nOfPassangerWantToUnloadHere > 0):
			for x in range(self.nOfPassangerWantToUnloadHere):
				passangerWantToUnload = self.passangersInsideBus.pop(0)
				self.unloadPassanger(passangerWantToUnload)

	def loadPassangers(self):
		currentSessionbusWaitingTime = self.getMaxbusWaitingTime()
		currentStationQueue = self.StationQueue[self.currentPosition]
		isWaitingPhase = True
		while (self.simulationTime <= currentSessionbusWaitingTime) and (not self.isFull()) and (isWaitingPhase):

			# Load All Passanger Who Already Waiting in Station Queue as Long Bus is Not Full
			while (len(currentStationQueue.currentQueue) > 0) and (not self.isFull()):
				passanger = currentStationQueue.currentQueue.pop(0)
				self.loadPassanger(passanger)
				# Additional Waiting Time Due People Loading
				if (self.simulationTime > currentSessionbusWaitingTime):
					currentSessionbusWaitingTime = self.simulationTime
			
			# Peek Future Passanger
			# If There is Future Passanger Who Will Come Faster Before WaitTime Ends. Wait...
			# If No. Wait Until WaitTime Ends. Then Go..
			if (currentStationQueue.peekFuturePassanger().arrivedTimeAtOriginStation <= currentSessionbusWaitingTime):
				self.setsimulationTime(currentStationQueue.peekFuturePassanger().arrivedTimeAtOriginStation)
			else:
				isWaitingPhase = False
				# Force Wait Until 5 Minutes (Even Is Predicted There Is No Passanger Will Come Anyway)
				if (self.simulationTime < currentSessionbusWaitingTime):
					self.setsimulationTime(currentSessionbusWaitingTime)
				# Collect The Statistics Data (Waiting Time Duration)	
				busWaitingTime = self.simulationTime - self.timeArrivedAtStation
				self.addbusWaitingTimeStatistics(busWaitingTime)
				# Collect The Statistics Data (Loop Time)
				if ((self.currentPosition == 3) and (self.isFreshStart)):
					self.carRentalDepartureTime = self.simulationTime
				if ((self.currentPosition == 3) and (not self.isFreshStart)):
					loopTime = self.simulationTime - self.carRentalDepartureTime
					self.carRentalDepartureTime = self.simulationTime
					self.addLoopTimeStatistics(loopTime)

	def movePlace(self):
		self.isFreshStart = False	
		# [STATS] Check if Current Number of People in The Bus Breaks Record
		if (self.maxNPassangers < len(self.passangersInsideBus)):
			self.maxNPassangers = len(self.passangersInsideBus)
		if (self.currentPosition == 3):
			self.currentPosition = 1
			self.simulationTime = self.simulationTime + (4.5 / self.busSpeed * 3600)
			timeSpentOnRoad = (4.5 / self.busSpeed * 3600)
			self.determinePassangerTargetStation()
			self.nOfPassangerWantToUnloadHere = self.nOfPassangerToTerminal1
			self.nOfPassangerFromTerminal = 0
		elif (self.currentPosition == 1):
			self.currentPosition = 2
			self.simulationTime = self.simulationTime + (1 / self.busSpeed * 3600)
			timeSpentOnRoad = (1 / self.busSpeed * 3600)
			self.nOfPassangerWantToUnloadHere = self.nOfPassangerToTerminal2
			self.nOfPassangerToTerminal1 = 0
		else:
			self.currentPosition = 3
			self.simulationTime = self.simulationTime + (4.5 / self.busSpeed * 3600)
			timeSpentOnRoad = (4.5 / self.busSpeed * 3600)
			self.nOfPassangerWantToUnloadHere = self.nOfPassangerFromTerminal
			self.nOfPassangerToTerminal2 = 0
		self.timeArrivedAtStation = self.simulationTime	
		self.qtArea_nPassangerInsideBus += len(self.passangersInsideBus) * timeSpentOnRoad
		self.timeoutCheck()

	def timeoutCheck(self):
		self.refreshQueue()
		if self.simulationTime >= (80 *3600):
			self.printStatistics()
			sys.exit()

	def refreshQueue(self):
		self.StationQueue[1].updateStationQueue(self.simulationTime)
		self.StationQueue[2].updateStationQueue(self.simulationTime)
		self.StationQueue[3].updateStationQueue(self.simulationTime)

	def printStatistics(self):
		print "Total Passanger Served : " + str(len(self.arrivedPassangers))
		self.printBusWaitingTimeStatistics()
		self.printLoopTimeStatistics()
		self.printNumberPeopleOnBusStatistics()					
		self.printNumberPersonQueueStatistics()
		self.printDelayTimeInQueueStatistics()
		self.printPersonInSystemStatistics()

	def unloadPassanger(self,passanger):
		unloadTime = self.unloadPassangerDuration()
		passanger.timeArrivedAtStation = self.simulationTime
		self.simulationTime += unloadTime
		passanger.timeLeavingTheBus = self.simulationTime
		passanger.targetStation = self.currentPosition
		self.arrivedPassangers.append(passanger)	
		if (passanger.originStation == 3):
			self.nOfPassangerFromCarRental -= 1
		else:
			self.nOfPassangerFromTerminal -= 1

		self.timeoutCheck()

	def loadPassanger(self,passanger):
		loadTime = self.loadPassangerDuration()
		passanger.enteringTheBus(self.simulationTime + loadTime)
		self.passangersInsideBus.append(passanger)
		self.simulationTime = passanger.timeEnteringTheBus
		if (passanger.originStation == 3):
			self.nOfPassangerFromCarRental += 1
		else:
			self.nOfPassangerFromTerminal +=1
		self.timeoutCheck()

	def loadPassangerDuration(self):
		rand_var = random.uniform(0,1)
		processed_var = (rand_var * 10) + 15
		return processed_var

	def unloadPassangerDuration(self):
		rand_var = random.uniform(0,1)
		processed_var = (rand_var * 8) + 16
		return processed_var

	def determinePassangerTargetStation(self):
		for x in range(self.nOfPassangerFromCarRental):
			if (random.uniform(0,1) <= 0.583):
				self.nOfPassangerToTerminal1 += 1
			else:
				self.nOfPassangerToTerminal2 += 1

	def printNumberPersonQueueStatistics(self):
		print "Average Number Queue"
		print "	Station1 :",
		print self.StationQueue[1].qtArea_nPeopleOnQueue / self.simulationTime
		print "	Station2 :",
		print self.StationQueue[2].qtArea_nPeopleOnQueue / self.simulationTime
		print "	Station3 :",
		print self.StationQueue[3].qtArea_nPeopleOnQueue / self.simulationTime
		print "Max Number Queue"
		print "	Station1 :",
		print self.StationQueue[1].maxNumberQueue 
		print "	Station2 :",
		print self.StationQueue[2].maxNumberQueue 
		print "	Station3 :",
		print self.StationQueue[3].maxNumberQueue 

	def printBusWaitingTimeStatistics(self):
		l = self.busWaitingTimeStatistics
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
	
	def printLoopTimeStatistics(self):
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
		
	def printNumberPeopleOnBusStatistics(self):
		#Calculate Area Under Qt Based On Remaining Passanger in The Bus
			#Calculate Avg Number of People on The Bus
		avgNumberOfPeopleOnTheBus = self.qtArea_nPassangerInsideBus / self.simulationTime
		print "Number of People On The Bus"
		print "	Max : ",
		print self.maxNPassangers
		print "	Avg : ",
		print avgNumberOfPeopleOnTheBus	

	# Calculate "Time Spent In System" Statistics by Using List of Arrived Passanger
	def printPersonInSystemStatistics(self):
		penumpangInSystemTime = []
		for x in range(len(self.arrivedPassangers)):
			penumpangInSystemTime.append(self.arrivedPassangers[x].timeLeavingTheBus - self.arrivedPassangers[x].arrivedTimeAtOriginStation)
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
	def printDelayTimeInQueueStatistics(self):
		max_delayTime = [-1,-1,-1]
		sum_delayTime = [0,0,0]
		avg_delayTime = [0,0,0]
		n_passangerInStation  = [0,0,0]
		for x in range(len(self.arrivedPassangers)):
			station_type = self.arrivedPassangers[x].originStation - 1
			n_passangerInStation[station_type] += 1
			sum_delayTime[station_type] += self.arrivedPassangers[x].delayTimeInQueue
			if (self.arrivedPassangers[x].delayTimeInQueue > max_delayTime[station_type]):
				max_delayTime[station_type] = self.arrivedPassangers[x].delayTimeInQueue
		print "Max Delay Time"
		for x in range(0,3):
			avg_delayTime[x] = sum_delayTime[x] / n_passangerInStation[x]		
			print "	Queue " + str(x+1) + " : ",
			timeFormatter(max_delayTime[x])
		print "Avg Delay Time"
		for x in range(0,3):	
			print "	Queue " + str(x+1) + " : ",
			timeFormatter(avg_delayTime[x])

	def addbusWaitingTimeStatistics(self,busWaitingTime):
		self.busWaitingTimeStatistics.append(busWaitingTime)

	def addLoopTimeStatistics(self,loopTime):
		self.loopTimeStatistics.append(loopTime)

	def getMaxbusWaitingTime(self):
		return self.simulationTime + (5 * 60)

	def setsimulationTime(self,newtime):
		self.simulationTime = newtime
		self.timeoutCheck()

	def isFull(self):
		return len(self.passangersInsideBus) >= 20

	def getNPassanger(self):
		return len(self.passangersInsideBus)
	
		
bus = Bus()
while True:
	bus.unloadPassangers()
	bus.loadPassangers()
	bus.movePlace()