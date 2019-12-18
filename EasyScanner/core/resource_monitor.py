import requests
import re
from queue import Queue
import threading
import random
import time
from proxy_scanner import ProxyScanner
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import psutil
import os



class WorkerSignals(QObject):
    
    status 	 = pyqtSignal(float,float)


class ResourceMonitor(QRunnable):
	def __init__(self,pid):
		super(ResourceMonitor,self).__init__()
		self.signals = WorkerSignals()
		self.pid = pid

	@pyqtSlot()
	def run(self):
		self.watch_resources()

	def watch_resources(self):
		process = psutil.Process(self.pid)
		while True:
			#print("status: "+str(process.status()))
			#print("cpu percent: "+str(process.cpu_percent(interval=2.0)))
			cpu_usage = process.cpu_percent(interval=0.3)
			mem_usage = process.memory_percent(memtype="rss")
			mem_usage = "%.1f" % mem_usage
			self.signals.status.emit(cpu_usage,float(mem_usage))
			#print(self.pid)
			#print(len(process.connections()))
			#print(process.cpu_num())
			#print("threads: " +str(process.num_threads()))

	# def get_pid(self):
	# 	for i in psutil.pids():
	# 		if self.progname in psutil.Process(i).cmdline():
	# 			return psutil.Process(i).pid