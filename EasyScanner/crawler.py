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
		self.forms_get = set()
		self.forms_post = set()
		self.form_urls = set() # Buradan devam et
		self.srcs = set()
		self.base = self.base_url
		print("BASE: "+ self.base)
		self.preperation()
		#self.crawl()
		self.login()
		self.crawl()
		print("crawling finished")
		#self.print_hrefs()
		#self.print_post_forms()
		#self.print_get_forms()

	def return_results(self):
		return self.internal_hrefs , self.forms_get, self.forms_post, self.session #


	def preperation(self):
		self.internal_hrefs.append(self.url)
		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		self.headers 		= requests.utils.default_headers()
		self.headers['User-Agent'] = user_agent
		self.session = requests.session()


	#login bilgileri verilecek
	def login(self):
		response = self.session.get("http://testphp.vulnweb.com/login.php")
		user = {
			'uname':'test',
			'pass':'test',
			#'Login':'Login'

		}
		response = self.session.post("http://testphp.vulnweb.com/userinfo.php",data=user,headers=self.headers)
		#print(response.content)
		
	def crawl(self):
		print("crawler started")
		for url in self.internal_hrefs:
			try:
				response = self.session.get(url,headers=self.headers)
			except:
				return
			soup = BeautifulSoup(response.content,features="html.parser",from_encoding="iso-8859-1")

			links = soup.find_all("a")
			imgs = soup.find_all('img')
			#print(links)
			for link in links:
				try:
					if link["href"]:
						mylink = link["href"]
						# print(mylink)
						if "#" in mylink:
							mylink = mylink.split("#")[0]
						url = parse.urljoin(self.base,mylink)
						#print(url)
						if self.check_existence(url):
							if self.base in url:
								self.internal_hrefs.append(url)
								#print(url)
								#print(response.content)
								self.get_forms(url)
								#print(url)
							else:
								self.external_hrefs.append(url)
				except:
					pass
			for img in imgs:
				self.srcs.add(img['src'])
		print("crawl finished")
			

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
		response = requests.get(url)
		for key in response.headers:
			print(key + " : " +response.headers[key])

		print("************** RESPONSE *****************")

		for key in response.request.headers:
			print(key + " : " +response.request.headers[key])

	def get_forms(self,url):
		response = self.session.get(url)

		soup = BeautifulSoup(response.content,features="html.parser")
		post_forms = soup.findAll("form",attrs={"method":"post"})
		get_forms = soup.findAll("form",attrs={"method":"get"})
		

		for form in post_forms:
			#print(url,"****",form)
			#print("\n\n")
			self.forms_post.add((url,form))
			
		for form in get_forms:
			#print(form)
			self.forms_get.add((url,form))

		post_forms = soup.findAll("form",attrs={"method":"POST"})
		get_forms = soup.findAll("form",attrs={"method":"GET"})
		

		for form in post_forms:
			self.forms_post.add((url,form))
			
		for form in get_forms:
			#print(form)
			self.forms_get.add((url,form))



	def is_redirection(self,href):
		http_start_position = re.search(self.url,href)


		if http_start_position:
			return http_start_position.start() == 0
		else:
			return False
			


	#thread ile formlar alınacak



		




# craw = Crawler("http://testphp.vulnweb.com/")
