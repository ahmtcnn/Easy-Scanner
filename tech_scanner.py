from builtwith import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *




class TechScanner():
	def __init__(self,url):
		self.url = url
		self.response = ""
		self.counter = 0
		print(url)
		self.run()


	def run(self):
		self.response = builtwith(self.url)
		print(self.response)





scanner = TechScanner("https://bekchy.com")
#https://www.ostraining.com/blog/wordpress/site-built-in-wordpress/