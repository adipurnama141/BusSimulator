import random
import sys
from Queue import *


# List Containing All Arrived Passangers
arrivedPenumpang = []

areaUnderQt_queue = dict()
areaUnderQt_queue[1] = 0
areaUnderQt_queue[2] = 0
areaUnderQt_queue[3] = 0

# Convert Seconds to Hour:Minute:Second Format
def timeFormatter(inputSecond):
	m, s = divmod(inputSecond, 60)
	h, m = divmod(m, 60)
	print "%d:%02d:%02d" % (h, m, s)

# Return Uniform Random Variable (15-25)
def loadPassanger():
	rand_var = random.uniform(0,1)
	processed_var = (rand_var * 10) + 15
	return processed_var

# Return Uniform Random Variable (16 - 24)
def unloadPassanger():
	rand_var = random.uniform(0,1)
	processed_var = (rand_var * 8) + 16
	return processed_var

# Generate Stream of Passanger Using Expovariate 
# Return List of Passangers
def generatePassanger(passangerPerHour,originStation):
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
			stationList.append(a)
	return stationList




# Data Model of A Passanger
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
		print "Delay Time In Queue : " + str(self.delayTimeInQueue)
	def leavingTheBus(self, timeLeavingTheBus):
		self.timeLeavingTheBus = timeLeavingTheBus


def nPersonInQueueStatistics_partArrivedPenumpang():
	for x in range(len(arrivedPenumpang)):
		penumpang = arrivedPenumpang[x]
		areaUnderQt_queue[penumpang.originStation] += penumpang.timeEnteringTheBus - penumpang.arrivedTimeAtOriginStation


# Calculate "Time Spent In System" Statistics
# Input : List of Arrived Passanger 
def personInSystemStatistics():
	penumpangInSystemTime = []
	for x in range(len(arrivedPenumpang)):
		penumpangInSystemTime.append(arrivedPenumpang[x].timeLeavingTheBus - arrivedPenumpang[x].arrivedTimeAtOriginStation)
	l = penumpangInSystemTime
	print "Average In System Time : ",
	print reduce(lambda x, y: x + y, l) / len(l)
	print "Max In System Time  : ",
	print max(l)
	print "Min In System Time : ",
	print min(l)


# Calculate "Delay Time In Queue" Statistics
# Input : List of Arrived Passanger
def delayTimeInQueueStatistics():
	max_delayTime = [-1,-1,-1]
	sum_delayTime = [0,0,0]
	avg_delayTime = [0,0,0]
	n_passangerInStation  = [0,0,0]
	for x in range(len(arrivedPenumpang)):
		station_type = arrivedPenumpang[x].originStation - 1
		n_passangerInStation[station_type] += 1
		sum_delayTime[station_type] += arrivedPenumpang[x].delayTimeInQueue
		if (arrivedPenumpang[x].delayTimeInQueue > max_delayTime[station_type]):
			max_delayTime[station_type] = arrivedPenumpang[x].delayTimeInQueue
	for x in range(0,3):		
		avg_delayTime[x] = sum_delayTime[x] / n_passangerInStation[x]
		print "Max Delay Time In Queue " + str(x+1) + " : " + str(max_delayTime[x])
		print "Avg Delay Time In Queue " + str(x+1) + " : "+ str(avg_delayTime[x])
	for x in range(0,3):		
		print "Max Delay Time In Queue " + str(x+1) + " : ",
		timeFormatter(max_delayTime[x])
		print "Avg Delay Time In Queue " + str(x+1) + " : ",
		timeFormatter(avg_delayTime[x])

