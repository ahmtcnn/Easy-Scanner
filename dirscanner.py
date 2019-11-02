import requests
import re
from queue import Queue
import threading
from queue import Queue
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
from proxy_scanner import ProxyScanner

class DirScanner():
	def __init__(self,url,tab,bar):
		self.startTime = time.time()
		self.num_lines = 0
		self.bar = bar
		self.tab = tab
		self.counter = 0
		self.dir_counter = 0
		self.num_lines
		self.tab.insertItem(self.counter,"Proxy Scan started..")
		proxy_scanner = ProxyScanner()
		self.proxies = proxy_scanner.return_proxies()
		self.counter+=1
		self.tab.insertItem(self.counter,"Proxy Scan Finished..Using "+str(len(self.proxies))+ "live proxy")
		self.proxy_url ='http://free-proxy-list.net/'
		self.session = requests.Session()
		self.retry = Retry(connect=2, backoff_factor=0.3)
		self.adapter = HTTPAdapter(max_retries=self.retry)
		self.session.mount('http://', self.adapter)
		self.session.mount('https://', self.adapter)
		self.print_lock = threading.Lock()
		self.headers = requests.utils.default_headers()
		self.user_agents = []
		self.read_user_agent_file()
		self.url = url
		self.q = Queue()
		self.queue_dirs()
		self.start_threads()
		self.q.join()
		time = (time.time() - self.startTime)
		self.tab.insertItem(self.counter,"Directory scan completed! Time taken: "+str(time))
		print('Time taken:', time.time() - self.startTime)


	def queue_dirs(self):
		self.num_lines = sum(1 for line in open('data/directoriestest.dat'))
		with open("data/directoriestest.dat","r") as fp:
			for line in fp:
				line = line.rstrip("\n")
				self.q.put(line)

	def get_proxies(self,proxies):
		self.proxies = proxies

	def test(self,word):
		url = self.url + "/" + word
		try:
			self.test_url(url,(2,4))
		except:
			pass
		self.dir_counter+=1
		text = "[" + str(self.dir_counter) + " / " + str(self.num_lines) + "]"
		self.bar.setFormat( text );
		self.bar.setValue(self.dir_counter)

	def test_url(self,url,timeout):


		proxy = self.get_working_proxy(None)
		agent = random.choice(self.user_agents)
		header = self.headers.update(agent)
		try:
			response = self.session.get(url,proxies={"http": proxy, "https": proxy},headers=agent,timeout=timeout)
			if response.status_code == 200:
				with self.print_lock:
					self.counter+=1
					self.tab.insertItem(self.counter,url + " : " +str(response.status_code))
		except:
			pass



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



#scanner = DirScanner("https://bekchy.com")