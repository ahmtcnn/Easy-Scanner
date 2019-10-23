import requests
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
from queue import Queue


class Crawler():
	def __init__(self,url):
		self.url = url
		self.internal_hrefs = set()
		self.external_hrefs = set()
		self.forms = set()
		self.base = self.base_url(url)
		print("BASE: "+ self.base)
		#self.start_crawler(self.url)
		self.get_headers(self.url)


	def start_crawler(self,url):
		hrefs = self.extract_links(url)
		#print(hrefs)
		for href in hrefs:
			print(href)
			if self.base in href and not href in self.internal_hrefs:
				self.internal_hrefs.add(href)
				self.start_crawler(href)
			elif not self.base in href and not href in self.external_hrefs:
				self.external_hrefs.add(href)


	def extract_links(self,url):
		hrefs = []
		try:
			response = requests.get(url,timeout=(3,4))
		except:
			return hrefs
		parsed_html = BeautifulSoup(response.content)
		links = parsed_html.findAll(href=True)
		for link in links:
			if link["href"]:
				mylink = link["href"]
				if "#" in mylink:
					mylink = mylink.split("#")[0]
				hrefs.append(mylink)
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

craw = Crawler("https://ahmetcankaraagacli.com")
