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
		self.internal_hrefs = set()
		self.external_hrefs = set()
		self.forms = set()
		self.forms_get = []
		self.forms_post = []
		self.base = self.base_url(url)
		print("BASE: "+ self.base)
		self.start_crawler(self.url)
		self.get_headers(self.url)


	def start_crawler(self,url):
		hrefs = self.extract_links(url)
		for href in hrefs:
			if self.base in href and not href in self.internal_hrefs:
				if self.is_redirection(href):
					self.internal_hrefs.add(href)
					print(href)
					self.start_crawler(href)
			elif not self.base in href and not href in self.external_hrefs:
				self.external_hrefs.add(href)


	def extract_links(self,url):
		hrefs = []
		try:
			response = requests.get(url,timeout=(3,4))
		except:
			return hrefs
		parsed_html = BeautifulSoup(response.content,features="lxml")

		links = parsed_html.findAll(href=True)
		for link in links:
			if link["href"]:
				mylink = link["href"]
				if "#" in mylink:
					mylink = mylink.split("#")[0]
				hrefs.append(parse.urljoin(url,mylink))
		return hrefs


	def base_url(self,url):
		parsed = urlparse(url)
		return parsed.netloc

	def print_hrefs(self):
		for i in self.internal_hrefs:
			print(i)


	def get_headers(self,url):
		response = requests.get(url)
		for key in response.headers:
			print(key + " : " +response.headers[key])

		print("************** RESPONSE *****************")

		for key in response.request.headers:
			print(key + " : " +response.request.headers[key])

	def get_forms(self,url,content):
		post_forms = content.findAll("form",attrs={"method":"post"})
		get_forms = content.findAll("form",attrs={"method":"get"})

		for form in post_forms:
			self.forms_post.append((url,form))
		for form in get_forms:
			self.forms_get.append((url,form))

	def is_redirection(self,href):
		http_start_position = re.search(self.url,href)


		if http_start_position:
			return http_start_position.start() == 0
		else:
			return False
			


	#thread ile formlar alınacak



		




craw = Crawler("https://www.bekchy.com")
