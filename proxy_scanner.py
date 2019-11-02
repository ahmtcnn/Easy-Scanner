import requests
import re
import threading
from queue import Queue
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
			print("proxy scan finished", len(self.working_proxies), "live proxy found.")
			self.write_file()
		else:
			print("Updated Proxy File Detected. Using Proxy File.")
			self.read_file()


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
			response = requests.get(self.url,proxies={"http": proxy, "https": proxy},timeout=3)
			with self.print_lock:
				print(proxy)
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







#scanner = ProxyScanner()

# proxies = scanner.return_proxies()

# print(proxies)