class StationQueue:
	def __init__(self,passangerPerHour,originStation):
		self.allQueue = []
		self.currentQueue = []
		self.qtArea = 0
		self.localClock = 0
		self.firstStart = True
		self.topRecord = 0
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

	def getNumberPersonQueueStatistics(self):
		print "Average Number Queue (Station1) :",
		print self.StationQueue[1].qtArea / self.currentTime
		print "Average Number Queue (Station2) :",
		print self.StationQueue[2].qtArea / self.currentTime
		print "Average Number Queue (Station3) :",
		print self.StationQueue[3].qtArea / self.currentTime


		print "Max Number Queue (Station1) :",
		print self.StationQueue[1].topRecord 
		print "Max Number Queue (Station2) :",
		print self.StationQueue[2].topRecord 
		print "Max Number Queue (Station3) :",
		print self.StationQueue[3].topRecord 

	def addNgetemTimeStatistics(self,ngetemTime):
		self.ngetemTimeStatistics.append(ngetemTime)
	def addLoopTimeStatistics(self,loopTime):
		self.loopTimeStatistics.append(loopTime)
	def getNgetemTimeStatistics(self):
		l = self.ngetemTimeStatistics
		print "Average Ngetem Time : ",
		print reduce(lambda x, y: x + y, l) / len(l)
		print "Max Ngetem Time  : ",
		print max(l)
		print "Min Ngetem Time : ",
		print min(l)
	def getLoopTimeStatistics(self):
		l = self.loopTimeStatistics
		print "Average Loop Time : ",
		print reduce(lambda x, y: x + y, l) / len(l)
		print "Max Loop Time  : ",
		print max(l)
		print "Min Loop Time : ",
		print min(l)
	def refreshQueue(self):
		self.StationQueue[1].progressTime(self.currentTime)
		self.StationQueue[2].progressTime(self.currentTime)
		self.StationQueue[3].progressTime(self.currentTime)
	def timeoutCheck(self):
		self.refreshQueue()
		#print "Q1 : " + str(len(self.StationQueue[1].currentQueue))
		#print "Q2 : " + str(len(self.StationQueue[2].currentQueue))
		#print "Q3 : " + str(len(self.StationQueue[3].currentQueue))

		if self.currentTime >= (80 *3600):
			timeFormatter(self.currentTime)
			print "Time Is Over - Simulation Halted!"

			#Calculate Area Under Qt Based On Remaining Passanger in The Bus
			for x in range(len(self.passangers)):
				self.areaUnderQt = self.areaUnderQt + (self.currentTime - self.passangers[x].timeEnteringTheBus)
			#Calculate Avg Number of People on The Bus
			avgNumberOfPeopleOnTheBus = self.areaUnderQt / self.currentTime

			print "Total Passanger Served : " + str(len(arrivedPenumpang))
			delayTimeInQueueStatistics()
			self.getNgetemTimeStatistics()
			self.getLoopTimeStatistics()
			personInSystemStatistics()
			print "Average Number of People On The Bus",
			print avgNumberOfPeopleOnTheBus
			print "Max Number of People On The Bus",
			print self.maxNPassangers
			self.getNumberPersonQueueStatistics()
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
	def getMaxNgetemTime(self):
		return self.currentTime + (5 * 60)
	def loadPassanger(self,passanger):
		loadTime = loadPassanger()
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
				unloadTime = unloadPassanger()
				penumpangTurun = self.passangers.pop(0)
				penumpangTurun.timeArrivedAtStation = self.currentTime
				self.currentTime += unloadTime
				penumpangTurun.timeLeavingTheBus = self.currentTime
				penumpangTurun.targetStation = self.currentPosition
				arrivedPenumpang.append(penumpangTurun)	
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
				if (angkot.currentTime > currentSessionNgetemTime):
					currentSessionNgetemTime = angkot.currentTime
			if (currentStationQueue.peekFuturePassanger().arrivedTimeAtOriginStation <= currentSessionNgetemTime):
				self.setCurrentTime(currentStationQueue.peekFuturePassanger().arrivedTimeAtOriginStation)
			else:
				isWaitingPhase = False
				# Force Wait Until 5 Minutes (Even Is Predicted There Is No Passanger Will Come Anyway)
				if (self.currentTime < currentSessionNgetemTime):
					self.setCurrentTime(currentSessionNgetemTime)

				# Collect The Statistics Data (Waiting Time Duration)	
				ngetemTime = self.currentTime - self.timeArrivedAtStation
				angkot.addNgetemTimeStatistics(ngetemTime)

				#Collect The Statistics Data (Loop Time)
				if ((self.currentPosition == 3) and (self.isFreshStart)):
					self.carRentalDepartureTime = angkot.currentTime
				if ((self.currentPosition == 3) and (not angkot.isFreshStart)):
					loopTime = self.currentTime - self.carRentalDepartureTime
					carRentalDepartureTime = angkot.currentTime
					angkot.addLoopTimeStatistics(loopTime)		





# Station 3 : Car Rental
# Station 1 : Air Terminal 1
# Station 2 : Air Terminal 2


station = dict()
station[1] = generatePassanger(14,1)
station[2] = generatePassanger(10,2)
station[3] = generatePassanger(24,3)
carRentalDepartureTime = 0

