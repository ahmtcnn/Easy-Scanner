import socket
import threading
import time
from queue import Queue
import socket
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class WorkerSignals(QObject):
    
    progress = pyqtSignal(float,str)
    list  	 = pyqtSignal(str,int)


"""By setting them as daemon threads, we can let them run and forget about them, and when our program quits, any daemon threads are killed automatically."""
class PortScanner(QRunnable):
	def __init__(self,target):
		super(PortScanner, self).__init__()
		#self.port_list = port_list
		self.target = target
		self.list_counter = 1
		self.signals = WorkerSignals()

	@pyqtSlot()
	def run(self):
		socket.setdefaulttimeout(0.25)
		self.print_lock = threading.Lock()

		self.bar_counter=1
		
		#self.port_list.insertItem(0,"Port\tService")

		self.q = Queue()
		self.startTime = time.time()
		self.start_threads()
		self.queue_ports()
		self.q.join()
		#print('Time taken:', time.time() - self.startTime)
	
	def start_threads(self):
		for _ in range(50):
			t = threading.Thread(target = self.threader)
			t.daemon = True
			t.start()
	
	def queue_ports(self):	
		for port in range(0, 65000):
			self.q.put(port)
	
	def threader(self):
		while True:
			port  = self.q.get()
			self.portscan(port)
			self.q.task_done() # bu q.join i tetiklemek için.


	def portscan(self,port):
		text = "[" + str(self.bar_counter) + " / " + str(2000) + "]"
		val = (100*self.bar_counter)/(2000)
		self.signals.progress.emit(val,text)
		self.bar_counter+=1
		s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
		try:
			con = s.connect((self.target, port))
			try:
				service = socket.getservbyport(port)
			except:
				service = "unknown"
			with self.print_lock:
				#self.port_list.insertItem(self.list_counter,str(port) + "\t" + str(service))
				self.list_counter+=1
				text = str(port) + "\t" + str(service)
				self.signals.list.emit(text,list_counter)
				print("geçti")
				con.close()
		except:
			
			pass

