import requests
import re
from queue import Queue
import threading
import random
import time
from proxy_scanner import ProxyScanner
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from urllib.parse import urlparse,urljoin


import asyncio
import time
import aiohttp


async def download_site(session, url,signal):
	try:
		async with session.get(url) as response:
			if response.status == 200:# and url in response.url: 
				print("URL: {0}\t\t\t Status {1}".format(url, response.status))
				signal.emit("URL: {0}\t\t\t Status {1}".format(url, response.status))
				return url
	except Exception as s:
		print(s)


async def download_all_sites(sites,signal):
	async with aiohttp.ClientSession() as session:
		tasks = []
		for url in list(sites):
			urli = url[0]
			#	print(urli)
			task = asyncio.ensure_future(download_site(session, urli,signal))
			#print(str(next(sites)))
			tasks.append(task)
		await asyncio.gather(*tasks)



class WorkerSignals(QObject):

	result_list   = pyqtSignal(str)
	finish_control = pyqtSignal()
	info_box = pyqtSignal(str)

class DirScanner(QRunnable):
	def __init__(self,target):
		super(DirScanner,self).__init__()
		self.target = target
		self.signals = WorkerSignals()
		# info liste -> using a... wordlist file diye eklenecek
		self.sites =   ([urljoin(target,line.rstrip("\n"))] for line in open("data/directories.dat"))

		
	@pyqtSlot()
	def run(self):
		print(self.sites)
		start_time = time.time()
		loop = asyncio.new_event_loop()
		result = loop.run_until_complete(download_all_sites(self.sites,self.signals.result_list))
		finish_time = time.time()
		difference = finish_time - start_time
		self.signals.info_box.emit("Time Taken " + str(difference) + '')

		print(result)
		self.signals.info_box.emit("[✔] Directory Scan Finished")
		self.signals.finish_control.emit()



# if __name__ == "__main__":
# 	url = "http://ahmetcankaraagacli.com/"
# 	sites =   ([url+line.rstrip("\n")] for line in open("data/directories.dat"))
# 	start_time = time.time()

# 	loop = asyncio.get_event_loop()
# 	loop.run_until_complete(download_all_sites(sites))
# 	duration = time.time() - start_time
# 	leng = len(list(sites))
# 	print(f"Tested dirs in {duration} seconds")