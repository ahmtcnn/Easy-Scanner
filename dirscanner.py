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


#https://ysar.net/python/yield.html
#yield ile dosya okuma ve web istekleri kullanılacak
#https://julien.danjou.info/python-and-fast-http-clients/

class WorkerSignals(QObject):
    
    progress = pyqtSignal(float,str)
    list 	 = pyqtSignal(str,int)

class DirScanner(QRunnable):
	def __init__(self,target):
		super(DirScanner, self).__init__()

		self.startTime		= time.time()
		self.wordlist_size 	= 0
		self.list_counter 	= 0
		self.dir_counter 	= 0
		self.user_agents 	= []
		self.q 				= Queue()
		self.target 		= target
		self.print_lock 	= threading.Lock()
		self.signals 		= WorkerSignals()
		self.session 		= requests.Session()
		self.proxy_url 		= 'http://free-proxy-list.net/'
		self.headers 		= requests.utils.default_headers()
		#self.signals.list.emit("test",0)


	@pyqtSlot()
	def run(self):
		print("started")
		proxy_scanner 		= ProxyScanner()
		self.proxies 		= proxy_scanner.return_proxies()
		print("finished")
		start_time = time.time()
		self.read_user_agent_file()
		self.start_threads()
		self.queue_dirs()
		self.q.join()
		stop_time = time.time()


	def queue_dirs(self):
		self.wordlist_size = sum(1 for line in open('data/directories.dat'))
		with open("data/directories.dat","r") as fp:
			for line in fp:
				line = line.rstrip("\n")
				self.q.put(line)

	def test(self,word):
		

		url = self.target + "/" + word
		try:
			self.test_url(url)
		except:
			pass
		self.update_progresbar()

		

	def update_progresbar(self):
		self.dir_counter+=1
		text = "[" + str(self.dir_counter) + " / " + str(self.wordlist_size) + "]"
		progress_bar_value = (100*self.dir_counter)/(self.wordlist_size)
		self.signals.progress.emit(progress_bar_value,text)


	def test_url(self,url):
		proxy = self.get_working_proxy(None)
		agent = random.choice(self.user_agents)
		header = self.headers.update(agent)
		try:
			response = self.session.get(url,headers=agent,allow_redirects=True,timeout=5)
			if response.status_code == 200:
				with self.print_lock:
					print(url,response.status_code)
					self.list_counter+=1
					self.signals.list.emit(str(url)+str(response.status_code),self.list_counter)
		except:
			pass


	def threader(self):
		while True:
			word = self.q.get()
			self.test(word)
			self.q.task_done()

	def start_threads(self):
		for _ in range(1):
			t = threading.Thread(target = self.threader)
			t.daemon = True
			t.start()

	def read_user_agent_file(self):
		with open("data/user_agents.dat","r+") as fp:
			for agent in fp:
				agent=agent.rstrip("\n")
				self.user_agents.append({"User-agent":agent})

	def get_working_proxy(self,proxy):
		if proxy == None:
			proxy = random.choice(self.proxies)
		url = 'https://google.com/'
		try:
			response = requests.get(self.proxy_url,proxies={"http": proxy, "https": proxy},timeout=5)
			if response.status_code == 200:
				return proxy.rstrip("\n")
			else:
				return self.get_working_proxy(None)
		except:
			return self.get_working_proxy(None)



#scanner = DirScanner("https://bekchy.com")