
from crawler import Crawler
from urllib.parse import urlparse,parse_qs
import re
import requests
import time
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


# lfi yapıldı ancak rfi yapmadık
# formlar test edilecek aynı düzende
#sadecee urllerde arayacam, regex oluşturcam, query string varsa ve file varsa testler yapılacak
# ilk passwd cıktısına bakılacak yoksa bilinen hatalara bakılacak.
FILE_REGEX = r'.*\.[a-zA-z_]{1,5}'
PASSWD_REGEX = r'^(root):.*:*:*'
ERROR_REGEX = r'.*(Warning).*(include)*.*'


class WorkerSignals(QObject):
    
    result_list     = pyqtSignal(str)
    info_box        = pyqtSignal(str)
    finish_control  = pyqtSignal()



class FileInclusionScanner(QRunnable):
	def __init__(self,url,login_form):
		super(FileInclusionScanner,self).__init__()
		self.login_form = login_form
		self.url = url
		self.parameterized_hrefs = []
		self.tried_urls = []
		self.error_based_detections = []
		self.certain_detections = []
		self.signals = WorkerSignals()



	@pyqtSlot()
	def run(self):
		start_time = time.time()
		self.signals.info_box.emit("\t[+] Crawler Started!")
		crawler =Crawler(self.url,self.login_form,quiet=True)
		crawler.run()
		self.internal_hrefs, self.get_forms, self.post_forms, self.session	= crawler.return_results()
		self.signals.info_box.emit("\t[+] Crawler Finished!")
		self.get_parameterized_hrefs()
		self.check_file_in_parameters()
		finish_time = time.time()
		difference = finish_time - start_time
		self.signals.finish_control.emit()
		self.signals.info_box.emit("[✔] File Inclusion Scan Finished!")
		self.signals.info_box.emit("Time taken: "+str(difference))

	def get_parameterized_hrefs(self):
		for url in self.internal_hrefs:
			parsed = urlparse(url)
			try:
				query = parsed.query
				if query != "":
					self.parameterized_hrefs.append(url)
			except:
				pass

	def check_file_in_parameters(self):
		for url in self.parameterized_hrefs:
			self.test_url(url)


	def test_url(self,url):
		parsed = urlparse(url)
		queries = parse_qs(parsed.query)
		with open("data/file_inclusion.dat","r") as fp:
			for key in queries.keys():
				for line in fp:
					payload = line.rstrip('\n')
					query = key+"="+ payload
					self.analysis_response(parsed._replace(query=query))


	def analysis_response(self,parsed):
		url = parsed.geturl()
		query = parsed.query
		path = parsed.path
		vulnerable_path = (path,query.split("=")[0])
		response = self.session.get(url)

		if vulnerable_path not in self.certain_detections:
			if re.search(PASSWD_REGEX,str(response.text)):
				text = "Possible LFi detected (able to read '/etc/passwd' file)-> "+ str(url)
				self.signals.result_list.emit(text)
				print("Possible LFi detected (able to read '/etc/passwd' file)-> ", url)
				self.certain_detections.append((parsed.path,parsed.query.split("=")[0]))

		if vulnerable_path not in self.error_based_detections:	
			if re.search(ERROR_REGEX,str(response.text),re.IGNORECASE):
				text = "Possible LFi detected (Error detected)-> "+ str(url)
				self.signals.result_list.emit(text)
				print("Possible LFi detected -> ", url)
				self.error_based_detections.append((parsed.path,parsed.query.split("=")[0]))








# scanner = FileInclusionScanner("http://testphp.vulnweb.com/")
