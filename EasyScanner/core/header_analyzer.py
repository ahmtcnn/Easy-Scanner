import requests
import re
import urllib3
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class WorkerSignals(QObject):

    result_list   = pyqtSignal(str)
    finish_control = pyqtSignal()
    info_box = pyqtSignal(str)

class HeaderAnalyzer(QRunnable):
	def __init__(self,url):
		super(HeaderAnalysis, self).__init__()
		self.url = url
		self.signals = WorkerSignals()
		self.common_response_headers = []
		self.common_requests_headers = []
		self.response_headers = None
		self.request_headers = None
		self.get_headers()
		self.response_header_as_string = "|".join(self.response_headers)
		self.counter = 0

	@pyqtSlot()
	def run(self):
		self.check_x_xss_protection()
		self.check_x_frame_options()
		self.check_x_content_type_options()
		self.check_strict_transport_security()
		self.check_content_security_policy()
		self.check_x_content_security_policy()
		self.check_access_control_allow_origin()
		self.check_x_download_options()
		self.check_cache_control()
		self.check_x_permitted_Cross_Domain_Policies()
		self.read_header_files()
		self.check_uncommon_headers()
		self.signals.finish_control.emit()
		self.signals.info_box.emit("[+] Header Analysis finished!")

	def get_headers(self):
		try:
			self.response_headers = requests.get(self.url).headers
			self.request_headers = requests.get(self.url).request.headers
			
		except:
			pass

	def write_result(self,text):
		self.signals.result_list.emit(text)


	def test_possible_vulnerabilities(self):
		pass

	def check_x_xss_protection(self):
		if re.search("x-xss-protection",self.response_header_as_string,re.IGNORECASE):
			if self.response_headers["x-xss-protection"].startswith('1; mode=block') or (self.response_headers["x-xss-protection"]).startswith('1;mode=block'):
					text = "[+] (X-XSS-Protection) Cross-Site Scripting Protection is active"
					self.write_result(text)
					#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
					self.counter+=1
			else:
					text = "[-] (X-XSS-Protection) Server does not enabled Cross-Site Scripting Protection."
					self.write_result(text)
					#self.list.item(self.counter).setForeground(QBrush(Qt.red))
					self.counter+=1
		else:
			text = "[-] (X-XSS-Protection) Server does not enabled Cross-Site Scripting Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1


	def check_x_frame_options(self):
		if re.search("x-frame-options",self.response_header_as_string,re.IGNORECASE) and (self.response_headers["x-frame-options"]).lower() in ['deny', 'sameorigin']:
			text ="[+] (X-Frame-Options) Cross-Frame Scripting Scripting Protection is active."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
			self.counter+=1
		else:
			text = "[-] (X-Frame-Options) Server did not enable Cross-Frame Scripting Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1


	def check_x_content_type_options(self):
		if re.search("x-content-type-options",self.response_header_as_string,re.IGNORECASE) and self.response_headers["x-content-type-options"] == "nosniff":
				text = "[+] (X-Content-Type-Options) MIME-Sniffing Protection is active."
				self.write_result(text)
				#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
				self.counter+=1
		else:
			text = "[-] (X-Content-Type-Options) Server did not enable MIME-Sniffing Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1


	def check_strict_transport_security(self):
		if re.search("strict-transport-security",self.response_header_as_string,re.IGNORECASE):
				text = "[+] (Strict-Transport-Security) HTTP over TLS/SSL is active."
				self.write_result(text)
				#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
				self.counter+=1
		else:
			text = "[-] (Strict-Transport-Security) Server did not enable HTTP over TLS/SSL requirement Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1

	def check_content_security_policy(self):
		if re.search("content-security-policy",self.response_header_as_string,re.IGNORECASE):
			text = "[+] (Content-Security-Policy) Content Security Policy is active."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
			self.counter+=1
		else:
			text = "[-] (Content-Security-Policy) Server did not enable Content Security Policy Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1

	def check_x_content_security_policy(self):
		if re.search("x-content-security-policy",self.response_header_as_string,re.IGNORECASE):
				text = " (X-Content-Security-Policy) x-Content Security Policy is active."
				self.write_result(text)
				#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
				self.counter+=1
		else:
			text = "[-] (X-Content-Security-Policy) Server did not enable x-Content Security Policy Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1


	def check_access_control_allow_origin(self):
		if re.search("access_control_allow_origin",self.response_header_as_string,re.IGNORECASE):
			text = "[+] (Access-Control-Allow-Origin) Access Control Policies are active"
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
			self.counter+=1
		else:
			text = "[-] (Access-Control-Allow-Origin) Server did not enable Access Control Policies Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1

	def check_x_download_options(self):
		if re.search("x-download-options",self.response_header_as_string,re.IGNORECASE) and self.response_headers["x-download-options"] == "noopen":
			text = "[+] (X-Download-Options) File Download and Open Restriction Policies are active."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
			self.counter+=1
		else:
			text = "[-] (X-Download-Options) Server did not enable File Download and Open Restriction Policies Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1


	def check_cache_control(self):
		if re.search("cache-control",self.response_header_as_string,re.IGNORECASE) and (self.response_headers["cache-control"].startswith('private') or self.response_headers["cache-control"].startswith('no-cache')):
			text = "[+] (Cache-control) Private Caching or No-Cache is active."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
			self.counter+=1

		else:
			text = "[-] (Cache-control) Server did not enable Private Caching or No-Cache Protection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1
	def check_x_permitted_Cross_Domain_Policies(self):
		if re.search("X-Permitted-Cross-Domain-Policies",self.response_header_as_string,re.IGNORECASE): 
			if self.response_headers["X-Permitted-Cross-Domain-Policies"] == None or self.response_headers["X-Permitted-Cross-Domain-Policies"] == "master-only":
				text = "[+] (X-Permitted-Cross-Domain-Policies) X-Permitted-Cross-Domain-Policies are active."
				self.write_result(text)
				#self.list.item(self.counter).setForeground(QBrush(Qt.blue))	
				self.counter+=1
			else:
				text = "[-] X-Permitted-Cross-Domain-Policies) Server did not enable X-Permitted-Cross-Domain-PoliciesProtection."
				self.write_result(text)
				#self.list.item(self.counter).setForeground(QBrush(Qt.blue))
				self.counter+=1
		else:
			text = "[-] X-Permitted-Cross-Domain-Policies) Server did not enable X-Permitted-Cross-Domain-PoliciesProtection."
			self.write_result(text)
			#self.list.item(self.counter).setForeground(QBrush(Qt.red))
			self.counter+=1

	def check_uncommon_headers(self):
		lowercase = [item.lower() for item in self.common_response_headers]
		for header in self.response_headers:
			if not header in self.common_response_headers and not header in lowercase:
				text = "[?] Uncommon header ! : "+ str(header) + " : " + str(self.response_headers[header])
				self.write_result(text)
				#self.list.item(self.counter).setForeground(QBrush(Qt.black))
				self.counter+=1

	def read_header_files(self):
		with open("data/common_response_headers.txt") as fp:
			for line in fp:
				line = line.rstrip("\n")
				self.common_response_headers.append(line)
		with open("data/common_request_headers.txt") as fp:
			for line in fp:
				line = line.rstrip("\n")
				self.common_requests_headers.append(line)

#response.info().getheader('cache-control') and (response.info().getheader('cache-control').startswith('private') or response.info().getheader('cache-control').startswith('no-cache')):

# h = HeaderAnalysis("https://nintechnet.com")
# print(h.check_x_xss_protection())
# print(h.check_x_frame_options())
# print(h.check_x_content_type_options())
# print(h.check_strict_transport_security())
# print(h.check_content_security_policy())
# print(h.check_x_content_security_policy())
# print(h.check_access_control_allow_origin())
# print(h.check_x_download_options())
# print(h.check_cache_control())
# print(h.check_x_permitted_Cross_Domain_Policies())
# h.read_header_files()
# h.check_uncommon_headers()