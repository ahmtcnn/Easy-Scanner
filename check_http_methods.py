import requests
import re


# data = {'1': 'a', '2': 'b'}
# r = requests.options('http://bekchy.com',data=data)
# for i in r.headers:
# 	print(i,r.headers[i])

resp = requests.request(method='OPTIONS', url="https://www.medium.com")
for i in resp.headers:
	print(i,resp.headers[i])
# print(resp.headers