from PyQt5.QtCore import QObject,pyqtSignal,QRunnable,pyqtSlot
from ip2geotools.databases.noncommercial import DbIpCity
from helpers.waf_analysis import WafAnalysis
from helpers.worker_signals import WorkerSignals
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
from builtwith import *
import dns.resolver
import validators
import subprocess
import requests
import socket
import time



class InfoCollector(QRunnable):
	def __init__(self,url):
		"""Our Constructor Method"""
		super(InfoCollector,self).__init__()
		self.devnull 		 = open(os.devnull, 'w')
		self.signals 		 = WorkerSignals()
		self.allowed_methods = set()
		self.ip 			 = None
		self.url 			 = url
		self.plain_url 		 = self._plain_url


	@pyqtSlot()
	def run(self):
		"""We are running our modules"""

		self.start_time 	= time.time()
		self.ping_domain()
		self.resolve_ip_address()
		self.check_http_status()
		self.get_tech_info()
		self.get_geo_location()
		self.find_allowed_methods()
		self.resolve_dns()
		self.check_wayback_machine()
		self.get_ip_history()
		self.analyze_waf()
		self.get_whois()

		finish_time = time.time()
		time_taken = finish_time - self.start_time

		self.signals.finish_control.emit()
		self.signals.info_box.emit("[✔] Infomation Gathering finished!")
		self.signals.info_box.emit("Time taken: %.3f" % time_taken)

	@property
	def _plain_url(self):
		""" Return plain text url e.g (example.com)"""

		parser = urlparse(self.url)
		return parser.netloc


	def ping_domain(self):
		"""Ping with plain url and see if Host is alive"""
		response =  subprocess.run(["ping","-c", "1",self.plain_url], stdout=self.devnull, stderr=self.devnull)
		if response.returncode == 0:
			self.signals.result_list.emit("[✔] Ping Successfull")
			return True
		else: 
			self.signals.result_list.emit("[×] Ping Failed ×")
			return False


	def resolve_ip_address(self):
		"""Try to resolve ip address of Host"""
		try:
			ip = socket.gethostbyname(self.plain_url)
			self.ip = ip

			self.signals.result_list.emit("\n[✔] Ip Address Resolved:")
			self.signals.result_list.emit("\t[+] " +ip)
		except:
			self.signals.result_list.emit("[×] Ip Address Couldn't Resolved")


	def check_http_status(self):
		"""Checking HTTP status code when requesting page"""

		headers = requests.utils.default_headers()
		session = requests.session()
		try:
			response = session.get(self.url,allow_redirects=True,verify=True,timeout=10)
			if response.status_code == 200:
				self.signals.result_list.emit("\n[✔] HTTP Response Status Code: "+str(response.status_code)+" Successfull")
				return True
			else:
				self.signals.result_list.emit("\n[×] Http Response Status Code "+str(response.status_code))
				return False
		except:
			self.signals.result_list.emit("[×] \nHTTP Connection Failed ")
			return False


	def get_geo_location(self):
		"""Getting ip GEO location with dpIpCity free API"""

		if self.ip:
			try:
				response = DbIpCity.get(self.ip, api_key='free')
				location = response.city +" / "+ response._region + " / " + response.country
				location_url = "https://maps.google.com/?q="+str(response.latitude)+","+str(response.longitude)

				self.signals.result_list.emit("\n[✔] Ip address location:")
				self.signals.result_list.emit("\t[+] "+location)
				self.signals.result_list.emit("\n[✔] Ip Location link via google map:")
				self.signals.result_list.emit("\t[+] "+ location_url)
			except:
				self.signals.result_list.emit("\n[×] Ip Location couldn't found due to ip resolving issues: ")

		else:
			self.signals.result_list.emit("[×] Ip Location couldn't found due to ip resolving issues: ")


	def get_tech_info(self):
		"""Getting web technology information via buildwith API"""
		try:
			response = builtwith(self.url)
			self.parse_and_print(response)
		except:
			self.signals.result_list.emit("[×] Couldn't get website technology information")
			#print("Error with builtwith")
		

	def parse_and_print(self,response):
		"""Helper function for 'get_tech_info'"""

		if response == {}:
			info = "\n[×] Couldn't get website technology information"
			self.signals.result_list.emit(info)
		else:
			info = "\n[✔] Some Web Technologies Determined"
			self.signals.result_list.emit(info)

			for key in response:
				text = "\t[+] " + str(key) + " : " + str(response[key][0])
				self.signals.result_list.emit(text)



	def find_http_method_with_trying(self):
		"""Finding allowed HTTP method with trying every one of them"""

		info = "\n[✔] Testing http method manually for given url..."
		self.signals.result_list.emit(info)
		methods = ['GET','POST','PUT','DELETE','OPTIONS','HEAD','CONNECT','TRACE','PATCH']
		for method in methods:
			try:
				response = requests.request(method,url=self.url)
				print(response.status_code)
				if response.status_code == 200:
					info = "\t[+] "+str(method)+" "+str(response.status_code)
					self.signals.result_list.emit(info)
			except:
				pass

	def find_http_method_with_options(self):
		"""Finding allowed HTTP methods by sending OPTION header to HOST"""

		info = "\n[✔] Testing http methods with OPTION header.."
		self.signals.result_list.emit(info)
		
		url1 = "http://"+self.plain_url
		url2 = "https://"+self.plain_url
		self.test_url(url1)
		self.test_url(url2)

	def test_url(self,url):
		"""Helper function for finding HTTP method with options"""
		try:
			response = requests.options(url)
			for i in response.headers:
				if i == "Allow":
					for method in response.headers[i].split(","):
						info = "\t[+] "+str(method)
						self.signals.result_list.emit(info)
		except Exception as e:
			print(e)

	def find_allowed_methods(self):
		"""Main function for two kind of findings"""

		self.find_http_method_with_options()
		self.find_http_method_with_trying()


	def resolve_dns(self):
		"""Trying to resolve Nameservers for HOST via dns.resolver"""

		self.signals.result_list.emit("\n[✔] Trying to get nameservers ")
		try:
			nameservers = dns.resolver.query(self.plain_url,'NS')
			for data in nameservers:
				self.signals.result_list.emit("\t[+] " +str(data))
		except:
			self.signals.result_list.emit("\n[×] Error occured while Nameserver resolving ")

	def check_wayback_machine(self):
		""" Checks and gives latest wayback machine snapshot's link" via API"""

		self.signals.result_list.emit("\n[✔] Querying for wayback machine snapshots ")

		resp = requests.get("http://archive.org/wayback/available?url="+self.plain_url)
		resp = resp.json()

		if resp['archived_snapshots'] == {}:
			self.signals.result_list.emit("\t[-] No snapshots available. ")
		else:
			self.signals.result_list.emit("\t[+] Snapshots available ")
			closest_snapshot = resp['archived_snapshots']['closest']['url']
			self.signals.result_list.emit("\t[+] "+ closest_snapshot)


	# API da var
	def get_ip_history(self):
		"""Getting ip history via viewdns and parse result"""

		self.signals.result_list.emit("\n[✔] Trying to get ip history")
		headers = requests.utils.default_headers()
		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		headers['User-Agent'] = user_agent
		session = requests.session()

		resp = session.get("https://viewdns.info/iphistory/?domain="+self.plain_url,headers=headers)

		if 'try again' in resp.text:
			self.signals.result_list.emit("\t[×] Couldn't get ip history ")
		soup = BeautifulSoup(resp.content, 'html.parser',from_encoding="iso-8859-1")
		tables = soup.find_all("table")
		tds = tables[3].find_all('td')
		control=1
		for i in tds[3::]:
			self.signals.result_list.emit("\t[+] "+i.text)
			
	def get_whois(self):
		"""Getting Whois Information via whois.com and parsing result"""

		self.signals.result_list.emit("\n[✔] Trying to get whois info")
		resp = requests.get("https://www.whois.com/whois/"+self.plain_url)

		soup = BeautifulSoup(resp.content,'html.parser')
		raw_data = soup.find('pre',{'id':"registrarData",'class':'df-raw'})
		if raw_data != None:
			text = raw_data.text
			self.signals.result_list.emit("\t[+] "+text)
		else:
			text = "Couldn't get whois info"
			self.signals.result_list.emit("\t[-] "+text)


	def analyze_waf(self):
		"""Analyze WAF or other backend services through headers and responses"""

		self.signals.result_list.emit("\n[✔] Trying to get Waf/Backend Systems")
		waf_analysis = WafAnalysis(self.url)
		guess = waf_analysis.return_result()
		self.signals.result_list.emit("\t[+] "+str(guess))
		

