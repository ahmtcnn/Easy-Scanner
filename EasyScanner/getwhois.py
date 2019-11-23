from whois import whois
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class WorkerSignals(QObject):
    
    list 	 = pyqtSignal(int,str)

class Whois(QRunnable):
	def __init__(self,url):
		super(Whois,self).__init__()
		self.url = url
		self.counter = 0
		self.signals = WorkerSignals()


	@pyqtSlot()
	def run(self):
		result = whois(self.url)
		for key in result:
			text = str(key) + " : " + str(result[key])
			self.signals.list.emit(self.counter,str(text))
			self.counter+=1
		#self.signals.list.emit(0,str(result))






#https://freedomainapi.com/members/register.php sql injection