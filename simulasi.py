import random
import sys
from Queue import *


arrivedPenumpang = []

def timeFormatter(inputSecond):
	m, s = divmod(inputSecond, 60)
	h, m = divmod(m, 60)
	print "%d:%02d:%02d" % (h, m, s)

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
	def arrivedAtTarget(self, timeArrivedAtTarget):
		self.arrivedTimeAtTargetStation = timeArrivedAtTarget
	def leavingTheBus(self, timeLeavingTheBus):
		self.timeLeavingTheBus = timeLeavingTheBus


def	

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

class Bus:
	def __init__(self):
		self.currentTime = 0.0
		self.passangers = []
		self.currentPosition = 3
		#Bus Speed in Miles Per Hour
		self.busSpeed = 30
		self.nOfTermixesePeople = 0
		self.nOfCarexesePeople = 0
		self.nOfTerminal1Target = 0
		self.nOfTerminal2Target = 0
		self.nPenumpangMauTurun = 0
	def timeoutCheck(self):
		if self.currentTime >= (80 *3600):
			timeFormatter(self.currentTime)
			print "Time Is Over - Simulation Halted!"
			print "Total Passanger Served : " + str(len(arrivedPenumpang))
			delayTimeInQueueStatistics()
			sys.exit()
	def whichTerminalSir(self):
		for x in range(self.nOfCarexesePeople):
			if (random.uniform(0,1) <= 0.583):
				self.nOfTerminal1Target += 1
			else:
				self.nOfTerminal2Target += 1
	def movePlace(self):
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
		self.timeoutCheck()
	def getMaxNgetemTime(self):
		return self.currentTime + (5 * 60)
	def loadPassanger(self,passanger):
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
	def unloadPassanger(self,unloadTime):
		self.currentTime += unloadTime
		penumpangTurun = self.passangers.pop(0)
		if (penumpangTurun.originStation == 3):
			self.nOfCarexesePeople -= 1
		else:
			self.nOfTermixesePeople -= 1
		self.timeoutCheck()
		return penumpangTurun



def generatePassanger(passangerPerHour,originStation):
	global_time = 0.0
	simulation_end = 81
	simulation_end = simulation_end * 3600
	n_passanger = 0
	#stationQueue = Queue(maxsize=0)
	stationList = []
	while global_time < simulation_end:
		passanger_arrival = random.expovariate(passangerPerHour) * 3600
		global_time += passanger_arrival
		if (global_time <= simulation_end):
			n_passanger += 1
			m, s = divmod(global_time, 60)
			h, m = divmod(m, 60)
			a = Passanger(n_passanger,originStation,global_time)
			#stationQueue.put(a)
			stationList.append(a)
			#print "Passanger #" + str(n_passanger) + " arrived at",
			#print "%d:%02d:%02d" % (h, m, s)
	return stationList

def loadPassanger():
	rand_var = random.uniform(0,1)
	processed_var = (rand_var * 10) + 15
	return processed_var

def unloadPassanger():
	rand_var = random.uniform(0,1)
	processed_var = (rand_var * 8) + 16
	return processed_var



station = dict()
station[1] = generatePassanger(14,1)
station[2] = generatePassanger(10,2)
station[3] = generatePassanger(24,3)



angkot = Bus()

while angkot.currentTime < 80 * 3600:
	stasiun = angkot.currentPosition
	#timeFormatter(angkot.currentTime)
	print "Angkot Sampai Di Terminal "+ str(stasiun) + " pada " + str(angkot.currentTime)
	
	currentSessionNgetemTime = angkot.getMaxNgetemTime()
	

	#unloading orang
	if (angkot.nPenumpangMauTurun == 0):
		print "Tidak Ada Penumpang Mau Turun Di Terminal Ini..."
	else:
		print "Ada " + str(angkot.nPenumpangMauTurun) + " Penumpang Mau Turun Disini"
	nPenumpangMauTurun = angkot.nPenumpangMauTurun
	waktuPenumpangSampaiKeTujuan = angkot.currentTime
	for x in range(nPenumpangMauTurun):
		unloadTime = unloadPassanger()
		penumpangTurun = angkot.unloadPassanger(unloadTime)
		penumpangTurun.arrivedAtTarget(waktuPenumpangSampaiKeTujuan)
		waktuPenumpangKeluarAngkot = angkot.currentTime + unloadTime
		print "Penumpang " +str(penumpangTurun.originStation) + "#"  + str(penumpangTurun.id) + " Berusaha Keluar Dari Angkot Selama " + str(unloadTime)
		penumpangTurun.leavingTheBus(waktuPenumpangKeluarAngkot)
		penumpangTurun.targetStation = stasiun
		arrivedPenumpang.append(penumpangTurun)
		print "Penumpang " +str(penumpangTurun.originStation) + "#"  + str(penumpangTurun.id) + " Berhasil Keluar Dari Angkot Pada " + str(angkot.currentTime)

		


		

	yukGasBang = False
	while (angkot.currentTime <= currentSessionNgetemTime) and (not angkot.isFull()) and (not yukGasBang):
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
			print "Abang Angkot Memutuskan Untuk Tancap Gas :v"
			yukGasBang = True
	angkot.movePlace()
	print "Angkot saat ini berisi " + str(angkot.getNPassanger()) + " penumpang"
	print "Ke Terminal 1 : " + str(angkot.nOfTerminal1Target)
	print "Ke Terminal 2 : " + str(angkot.nOfTerminal2Target)
	print "Ke Car Rental : " + str(angkot.nOfTermixesePeople)
	print "Mau Turun  : " + str(angkot.nPenumpangMauTurun)
	print ""



