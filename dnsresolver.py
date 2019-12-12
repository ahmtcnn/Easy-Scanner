# import dns.query
# import dns.zone

# z = dns.zone.from_xfr(dns.query.xfr('ahmetcankaraagacli.com', 'zonetransfer.me'))
# names = z.nodes.keys()
# for n in names:
#     print (z[n].to_text(n))


# import dns.resolver

# domain = 'bekchy.com'
# nameservers = dns.resolver.query(domain,'NS')
# for data in nameservers:
# 	print (data)

# import requests

# response = requests.get("https://nintechnet.com")
# for i in response.headers:
# 	print(i," : ",response.headers[i])
# print("\n")
# print(response.request.headers)

# import requests
# resp = requests.get("http://archive.org/wayback/available?url=bekchy.com")
# resp = resp.json()
# if resp['archived_snapshots'] == {}:
# 	print("no")
# print(resp)
# print(resp['archived_snapshots']['closest']['url'])

# API

# import requests
# import re
# resp = requests.get("https://api.viewdns.info/iphistory/?domain=bekchy.com&apikey=46f9c42a5590420ea7bfa3297f853c14fb46aa96&output=json")
# resp = resp.json()
# for record in resp['response']['records']:
# 	print(record['lastseen']+" --> " +record['ip'])

# from bs4 import BeautifulSoup

# def get_ip_history(url):

# 	headers 		= requests.utils.default_headers()
# 	user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
# 	headers['User-Agent'] = user_agent
# 	session = requests.session()
# 	resp = session.get("https://viewdns.info/iphistory/?domain="+"ahmetcankaradfasdf.com",headers=headers)

# 	if 'try again' in resp.text:
# 		print("no")
# 	soup = BeautifulSoup(resp.content, 'html.parser')
# 	tables = soup.find_all("table")
# 	tds = tables[3].find_all('td')
# 	control=1
# 	for i in tds[3::]:
# 		print(i.text, end=" - ")


# get_ip_history("ahmetcankaraagacli.com")

#headers = headers.update(user_agent)

#session.get("https://viewdns.info",headers=user_agent)

#print(resp.content)
# print(resp.headers)






#print(soup.prettify())


# print(tables[3])


import requests
from bs4 import BeautifulSoup


def get_whois(url):

	resp = requests.get("https://www.whois.com/whois/"+"sadasdfasfasdfasdff.com")
	print(resp)
	soup = BeautifulSoup(resp.content,'html.parser')
	raw_data = soup.find('pre',{'id':"registrarData",'class':'df-raw'})
	print(raw_data)
	print(raw_data.text)

get_whois("test")