import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from queue import Queue
from urllib import parse
import re
from crawler import Crawler

##login olması durumu sonra eklenecek


NORMAL		 = "thisissometest"
XSS_PAYLOAD  = "<script>alert(1)</script>"
XSS_PAYLOAD_REGEX  = r"<script>alert\(1\)</script>"

# her seferinde get ile url yi alıp öyle post atmak gerek kontrol et

class XssScanner():
	def __init__(self,url,href_list,get_forms,post_forms,session):
		#self.session = session
		self.url 			 = url
		self.base 			 = self.base_url(url)
		self.forms_get 		 = get_forms
		self.forms_post 	 = post_forms
		self.reflections 	 = set()
		self.possible_filter = set()
		self.possible_xss 	 = []
		self.uniq_actions 	 = []
		self.preperation()

		self.login()
		# self.crawler = Crawler(url)
		# self.href_list, self.get_forms, self.post_forms 	= self.crawler.return_results()
		
		self.test_reflections()
		self.test_xss()
		#self.print_hrefs()





	def preperation(self):
		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		self.headers 		= requests.utils.default_headers()
		self.headers['User-Agent'] = user_agent
		self.session = requests.session()


	def login(self):
		response = self.session.get("http://testphp.vulnweb.com/login.php")
		# soup = BeautifulSoup(response.content,features="html.parser")

		# _token = soup.find("input",attrs={"name":"user_token"}).get("value")
		# print(_token)
		user = {
			'uname':'test',
			'pass':'test',
			#'Login':'Login',
		}
		response = self.session.post("http://testphp.vulnweb.com/userinfo.php",data=user,headers=self.headers)
		#print(response.content)
		


	def create_form(self,_form,test_word):
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

			
	def test_reflections(self):

		#response = self.session.get("http://192.168.1.106")
		#print("get",response.content)
		for form in self.forms_post:

			url, form_dictionary, target, _form = self.create_form(form,NORMAL)
			#print("target",target)
			#print(form_dictionary)

			response = self.session.post(target,data=form_dictionary,headers=self.headers)
			#print(target)
			#print(response.content)
			#print(response.content)
			if re.search(NORMAL,response.text,re.IGNORECASE):

				if target not in self.uniq_actions:
					self.uniq_actions.append(target)
					self.reflections.add((url, _form))
					print("Reflected -> ",target)
			else:
				pass

		for form in self.forms_get:
			#print(form)
			url, form_dictionary, target, _form = self.create_form(form,NORMAL)
			#print(target)

			response = self.session.get(target,params=form_dictionary,headers=self.headers)
			#print(response.content)
			if re.search(NORMAL,response.text,re.IGNORECASE):

				if target not in self.uniq_actions:
					self.uniq_actions.append(target)
					self.reflections.add((url, _form))
					print("Reflected -> ",target)
			else:
				pass

		print("reflection scan finished")

	def test_xss(self):
		for form in self.reflections:
			url, form_dictionary, target, form = self.create_form(form,XSS_PAYLOAD)
			response = self.session.post(target,data=form_dictionary,headers=self.headers)
			#print(response.content)

			if re.search(XSS_PAYLOAD_REGEX,response.text,re.IGNORECASE):
				#self.reflections.add((url,form,target))
				print("Possible XSS -> ",target)
			else:
				pass
			
		print("xss scan finished")


	# def test_xss(self):
	# 	for form,target in self.reflections:
	# 		data_dict = {}

	# 		TEST_WORD = "<script><alert(1)</script>"

	# 		inputs = form.find_all("input")
	# 		text_areas = form.find_all('textarea')


	# 		for input in inputs:
	# 			input_name=input.get('name')
	# 			input_type=input.get('type')
	# 			input_value=input.get('value')
	# 			if input_type == "text":
	# 				input_value = TEST_WORD
	# 			data_dict[input_name] = input_value

	# 		if text_areas:
	# 			for area in text_areas:
	# 				textarea_name = area.get('name')
	# 				textarea_value = TEST_WORD
	# 				data_dict[textarea_name] = textarea_value


	# 		response = self.session.post(target,data=data_dict,headers=self.headers)

	# 		if re.search(TEST_WORD,response.text,re.IGNORECASE):
	# 				self.possible_xss.append((form,target))
	# 		else:
	# 			self.possible_filter.add((form,target))

	# 	for form,target in self.possible_xss:
	# 		print("possible xss -> ",form,target)




	def base_url(self,url):
		parsed = urlparse(url)
		return parsed.scheme+"://"+parsed.netloc



	# def print_forms(self):
	# 	print("POST FORMS")
	# 	for i in self.forms_post:
	# 		print(i)


	# def get_headers(self,url):
	# 	response = requests.get(url)
	# 	for key in response.headers:
	# 		print(key + " : " +response.headers[key])

	# 	print("************** RESPONSE *****************")

	# 	for key in response.request.headers:
	# 		print(key + " : " +response.request.headers[key])

	# def get_forms(self):
	# 	for url in self.internal_hrefs:

	# 		response = requests.get(url)
	# 		soup = BeautifulSoup(response.content,features="lxml")
	# 		post_forms = soup.findAll("form",attrs={"method":"post"})
	# 		get_forms = soup.findAll("form",attrs={"method":"get"})

	# 		for form in post_forms:
	# 			self.forms_post.add((url,form))
				
	# 		for form in get_forms:
	# 			self.forms_get.add((url,form,action))

	# def is_redirection(self,href):
	# 	http_start_position = re.search(self.url,href)


	# 	if http_start_position:
	# 		return http_start_position.start() == 0
	# 	else:
	# 		return False
			


	#thread ile formlar alınacak



		



crawler 	= Crawler("http://testphp.vulnweb.com/")
href_list,get_forms, post_forms, session	= crawler.return_results()

scanner 	= XssScanner("http://testphp.vulnweb.com/", href_list,get_forms,post_forms,session)




























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