angkot = Bus()

while angkot.currentTime < 80 * 3600:

	# Bus Arrived At Station
	stasiun = angkot.currentPosition
	timeArrivedAtStation = angkot.currentTime

	currentSessionNgetemTime = angkot.getMaxNgetemTime()
	print "Angkot Sampai Di Terminal "+ str(angkot.currentPosition) + " pada " + str(angkot.currentTime)
	
	angkot.unloadPassanger()
	angkot.loadPassangers()


	'''
	isWaitingPhase = True
	while (angkot.currentTime <= currentSessionNgetemTime) and (not angkot.isFull()) and (isWaitingPhase):
		intipPenumpang = station[stasiun][0]
		if (intipPenumpang.arrivedTimeAtOriginStation <= currentSessionNgetemTime):
			penumpangSedangNaikAngkot = station[stasiun].pop(0)
			waktuPenumpangDatangKeStasiun = penumpangSedangNaikAngkot.arrivedTimeAtOriginStation
			if (waktuPenumpangDatangKeStasiun > angkot.currentTime):
				print "Abang Angkot Menunggu Selama " + str(waktuPenumpangDatangKeStasiun - angkot.currentTime)
				angkot.setCurrentTime(waktuPenumpangDatangKeStasiun)
			else:
				print "Penumpang #" + str(penumpangSedangNaikAngkot.id) + " Sudah Menunggu Dari Tadi"
			print "Penumpang #" + str(penumpangSedangNaikAngkot.id) + " Sampai Di Stasiun 3 Pada " + str(penumpangSedangNaikAngkot.arrivedTimeAtOriginStation)	
			loadTime = loadPassanger()
			waktuPenumpangMasukAngkot = angkot.currentTime + loadTime
			penumpangSedangNaikAngkot.enteringTheBus(waktuPenumpangMasukAngkot)
			angkot.loadPassanger(penumpangSedangNaikAngkot)
			print "Penumpang #" + str(penumpangSedangNaikAngkot.id) + " Berusaha Memasuki Angkot Selama " + str(loadTime)
			print "Penumpang #" + str(penumpangSedangNaikAngkot.id) + " Masuk Angkot Pada " + str(waktuPenumpangMasukAngkot)
			print "Waktu Saat Ini "+ str(angkot.currentTime)
			#perpanjangan waktu ngetem akibat saat 5 menit, masih proses unloading
			if (angkot.currentTime > currentSessionNgetemTime):
				currentSessionNgetemTime = angkot.currentTime
		else:
			print "Diramalkan bahwa penumpang selanjutnya akan datang pada " + str(intipPenumpang.arrivedTimeAtOriginStation)
			print "Waktu Ngetem Maksimal Sesi Ini " + str(currentSessionNgetemTime)
			if (angkot.currentTime < currentSessionNgetemTime):
				angkot.setCurrentTime(currentSessionNgetemTime)
				print "Abang Angkot Menunggu Hingga 5 Menit Minimum Ngetem Selesai~"
			print "Waktu Saat Ini "+ str(angkot.currentTime)
			ngetemTime = angkot.currentTime - timeArrivedAtStation
			angkot.addNgetemTimeStatistics(ngetemTime)
			print "Abang Angkot Memutuskan Untuk Tancap Gas :v"
			
			#Whenever The Bus Depart from Terminal 3, Its Called A Loop
			#Collect The Statistics Data
			if ((stasiun == 3) and (angkot.isFreshStart)):
				carRentalDepartureTime = angkot.currentTime
			if ((stasiun == 3) and (not angkot.isFreshStart)):
				loopTime = angkot.currentTime - carRentalDepartureTime
				carRentalDepartureTime = angkot.currentTime
				angkot.addLoopTimeStatistics(loopTime)		
			isWaitingPhase = False
	'''

	# Bus Moving To The Next Station		
	angkot.movePlace()
	print "Angkot saat ini berisi " + str(angkot.getNPassanger()) + " penumpang"
	print "Ke Terminal 1 : " + str(angkot.nOfTerminal1Target)
	print "Ke Terminal 2 : " + str(angkot.nOfTerminal2Target)
	print "Ke Car Rental : " + str(angkot.nOfTermixesePeople)
	print "Mau Turun  : " + str(angkot.nPenumpangMauTurun)
	print ""
