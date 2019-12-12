import requests
import re


# data = {'1': 'a', '2': 'b'}
# r = requests.options('http://bekchy.com',data=data)
# for i in r.headers:
# 	print(i,r.headers[i])
working_methods = set()

def find_http_method_with_options(url):
	print("Testing http methods with option header..")
	#resp = requests.request(method='OPTIONS', url="https://ahmetcankaraagacli.com")

	test_url(url)

def test_url(url):
	try:
		resp = requests.options(url)
		for i in resp.headers:
			if i == "Allow":
				print(i,resp.headers[i])
				allows = resp.headers[i].split(",")
				for j in allows:
					working_methods.add(j)
	except:
		pass




def find_http_method_with_trying(url):
	print("Testing http method manually for given url")
	methods = ['GET','POST','PUT','DELETE','OPTIONS','HEAD','CONNECT','TRACE','PATCH']
	for method in methods:
		response = requests.request(method=method,url=url)
		#if response.status_code != 405:
		print(method, response.status_code)
		working_methods.add(method)


	


# find_http_method_with_trying("https://bekchy.com")
# find_http_method_with_options("https://bekchy.com")

# print(working_methods)

# response = requests.post("https://dashboard.bekchy.com/")
# print(response.status_code)
# print(resp.headers

import http.client as httplib

conn = httplib.HTTPConnection('http://dashboard.bekchy.com')
conn.request('OPTIONS', '/')
response = conn.getresponse()
print (response.getheader('allow'))