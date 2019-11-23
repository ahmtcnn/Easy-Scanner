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

#kendi cms mi yazacam

class WorkerSignals(QObject):
    
    domain_control = pyqtSignal(bool,str,str)
    info_liste   = pyqtSignal(str)
    control = pyqtSignal(bool)


class Info(QRunnable):
	def __init__(self,url):
		super(Info,self).__init__()
		self.devnull 		= open(os.devnull, 'w')
		self.signals 		= WorkerSignals()
		self.url 			= url
		self.url_without_schema = ""
		self.ip = None


	@pyqtSlot()
	def run(self):
		if self.check_domain():
			self.ping_domain()
			self.resolve_ip_address()
			self.check_http_request()
			self.get_tech_info()
			self.get_geo_location()
			self.signals.control.emit(True)


	def check_domain(self):
		is_url_valid = validators.url(self.url) and False or True
		parser = urlparse(self.url)
		self.url_without_schema = parser.netloc
		self.signals.domain_control.emit(is_url_valid,self.url,self.url_without_schema)
		return is_url_valid



	def ping_domain(self):
		#print("test2")
		parser = urlparse(self.url)
		url_without_schema = parser.netloc
		response =  subprocess.run(["ping","-c", "1",url_without_schema],stdout=self.devnull, stderr=self.devnull)
		if response.returncode == 0:
			self.signals.info_liste.emit("[✔] Ping Successfull")
			return True
		else: 
			self.signals.info_liste.emit("[×] Ping Failed ×")
			return False


	def resolve_ip_address(self):
		try:
			ip = socket.gethostbyname(self.url_without_schema)
			self.signals.info_liste.emit("[✔] Ip Address Resolved : "+ip)
			self.ip = ip
		except:
			self.signals.info_liste.emit("[×] Ip Address Couldn't Resolved")
			self.ip = None

	def check_http_request(self):
		headers = requests.utils.default_headers()
		session = requests.session()
		try:
			response = session.get(self.url,allow_redirects=True,verify=True,timeout=10)
			if response.status_code == 200:
				self.signals.info_liste.emit("[✔] Http Response Status Code: "+str(response.status_code)+" Successfull")
				return True
			else:
				self.signals.info_liste.emit("[×] Http Response Status Code "+str(response.status_code))
				return False
		except:
			self.signals.info_liste.emit("[×] Http Connection Failed ")
			return False


	def get_geo_location(self):
		if self.ip:
			response = DbIpCity.get(self.ip, api_key='free')
			location = response.city +" / "+ response._region + " / " + response.country
			location_url = "https://maps.google.com/?q="+str(response.latitude)+","+str(response.longitude)
			self.signals.info_liste.emit("[✔] Ip address location: " + location)
			self.signals.info_liste.emit("[✔] Location link via google map: "+location_url)
		else:
			self.signals.info_liste.emit("[×] Location couldn't found due to ip resolving issues: "+location_url)


	def get_tech_info(self):
		try:
			response = builtwith(self.url)
			self.parse_and_print(response)
		except:
			self.signals.info_liste.emit("[×] Couldn't get website technology information")
			#print("Error with builtwith")
		

	def parse_and_print(self,response):
		text = "[✔] Some Web Technologies Determined"
		self.signals.info_liste.emit(text)
		for key in response:
			text = "\t[+] " + str(key) + " : " + str(response[key][0])
			#print(text)
			self.signals.info_liste.emit(text)
			#self.signals.list.emit(self.counter,text)

 		

