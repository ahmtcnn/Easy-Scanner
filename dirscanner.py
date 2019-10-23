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

import threading
from queue import Queue
import requests
import re
import string
import random

class ProxyScanner():
	def __init__(self):
		self.all_proxies = []
		self.working_proxies = []
		self.print_lock = threading.Lock()
		self.q = Queue()
		self.url = 'https://httpbin.org/ip'
		self.start_threads()
		self.queue_proxies()
		self.q.join()
		print("Proxy scan stopped")


	def get_proxies(self):
	    url = 'http://free-proxy-list.net/'
	    response = requests.get(url)

	    regex_ip = r'[0-9]+(?:\.[0-9]+){3}</td><td>[0-9]+'
	    proxy_ips = re.findall(regex_ip,response.content)

	    for i in proxy_ips:
	        i = string.replace(i,"</td><td>",":")
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
		    with self.print_lock:
		    	print("Proxy test failed!")


	def start_threads(self):
		for _ in range(200):
			t = threading.Thread(target=self.threader)
			t.daemon= True
			t.start()

	def return_proxies(self):
		return self.working_proxies

class DirScanner:
	def __init__(self,url,proxy):
		self.OKGREEN = '\033[92m'
		self.ENDC = '\033[0m'
		self.WARNING = '\033[91m'
		self.TIMEOUT = '\033[95m'
		self.proxy_url ='http://free-proxy-list.net/'
		self.proxies = proxy
		self.headers = requests.utils.default_headers()
		self.user_agents = []
		self.read_user_agent_file()
		self.retry_lock = threading.Lock()
		self.proxies = proxy
		self.url = url
		self.print_lock = threading.Lock()
		self.q = Queue()
		self.queue_dirs()
		self.start_threads()
		self.q.join()
		print("Directory scan Completed")


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
			self.test_url(url,(5,10))

		except Timeout:
			try:
				self.test(url,(10,15))
			except Timeout:
				with self.print_lock:
					print (self.TIMEOUT + url + " : "+ str(408) +  " Timeout!" +self.ENDC )
			except:
				with self.print_lock:
					print("except")
		except:
			with self.print_lock:
				print("except")

	def test_url(self,url,timeout):
		proxy = self.get_working_proxy(None)
		agent = random.choice(self.user_agents)

		header = self.headers.update(agent)
			
		response = requests.get(url,proxies={"http": proxy, "https": proxy},headers=agent,timeout = (6,10))
		if response.status_code != 404:
			with self.print_lock:
				print (self.OKGREEN + url + " : "+ str(response.status_code) + self.ENDC)
		else:
			with self.print_lock:
				print (self.WARNING + url + " : "+ str(response.status_code) + self.ENDC)		


	def threader(self):
		while True:
			word = self.q.get()

			self.test(word)
			self.q.task_done()	

	def start_threads(self):
		for _ in range(200):
			t = threading.Thread(target = self.threader)
			t.daemon = True
			t.start()

	def read_user_agent_file(self):
		with open("user_agents.dat","r+") as fp:
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
				return proxy
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
scanner = DirScanner("http://ahmetcankaraagacli.com",proxies)

