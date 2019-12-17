import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from queue import Queue
from urllib import parse
import asyncio
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import time
import socket
import re


REGEX_FOR_LOGOUT = ".*(logout).*"

#internal hrefs before and after login

class WorkerSignals(QObject):
    
    result_list     = pyqtSignal(str)
    info_box        = pyqtSignal(str)
    finish_control  = pyqtSignal()


class Crawler(QRunnable):
	def __init__(self,url,login_form,quiet=False,form_scan=True):
		super(Crawler,self).__init__()
		print("crawler started")
		self.form_scan      = form_scan
		self.quiet 			= quiet
		self.login_form 	= login_form
		self.url 			= url
		self.internal_hrefs = []
		self.external_hrefs = []
		self.forms_get 		= set()
		self.forms_post 	= set()
		self.form_urls 		= set()
		self.srcs 			= set()
		self.base 			= self.base_url
		self.signals 		= WorkerSignals()
		

	@pyqtSlot()
	def run(self):
		print(self.login_form)
		start_time = time.time()
		self.preperation()
		#self.crawl()
		if self.login_form != None:
			print("login oldu")
			self.login()
		self.crawl()
		self.get_forms_from_list()
		finish_time = time.time()
		difference = finish_time - start_time
		self.signals.finish_control.emit()
		self.signals.info_box.emit("[✔] Crawler Finished!")
		self.signals.info_box.emit("Time Taken: "+str(difference))



	def return_results(self):
		return (self.internal_hrefs , self.forms_get, self.forms_post, self.session)


	def preperation(self):
		print("BASE: "+ self.base)
		self.internal_hrefs.append(self.url)
		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		self.headers 		= requests.utils.default_headers()
		self.headers['User-Agent'] = user_agent
		self.session 		= requests.session()


	def login(self):

		action 					= self.login_form['action']
		form_url 				= self.login_form['url']

		response = self.session.get(form_url,headers=self.headers)
		soup = BeautifulSoup(response.content,features="html.parser",from_encoding="iso-8859-1")#,from_encoding="iso-8859-1"
		forms = soup.findAll("form",attrs={"method":re.compile("POST", re.IGNORECASE)})
		# if len(forms) == 1:
		# 	form = forms[0]
		# else:
		form = self.find_login_form(forms)

		# print(form)

		form_dictionary = self.create_login_form(form)

		try:
			response = self.session.post(action,data=form_dictionary,headers=self.headers)

		except Exception as e:
			print("Error while login: ",e)

	def find_login_form(self,forms):
		action = self.login_form['action']
		for form in forms:
			form_action = form.get('action')
			if form_action == "" or form_action == '#':
				form_action = form_url
			else:
				form_action = parse.urljoin(self.url,form_action)


			form_action = urlparse(form_action)
			_action = urlparse(action)
			if form_action.netloc == _action.netloc and form_action.path == _action.path:
				return form



	def create_login_form(self,form):
		user_name_field 		= self.login_form['user_name_field']
		user_value_field 		= self.login_form['user_value_field']
		password_name_field 	= self.login_form['password_name_field']
		password_value_field 	= self.login_form['password_value_field']
		form_dictionary 		= {}
		inputs 					= form.find_all("input")

		for input in inputs:
			input_name 		= input.get('name')
			input_type		= input.get('type')
			input_value 	= input.get('value')

			if input_name == user_name_field: 
				form_dictionary[input_name] = user_value_field
			elif input_name == password_name_field:
				form_dictionary[input_name] = password_value_field
			else:
				form_dictionary[input_name] = input_value

		return form_dictionary


	def create_form(self,form):
			url, form 		= _form
			#print(form)
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
				#print(target)
			else:
				target = parse.urljoin(self.base,action)
				#print(target)

			return url ,form_dictionary, target, form


	def crawl(self):
		
		for url in self.internal_hrefs:
			try:
				response = self.session.get(url,headers=self.headers)
			except:
				return
			soup = BeautifulSoup(response.content,features="html.parser",from_encoding="iso-8859-1")

			links = soup.find_all("a")
			imgs = soup.find_all('img')
			for link in links:
				try:
					if link["href"]:
						mylink = link["href"]
						if "#" in mylink:
							mylink = mylink.split("#")[0]
						url = parse.urljoin(self.base,mylink)
						if self.check_existence(url):
							if self.base in url:
								self.internal_hrefs.append(url)
								print(url)
								if not self.quiet:
									self.signals.result_list.emit(str(url))
								# if self.form_scan:
								# 	self.get_forms(url)
							else:
								self.external_hrefs.append(url)
				except:
					pass
			for img in imgs:
				self.srcs.add(img['src'])



	def check_existence(self,url):
		if url in self.internal_hrefs:
			return False
		else:
			return True

	@property
	def base_url(self):
		parsed = urlparse(self.url)
		return parsed.scheme+"://"+parsed.netloc

	def print_hrefs(self):
		for i in self.internal_hrefs:
			print(i)

	def print_post_forms(self):
		print("POST FORMS")
		for i in self.forms_post:
			print(i)

	def print_get_forms(self):
		print("GET FORMS")
		for i in self.forms_get:
			print(i)


	def get_headers(self,url):
		response = self.session.get(url,headers=self.headers)
		for key in response.headers:
			print(key + " : " +response.headers[key])

		print("************** RESPONSE *****************")

		for key in response.request.headers:
			print(key + " : " +response.request.headers[key])


	def get_forms_from_list(self):
		if self.login_form != None:
			print("login oldu")
			self.login()
		
		for url in self.internal_hrefs:
			if not re.search(REGEX_FOR_LOGOUT,url):
				self.get_forms(url)
			else:
				print("test ",url)

			


	def get_forms(self,url):
		response = self.session.get(url,headers=self.headers)

		soup = BeautifulSoup(response.content,features="html.parser",from_encoding="iso-8859-1")

		post_forms = soup.findAll("form",attrs={"method":re.compile("POST", re.IGNORECASE)})
		get_forms = soup.findAll("form",attrs={"method":re.compile("GET", re.IGNORECASE)})
		if url == "http://192.168.1.101/vulnerabilities/upload/":
			print("*****",post_forms)

		for form in post_forms:
			self.forms_post.add((url,form))
			
		for form in get_forms:
			self.forms_get.add((url,form))


	def is_redirection(self,href):
		http_start_position = re.search(self.url,href)


		if http_start_position:
			return http_start_position.start() == 0
		else:
			return False
			
