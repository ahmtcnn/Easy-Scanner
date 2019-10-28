import threading
from queue import Queue
import requests
import re
import string
from datetime import datetime

class ProxyScanner():
	def __init__(self):
		self.all_proxies = []
		self.working_proxies = []
		self.print_lock = threading.Lock()
		self.q = Queue()
		self.count = 0
		self.url = 'https://httpbin.org/ip'
		self.start_threads()
		self.queue_proxies()
		self.q.join()
		self.write_file()
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
				print(str(self.count)+response.json())
			self.working_proxies.append(proxy)

		except:
		    with self.print_lock:
		    	print(str(self.count)+"Proxy test failed!")


	def start_threads(self):
		for _ in range(50):
			t = threading.Thread(target=self.threader)
			t.daemon= True
			t.start()

	def return_proxies(self):
		return self.working.proxies

	def write_file(self):
		now = datetime. now()
		time = str(now.day) +" "+ str(now.month) + " " + str(now.year)
		with open("data/proxy_list","w+") as fp:
			fp.write(time)
			fp.write(self.working_proxies)







scanner = ProxyScanner()

# proxies = scanner.return_proxies()

# print(proxies)


