import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from queue import Queue
from urllib import parse
import re

##login olması durumu eklenecek
#stack overflow oluyor dolayısıyla sadece form içeriklerini alabiliriz.
class Crawler():
	def __init__(self,url):
		self.url = url
		self.internal_hrefs = []
		self.external_hrefs = []
		self.forms = set()
		self.forms_get = set()
		self.forms_post = set()
		self.reflections = set()
		self.uniq_actions = []

		self.base = self.base_url(url)
		self.internal_hrefs.append(self.url)

		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		self.headers 		= requests.utils.default_headers()
		self.headers['User-Agent'] = user_agent
		self.session = requests.session()

		print("BASE: "+ self.base)
		
		self.crawl()
		response = self.login()
		self.crawl()
		#self.login()
		# self.logout()
		# self.login()
		#self.crawl()
		#self.first_shot()

		#self.print_forms()
		#self.test_xss()
		#self.get_headers(self.url)
		self.print_hrefs()

	def logout(self):
		response = requests.get("http://127.0.0.1/logout.php")

	def login(self):
		response = self.session.get("http://127.0.0.1/login.php")
		soup = BeautifulSoup(response.content,features="html.parser")

		_token = soup.find("input",attrs={"name":"user_token"}).get("value")
		print(_token)
		user = {
			'username':'admin',
			'password':'password',
			'user_token':_token,
			'Login':'Login',
		}
		response = self.session.post("http://127.0.0.1/login.php",data=user,headers=self.headers)
		print(response.content)
		return response.content


	def reset_db(self,content):
		soup = BeautifulSoup(content,features="html.parser")
		post_forms = soup.findAll("form",attrs={"method":"post"})

		for form in post_forms:
			_token = soup.find("input",attrs={"name":"user_token"}).get("value")
			value = _token = soup.find("input",attrs={"name":"create_db"}).get("value")
			reset_dbs = {
			'user_token':_token,
			'create_db':value,
			}

		response = self.session.post("http://127.0.0.1/setup.php",data=reset_dbs,headers=self.headers)
		#print(response.content)
		time.sleep(5)
		#print("sleeped")
		#print(response.content)

# <form action="#" method="post">
# 	<input name="create_db" type="submit" value="Create / Reset Database">
# 	<input type='hidden' name='user_token' value='62cc1b1c4c81ef6d1f12cc6150ee5ea3' />
# </form>	



	def crawl(self):

		for url in self.internal_hrefs:
			try:
				response = self.session.get(url,headers=self.headers)
			except:
				return
			soup = BeautifulSoup(response.content,features="html.parser",from_encoding="iso-8859-1")

			links = soup.find_all("a")
			#print(links)
			for link in links:
				try:
					if link["href"]:
						mylink = link["href"]
						# print(mylink)
						if "#" in mylink:
							mylink = mylink.split("#")[0]
						#print(mylink)
						url = parse.urljoin(self.base,mylink)
						if self.check_existence(url):
							if self.base in url:
								self.internal_hrefs.append(url)
								self.get_forms(url)
								#print(url)
							else:
								self.external_hrefs.append(url)
				except:
					pass

	def test_xss(self):
		TEST_WORD = 'thisissometest'
		for form in self.forms_post:
			data_dict = {}
			url, form = form
			inputs = form.find_all("input")
			text_areas = form.find_all('textarea')

			action = form.get('action')


			for input in inputs:
				input_name=input.get('name')
				input_type=input.get('type')
				input_value=input.get('value')
				if input_type == "text":
					input_value = TEST_WORD
				data_dict[input_name] = input_value

			if text_areas:
				for area in text_areas:
					textarea_name = area.get('name')
					textarea_value = TEST_WORD
					data_dict[textarea_name] = textarea_value

			if action == "" or action == '#':
				target = url
			else:
				target = parse.urljoin(self.base,action)
			#print(target)
			response = self.session.post(target,data=data_dict,headers=self.headers)
			print(target,response.content,"\n\n")
			if re.search(TEST_WORD,response.text,re.IGNORECASE):
				if target not in self.uniq_actions:
					self.uniq_actions.append(target)
					self.reflections.add((form,target))
				#rint("reflected at"+url +" -> "+target)
			else:
				pass
				# print(form,data_dict,target)
				# print("**************************************\n\n")
				#print(url)
				#print(response.text)
		for i in self.reflections:
			print(i)

	def check_existence(self,url):
		if url in self.internal_hrefs:
			return False
		else:
			return True


	def base_url(self,url):
		parsed = urlparse(url)
		return parsed.scheme+"://"+parsed.netloc

	def print_hrefs(self):
		for i in self.internal_hrefs:
			print(i)

	def print_forms(self):
		print("POST FORMS")
		for i in self.forms_post:
			print(i)


	def get_headers(self,url):
		response = requests.get(url)
		for key in response.headers:
			print(key + " : " +response.headers[key])

		print("************** RESPONSE *****************")

		for key in response.request.headers:
			print(key + " : " +response.request.headers[key])

	def get_forms(self,url):
		response = requests.get(url)
		soup = BeautifulSoup(response.content,features="lxml")
		post_forms = soup.findAll("form",attrs={"method":"post"})
		get_forms = soup.findAll("form",attrs={"method":"get"})

		for form in post_forms:
			self.forms_post.add((url,form))
			
		for form in get_forms:
			self.forms_get.add((url,form,action))

	def is_redirection(self,href):
		http_start_position = re.search(self.url,href)


		if http_start_position:
			return http_start_position.start() == 0
		else:
			return False
			


	#thread ile formlar alınacak



		




craw = Crawler("http://127.0.0.1/")
