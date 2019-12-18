from helpers.worker_signals import WorkerSignals
from PyQt5.QtCore import QRunnable,pyqtSlot
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib import parse
from urllib import parse
import requests
import asyncio
import time
import re


REGEX_FOR_LOGOUT = ".*(logout).*"

#internal hrefs before and after login


class Crawler(QRunnable):
	def __init__(self,url,login_form,quiet=False,form_scan=True):
		"""Setting variables in Constructor"""

		super(Crawler,self).__init__()
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
		"""Running modules when starts"""
		start_time = time.time()

		self.preperation()
		self.crawl()
		self.get_forms_from_list()

		finish_time = time.time()
		difference = finish_time - start_time
		self.signals.finish_control.emit()
		self.signals.info_box.emit("[✔] Crawler Finished!")
		self.signals.info_box.emit("Time Taken: "+str(difference))



	def return_results(self):
		"""Returns all findings for other scanners"""
		return (self.internal_hrefs , self.forms_get, self.forms_post, self.session)


	def preperation(self):
		"""Setting session object attiributes"""
		print("BASE: "+ self.base)
		self.internal_hrefs.append(self.url)
		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		self.headers = requests.utils.default_headers()
		self.headers['User-Agent'] = user_agent
		self.session = requests.session()


	def login(self):
		"""Login option to crawl other pages that require login"""

		action 					= self.login_form['action']
		form_url 				= self.login_form['url']

		response = self.session.get(form_url,headers=self.headers)
		soup = BeautifulSoup(response.content,features="html.parser",from_encoding="iso-8859-1")#,from_encoding="iso-8859-1"
		forms = soup.findAll("form",attrs={"method":re.compile("POST", re.IGNORECASE)})

		form = self.find_login_form(forms)
		if form == None:
			print("Couldn't find the stated login form!")
			return

		form_dictionary = self.create_login_form(form)

		try:
			response = self.session.post(action,data=form_dictionary,headers=self.headers)

		except Exception as e:
			print("Error while login: ",e)

	def find_login_form(self,forms):
		"""Finding login form depending on action attiribute"""

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
		return None

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



	def crawl(self):
	"""Crawling links in website"""

		if self.login_form != None:
			self.login()
		
		for url in self.internal_hrefs:
			try:
				response = self.session.get(url,headers=self.headers)
			except:
				return
			soup = BeautifulSoup(response.content,features="html.parser",from_encoding="iso-8859-1")
			self.parse_and_get_links(soup,url)


	def parse_and_get_links(self,soup,url):
	"""Parsing response and getting all internal-external hrefs"""

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
							else:
								self.external_hrefs.append(url)
				except:
					pass
			for img in imgs:
				self.srcs.add(img['src'])


	def check_existence(self,url):
	"""Helper function that checks if an url exist in internal href"""
		if url in self.internal_hrefs:
			return False
		else:
			return True

	@property
	def base_url(self):
	"""Returns base url e.g (http://example.com)"""
		parsed = urlparse(self.url)
		return parsed.scheme+"://"+parsed.netloc

	"""These are for Debug Purpose"""
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
		"""Crawling header values"""
		response = self.session.get(url,headers=self.headers)
		for key in response.headers:
			print(key + " : " +response.headers[key])

		for key in response.request.headers:
			print(key + " : " +response.request.headers[key])


	def get_forms_from_list(self):
		"""Getting forms from detected links"""
		if self.login_form != None:
			self.login()
		
		for url in self.internal_hrefs:
			if not re.search(REGEX_FOR_LOGOUT,url):
				self.get_forms(url)
			else:
				print("test ",url)

			


	def get_forms(self,url):
		"""Helper function to get forms"""
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















	# def create_form(self,form):
	# 		url, form 		= _form
	# 		#print(form)
	# 		inputs 			= form.find_all("input")
	# 		text_areas 		= form.find_all('textarea')
	# 		action 			= form.get('action')
	# 		form_dictionary = {}
	# 		target			= ""	

	# 		for input in inputs:
	# 			input_name 		= input.get('name')
	# 			input_type		= input.get('type')
	# 			input_value 	= input.get('value')

	# 			if input_type == "text": input_value = test_word

	# 			form_dictionary[input_name] = input_value

	# 		if text_areas:
	# 			for area in text_areas:
	# 				textarea_name 			 = area.get('name')
	# 				textarea_value 			 = test_word
	# 				form_dictionary[textarea_name] = textarea_value

	# 		if action == "" or action == '#':
	# 			target = url
	# 		else:
	# 			target = parse.urljoin(self.base,action)

	# 		return url ,form_dictionary, target, form