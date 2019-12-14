import requests
import subprocess
import socket
from ip2geotools.databases.noncommercial import DbIpCity
import os
from urllib.parse import urlparse,urljoin
import validators
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from urllib.parse import urlparse
from builtwith import *
import time
import dns.resolver
from bs4 import BeautifulSoup


# allowed methoduna exception koyulacak
#kendi cms mi yazacam
#	46f9c42a5590420ea7bfa3297f853c14fb46aa96  API KEY dnsview
# shodan kullan
# archive.com'un linki 
# diğer şeylere de bak
#whois eklenecek
class WorkerSignals(QObject):
    
    result_list   = pyqtSignal(str)
    finish_control = pyqtSignal()
    info_box = pyqtSignal(str)


class Info(QRunnable):
	def __init__(self,url):
		super(Info,self).__init__()
		self.devnull 		= open(os.devnull, 'w')
		self.signals 		= WorkerSignals()
		self.url 			= url
		self.url_without_schema = ""
		self.ip = None
		self.allowed_methods = set()
		self.start_time = time.time()



	@pyqtSlot()
	def run(self):
		self.ping_domain()
		self.resolve_ip_address()
		self.check_http_request()
		self.get_tech_info()
		self.get_geo_location()
		self.find_allowed_methods()
		self.resolve_dns()
		self.check_wayback_machine()
		self.get_ip_history()
		self.get_whois()
		later = time.time()
		time_taken = later - self.start_time

		self.signals.finish_control.emit()
		self.signals.info_box.emit("[✔] Infomation Gathering finished!")
		self.signals.info_box.emit("Time taken: %.3f" % time_taken)


	def ping_domain(self):
		parser = urlparse(self.url)
		self.url_without_schema = parser.netloc
		response =  subprocess.run(["ping","-c", "1",self.url_without_schema], stdout=self.devnull, stderr=self.devnull)
		if response.returncode == 0:
			self.signals.result_list.emit("[✔] Ping Successfull")
			return True
		else: 
			self.signals.result_list.emit("[×] Ping Failed ×")
			return False


	def resolve_ip_address(self):
		try:

			ip = socket.gethostbyname(self.url_without_schema)
			print(ip)
			self.signals.result_list.emit("\n[✔] Ip Address Resolved:")
			self.signals.result_list.emit("\t[+] " +ip)
			self.ip = ip
		except:
			#response = subprocess.run(["ping", "-c", "1", "ahmetcankaraagacli.com", "|", "awk", "'NR==1{gsub(/\(|\)/,"",$3);print $3}'"])
			#print(response)
			self.signals.result_list.emit("[×] Ip Address Couldn't Resolved")
			self.ip = None


	def check_http_request(self):
		headers = requests.utils.default_headers()
		session = requests.session()
		try:
			response = session.get(self.url,allow_redirects=True,verify=True,timeout=10)
			if response.status_code == 200:
				self.signals.result_list.emit("\n[✔] Http Response Status Code: "+str(response.status_code)+" Successfull")
				return True
			else:
				self.signals.result_list.emit("\n[×] Http Response Status Code "+str(response.status_code))
				return False
		except:
			self.signals.result_list.emit("[×] \nHttp Connection Failed ")
			return False


	def get_geo_location(self):
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
		try:
			response = builtwith(self.url)
			self.parse_and_print(response)
		except:
			self.signals.result_list.emit("[×] Couldn't get website technology information")
			#print("Error with builtwith")
		

	def parse_and_print(self,response):
		if response == {}:
			text = "\n[×] Couldn't get website technology information"
		else:
			text = "\n[✔] Some Web Technologies Determined"
		self.signals.result_list.emit(text)
		print(response)
		for key in response:
			text = "\t[+] " + str(key) + " : " + str(response[key][0])
			#print(text)
			self.signals.result_list.emit(text)
			#self.signals.list.emit(self.counter,text)


	def find_http_method_with_trying(self):
		text = "[✔] Testing http method manually for given url..."
		self.signals.result_list.emit(text)
		methods = ['GET','POST','PUT','DELETE','OPTIONS','HEAD','CONNECT','TRACE','PATCH']
		for method in methods:
			try:
				response = requests.request(method=method,url=self.url,timeout=5)
				if response.status_code != 405:
					self.allowed_methods.add(method)
			except:
				pass

	def find_http_method_with_options(self):
		text = "\n[✔] Testing http methods with OPTION header.."
		self.signals.result_list.emit(text)
		
		#resp = requests.request(method='OPTIONS', url="https://ahmetcankaraagacli.com")
		url1 = "http://"+self.url_without_schema
		url2 = "https://"+self.url_without_schema
		self.test_url(url1)
		self.test_url(url2)

	def test_url(self,url):
		try:
			resp = requests.options(url,timeout=4)
			for i in resp.headers:
				if i == "Allow":
					print(i,resp.headers[i])
					allows = resp.headers[i].split(",")
					for j in allows:
						working_methods.add(j)
		except:
			pass

	def find_allowed_methods(self):
		self.find_http_method_with_options()
		self.find_http_method_with_trying()
		for i in self.allowed_methods:
			self.signals.result_list.emit("\t[+] " +i)


	def resolve_dns(self):
		try:
			self.signals.result_list.emit("\n[✔] Trying to get nameservers ")
			nameservers = dns.resolver.query(self.url_without_schema,'NS')
			for data in nameservers:
				self.signals.result_list.emit("\t[+] " +str(data))
		except:
			pass

	def check_wayback_machine(self):
		self.signals.result_list.emit("\n[✔] Querying for wayback machine snapshots ")
		resp = requests.get("http://archive.org/wayback/available?url="+self.url_without_schema)
		resp = resp.json()

		if resp['archived_snapshots'] == {}:
			self.signals.result_list.emit("\t[-] No snapshots available. ")
		else:
			self.signals.result_list.emit("\t[+] Snapshots available ")
			closest_snapshot = resp['archived_snapshots']['closest']['url']
			self.signals.result_list.emit("\t[+] "+ closest_snapshot)


	# API da var
	def get_ip_history(self):
		self.signals.result_list.emit("\n[✔] Trying to get ip history")
		headers 		= requests.utils.default_headers()
		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		headers['User-Agent'] = user_agent
		session = requests.session()
		resp = session.get("https://viewdns.info/iphistory/?domain="+self.url_without_schema,headers=headers)
		if 'try again' in resp.text:
			self.signals.result_list.emit("\t[×] Couldn't get ip history ")
		soup = BeautifulSoup(resp.content, 'html.parser')
		tables = soup.find_all("table")
		tds = tables[3].find_all('td')
		control=1
		for i in tds[3::]:
			self.signals.result_list.emit("\t[+] "+i.text)
			
	def get_whois(self):
		self.signals.result_list.emit("\n[✔] Trying to get whois info")
		resp = requests.get("https://www.whois.com/whois/"+self.url_without_schema)

		soup = BeautifulSoup(resp.content,'html.parser')
		raw_data = soup.find('pre',{'id':"registrarData",'class':'df-raw'})
		if raw_data != None:
			text = raw_data.text
			self.signals.result_list.emit("\t[+] "+text)
		else:
			text = "Couldn't get whois info"
			self.signals.result_list.emit("\t[-] "+text)


	def __del__(self):
		print('Destructor called, info deleted.')

