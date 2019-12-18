import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from queue import Queue
from urllib import parse
import re
from crawler import Crawler
import time
import asyncio
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import time
import socket

##login olması durumu sonra eklenecek


NORMAL		 = "thisissometest"
XSS_PAYLOAD  = "<script>alert(1)</script>"
XSS_PAYLOAD_REGEX  = r"<script>alert\(1\)</script>"

# her seferinde get ile url yi alıp öyle post atmak gerek kontrol et

class WorkerSignals(QObject):
    
    result_list     = pyqtSignal(str)
    info_box        = pyqtSignal(str)
    finish_control  = pyqtSignal()


class XssScanner(QRunnable):
	def __init__(self,url,login_form):
		super(XssScanner,self).__init__()
		self.login_form      = login_form
		self.session 		 = None
		self.signals 		 = WorkerSignals()
		self.url 			 = url
		self.base 			 = self.base_url(url)
		self.forms_get 		 = None
		self.forms_post 	 = None
		self.reflections 	 = set()
		self.possible_filter = set()
		self.possible_xss 	 = []
		self.uniq_actions 	 = []

		#self.login()
		# self.crawler = Crawler(url)
		# self.href_list, self.get_forms, self.post_forms 	= self.crawler.return_results()
		

		#self.print_hrefs()
	@pyqtSlot()
	def run(self):
		start_time = time.time()
		self.preperation()
		self.test_reflections()
		self.test_xss()
		finish_time = time.time()
		difference = finish_time-start_time
		self.signals.info_box.emit('[✔] Xss Scan Finished')
		self.signals.info_box.emit('Time taken: '+str(difference))
		self.signals.finish_control.emit()
	


	def preperation(self):
		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		self.headers 		= requests.utils.default_headers()
		self.headers['User-Agent'] = user_agent
		self.signals.info_box.emit("\t[+] Crawler started!")
		crawler 	= Crawler(self.url, self.login_form, quiet=True)
		crawler.run()
		self.href_list, self.forms_get, self.forms_post, self.session	= crawler.return_results()
		self.signals.info_box.emit("\t[+] Crawler Finished!")



		
	def create_form(self,_form,test_word):
		url, form 		= _form
		inputs 			= form.find_all("input")
		text_areas 		= form.find_all('textarea')
		action 			= form.get('action')
		form_dictionary = {}
		target			= ""	

		for input in inputs:
			input_name 		= input.get('name')
			input_type		= input.get('type')
			input_value 	= input.get('value')

			if input_type == "text": input_value = test_word

			form_dictionary[input_name] = input_value

		if text_areas:
			for area in text_areas:
				textarea_name 			 = area.get('name')
				textarea_value 			 = test_word
				form_dictionary[textarea_name] = textarea_value

		if action == "" or action == '#':
			target = url
		else:
			target = parse.urljoin(self.base,action)


		return url ,form_dictionary, target, form

			
	def test_reflections(self):

		for form in self.forms_post:

			url, form_dictionary, target, _form = self.create_form(form,NORMAL)

			response = self.session.post(target,data=form_dictionary,headers=self.headers)

			if re.search(NORMAL,response.text,re.IGNORECASE):

				if target not in self.uniq_actions:
					self.uniq_actions.append(target)
					self.reflections.add((url, _form))
					text = "Reflected -> "+str(target)
					self.signals.result_list.emit(text)
			else:
				pass

		for form in self.forms_get:
			url, form_dictionary, target, _form = self.create_form(form,NORMAL)

			response = self.session.get(target,params=form_dictionary,headers=self.headers)

			if re.search(NORMAL,response.text,re.IGNORECASE):

				if target not in self.uniq_actions:
					self.uniq_actions.append(target)
					self.reflections.add((url, _form))
			else:
				pass


	def test_xss(self):
		for form in self.reflections:
			url, form_dictionary, target, form = self.create_form(form,XSS_PAYLOAD)
			response = self.session.post(target,data=form_dictionary,headers=self.headers)


			if re.search(XSS_PAYLOAD_REGEX,response.text,re.IGNORECASE):
				text = "Possible XSS -> "+str(target)
				self.signals.result_list.emit(text)
			else:
				pass


	def base_url(self,url):
		parsed = urlparse(url)
		return parsed.scheme+"://"+parsed.netloc

	# def print_forms(self):
	# 	for form in self.forms_post:



# crawler 	= Crawler("http://testphp.vulnweb.com/")
# href_list,get_forms, post_forms, session	= crawler.return_results()

# scanner 	= XssScanner("http://testphp.vulnweb.com/", href_list,get_forms,post_forms,session)




























# 	def logout(self):
# 		response = requests.get("http://127.0.0.1/logout.php")

# 	def login(self):
# 		response = self.session.get("http://127.0.0.1/login.php")
# 		soup = BeautifulSoup(response.content,features="html.parser")

# 		_token = soup.find("input",attrs={"name":"user_token"}).get("value")
# 		print(_token)
# 		user = {
# 			'username':'admin',
# 			'password':'password',
# 			'user_token':_token,
# 			'Login':'Login',
# 		}
# 		response = self.session.post("http://127.0.0.1/login.php",data=user,headers=self.headers)
# 		print(response.content)
# 		return response.content


# 	def reset_db(self,content):
# 		soup = BeautifulSoup(content,features="html.parser")
# 		post_forms = soup.findAll("form",attrs={"method":"post"})

# 		for form in post_forms:
# 			_token = soup.find("input",attrs={"name":"user_token"}).get("value")
# 			value = _token = soup.find("input",attrs={"name":"create_db"}).get("value")
# 			reset_dbs = {
# 			'user_token':_token,
# 			'create_db':value,
# 			}

# 		response = self.session.post("http://127.0.0.1/setup.php",data=reset_dbs,headers=self.headers)
# 		#print(response.content)
# 		time.sleep(5)
# 		#print("sleeped")
# 		#print(response.content)

# # <form action="#" method="post">
# # 	<input name="create_db" type="submit" value="Create / Reset Database">
# # 	<input type='hidden' name='user_token' value='62cc1b1c4c81ef6d1f12cc6150ee5ea3' />
# # </form>	



	# def crawl(self):

	# 	for url in self.internal_hrefs:
	# 		try:
	# 			response = self.session.get(url,headers=self.headers)
	# 		except:
	# 			return
	# 		soup = BeautifulSoup(response.content,features="html.parser",from_encoding="iso-8859-1")

	# 		links = soup.find_all("a")
	# 		#print(links)
	# 		for link in links:
	# 			try:
	# 				if link["href"]:
	# 					mylink = link["href"]
	# 					# print(mylink)
	# 					if "#" in mylink:
	# 						mylink = mylink.split("#")[0]
	# 					#print(mylink)
	# 					url = parse.urljoin(self.base,mylink)
	# 					if self.check_existence(url):
	# 						if self.base in url:
	# 							self.internal_hrefs.append(url)
	# 							self.get_forms(url)
	# 							#print(url)
	# 						else:
	# 							self.external_hrefs.append(url)
	# 			except:
	# 				pass
