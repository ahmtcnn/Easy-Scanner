import requests
from itertools import cycle
import traceback
from lxml.html import fromstring
import re
import string
from queue import Queue
import threading
from requests.exceptions import Timeout
#from proxy_scanner import *
from queue import Queue
import requests
import string
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import os
from datetime import datetime

class ProxyScanner():
	def __init__(self):
		self.all_proxies = []
		self.working_proxies = []
		if not self.read_file():
			self.print_lock = threading.Lock()
			self.q = Queue()
			self.url = 'https://httpbin.org/ip'
			self.start_threads()
			self.queue_proxies()
			self.q.join()
			print("Proxy scan stopped")
			self.write_file()
		else:
			self.read_file()
			print("Updated Proxy File Detected. Using Proxy File.")


	def get_proxies(self):
	    url = 'http://free-proxy-list.net/'
	    response = requests.get(url)

	    regex_ip = r'[0-9]+(?:\.[0-9]+){3}</td><td>[0-9]+'
	    proxy_ips = re.findall(regex_ip,response.text)

	    for i in proxy_ips:
	        i = i.replace("</td><td>",":")
	        self.all_proxies.append(i)
	    print(str(len(self.all_proxies)) + " different proxy")
	    return self.all_proxies


	def queue_proxies(self):
		proxies = self.get_proxies()
		for proxy in  proxies:
			self.q.put(proxy)

	def threader(self):
		while True:
			proxy = self.q.get()
			self.test_proxy(proxy)
			self.q.task_done()

	def test_proxy(self,proxy):
		try:
			response = requests.get(self.url,proxies={"http": proxy, "https": proxy},timeout=5)
			with self.print_lock:
				print(response.json())
			self.working_proxies.append(proxy)
		except:
			pass


	def start_threads(self):
		for _ in range(120):
			t = threading.Thread(target=self.threader)
			t.daemon= True
			t.start()

	def return_proxies(self):
		return self.working_proxies

	def write_file(self):
		now = datetime. now()
		time = str(now.day) +" "+ str(now.month) + " " + str(now.year)
		with open("proxy_list.txt","w+") as fp:
			fp.write(time+"\n")
			for proxy in self.working_proxies:
				fp.write(proxy+"\n")

	def read_file(self):
		now = datetime. now()
		time = str(now.day) +" "+ str(now.month) + " " + str(now.year)
		if(os.path.exists('data/proxy_list.txt')):
			with open("data/proxy_list.txt","r+") as fp:
				date = fp.readline()
				if time in date:
					for line in fp:
						self.working_proxies.append(str(line.rstrip("\n")))
					return True
				else:
					return False
		return False

class DirScanner:
	def __init__(self,url,proxy):
		self.startTime = time.time()
		self.OKGREEN = '\033[92m'
		self.ENDC = '\033[0m'
		self.WARNING = '\033[91m'
		self.TIMEOUT = '\033[95m'
		self.proxy_url ='http://free-proxy-list.net/'
		self.session = requests.Session()
		self.retry = Retry(connect=2, backoff_factor=0.5)
		self.adapter = HTTPAdapter(max_retries=self.retry)
		self.session.mount('http://', self.adapter)
		self.session.mount('https://', self.adapter)
		self.print_lock = threading.Lock()
		self.proxies = proxy
		self.headers = requests.utils.default_headers()
		self.user_agents = []
		self.read_user_agent_file()
	
		self.proxies = proxy
		self.url = url
		
		self.q = Queue()
		self.queue_dirs()
		self.start_threads()
		self.q.join()
		print("Directory scan Completed")
		print('Time taken:', time.time() - self.startTime)


	def queue_dirs(self):
		with open("directories2.dat","r") as fp:
			for line in fp:
				line = line.rstrip("\n")
				self.q.put(line)

	def get_proxies(self,proxies):
		self.proxies = proxies

	def test(self,word):
		url = self.url + "/" + word
		try:
			self.test_url(url,(3,5))
		except:
			pass

	def test_url(self,url,timeout):
		proxy = self.get_working_proxy(None)
		agent = random.choice(self.user_agents)
		header = self.headers.update(agent)
		
		response = self.session.get(url,proxies={"http": proxy, "https": proxy},headers=agent,timeout=timeout)
		if response.status_code == 200:
			with self.print_lock:
				print (self.OKGREEN + url + " : "+ str(response.status_code) + self.ENDC + self.TIMEOUT + "  " +"(used proxy "+ proxy+")" + self.ENDC)
		else:
			with self.print_lock:
				print (self.WARNING + url + " : "+ str(response.status_code) + self.ENDC + self.TIMEOUT + "  " +"(used proxy "+ proxy+")" + self.ENDC)		


	def threader(self):
		while True:
			word = self.q.get()

			self.test(word)
			self.q.task_done()	

	def start_threads(self):
		for _ in range(5):
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
		url = 'http://google.com/'
		try:
			response = requests.get(self.proxy_url,proxies={"http": proxy, "https": proxy},timeout=5)
			if response.status_code == 200:
				return proxy.rstrip("\n")
			else:
				return self.get_working_proxy(None)
		except:
			return self.get_working_proxy(None)

	def test_agent(self):
		proxy = random.choice(self.proxies)
		agent = random.choice(self.user_agents)
		print(agent)



proxy_scanner = ProxyScanner()
proxies = proxy_scanner.return_proxies()
scanner = DirScanner("http://bekchy.com",proxies)

