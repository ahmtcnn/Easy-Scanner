import requests

class HeaderAnalysis():
	def __init__(self,url):
		self.url = url
		self.common_response_headers = []
		self.common_requests_headers = []

		self.response_headers = requests.get(url).headers
		self.request_headers = requests.get(url).request.headers
	def test_possible_vulnerabilities(self):
		pass

	def check_x_xss_protection(self):
		for header in self.response_headers:
			if "x-xss-protection" == header:
				if (self.response_headers[header]).startswith('1; mode=block') or (self.response_headers[header]).startswith('1;mode=block'):
					return True
		return False

	def check_x_frame_options(self):
		for header in self.response_headers:
			if "x-frame-options" == header.lower() and (self.response_headers[header]).lower() in ['deny', 'sameorigin'] :
				return True
		return False
	def check_x_content_type_options(self):
		for header in self.response_headers:
			if "x-content-type-options" == header.lower() and self.response_headers[header] == "nosniff":
				return True
		return False
	def check_strict_transport_security(self):
		for header in self.response_headers:
			if "strict-transport-security" == header.lower():
				return True
		return False
	def check_content_security_policy(self):
		for header in self.response_headers:
			if "content-security-policy" == header.lower():
				return True
		return False
	def check_x_content_security_policy(self):
		for header in self.response_headers:
			if "x-content-security-policy" == header.lower():
				return True
		return False

	def check_access_control_allow_origin(self):
		for header in self.response_headers:
			if "access_control_allow_origin" == header.lower():
				return True
		return False

	def check_x_download_options(self):
		for header in self.response_headers:
			if "x-download-options" == header.lower() and self.response_headers[header] == "noopen":
				return True
		return False	

	def check_cache_control(self):
		for header in self.response_headers:
			if "cache-control" == header.lower() and (self.response_headers[header].startswith('private') or self.response_headers[header].startswith('no-cache')):
				return True

		return False	
	def check_x_permitted_Cross_Domain_Policies(self):
		for header in self.response_headers:
			if "X-Permitted-Cross-Domain-Policies" == header.lower() and self.response_headers[header] == None or self.response_headers[header] == "master-only" :
				return True

		return False

	def check_uncommon_headers(self):
		lowercase = [item.lower() for item in self.common_response_headers]
		for header in self.response_headers:
			if not header in self.common_response_headers and not header in lowercase:
				print("uncommon header ! : ", header , " : ", self.response_headers[header])

	def read_header_files(self):
		with open("data/common_response_headers.txt") as fp:
			for line in fp:
				line = line.rstrip("\n")
				self.common_response_headers.append(line)
		with open("data/common_request_headers.txt") as fp:
			for line in fp:
				line = line.rstrip("\n")
				self.common_requests_headers.append(line)

#response.info().getheader('cache-control') and (response.info().getheader('cache-control').startswith('private') or response.info().getheader('cache-control').startswith('no-cache')):

h = HeaderAnalysis("https://nintechnet.com")
print(h.check_x_xss_protection())
print(h.check_x_frame_options())
print(h.check_x_content_type_options())
print(h.check_strict_transport_security())
print(h.check_content_security_policy())
print(h.check_x_content_security_policy())
print(h.check_access_control_allow_origin())
print(h.check_x_download_options())
print(h.check_cache_control())
print(h.check_x_permitted_Cross_Domain_Policies())
h.read_header_files()
h.check_uncommon_headers()