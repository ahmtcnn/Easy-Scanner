import requests
import dns.resolver
import re
from statistics import mode
from urllib.parse import urlparse,urljoin


class WafAnalysis():
	def __init__(self,url):
		self.url = url
		parser = urlparse(url)
		self.url_without_schema = parser.netloc
		self.waf_list = []
		self.waf_list_asString = ""
		self.guess = []
		self.read_file()
		self.header_analysis_for_waf()
		self.response_analyasis_for_waf()
		self.name_server_analysis_for_waf()


	def return_result(self):
		return mode(self.guess)

	def name_server_analysis_for_waf(self):
		try:
			nameservers = dns.resolver.query(self.url_without_schema,'NS')
			
			for data in nameservers:
				try:
					test = re.search(self.waf_list_asString,str(data),re.IGNORECASE)
					if test:
						self.guess.append((test.group(0)))
						#print(test.group(0),"*")
				except:
					pass
					#print("exeption2")
		except:
			print("excepptt")


	def header_analysis_for_waf(self):
		response = requests.get(self.url)
		self.check_headers(response.headers)
		self.check_headers(response.request.headers)

	def check_headers(self,headers):
		for header in headers:
			#print(header," : ",headers[header])
			try:
				#re.search(header,self.waf_list_asString,re.IGNORECASE) or re.search(headers[header],self.waf_list_asString,re.IGNORECASE) or
				test = re.search(self.waf_list_asString,header,re.IGNORECASE) or re.search(self.waf_list_asString,headers[header],re.IGNORECASE)
				if test:
					self.guess.append((test.group(0)))
					#print(test.group(0))
			except:
				pass


	def read_file(self):
		with open("data/wafs.dat","r+") as fp:
			for line in fp:
				line = line.rstrip("\n")
				self.waf_list.append(line)
		self.waf_list_asString = "|".join(self.waf_list)
		#print(self.waf_list_asString)

	def response_analyasis_for_waf(self):
		response = requests.get(self.url,params={"test":"<script>alert(1);</script>"})
		#print(response.content)
		try:
			test = re.search(self.waf_list_asString,response.content,re.IGNORECASE) or re.search(response.content,self.waf_list_asString,re.IGNORECASE)
			if test:
				#print(test.group(0),"waf guess")
				self.guess.append(test.group(0))
		except:
			pass
			#print("exception")



# wafs = WafAnalysis("https://bekchy.com")
# print(mode(wafs.guess))
#search sonucu 4 ten buyuk olanlari cekcez

#print(re.search("aeSecure|Airlock|Alert Logic|AliYunDun|Anquanbao|AnYu|Approach|Armor Defense|ASP.NET Generic Protection|Astra Web Protection|AWS Elastic Load Balancer|Yunjiasu|Barikode (Ethic Ninja)|Barracuda Application Firewall|Bekchy|BinarySec|BitNinja|BlockDoS|Bluedon|CacheWall|CdnNS|WP Cerber Security|ChinaCache CDN Load Balancer|Chuang Yu Shield|ACE XML Gateway|Cloudbric|Cloudflare|Cloudfront|Comodo cWatch|CrawlProtect (Jean-Denis Brun)|DenyALL (Rohde & Schwarz CyberSecurity)|Distil (Distil Networks)|DOSarrest (DOSarrest Internet Security)|DotDefender (Applicure Technologies)|DynamicWeb Injection Check (DynamicWeb)|Edgecast (Verizon Digital Media)|Expression Engine (EllisLab)|BIG-IP Access Policy Manager (F5 Networks)|BIG-IP Application Security Manager (F5 Networks)|BIG-IP Local Traffic Manager (F5 Networks)|FirePass (F5 Networks)|Trafficshield (F5 Networks)|FortiWeb (Fortinet)|GoDaddy Website Protection (GoDaddy)|Greywizard (Grey Wizard)|HyperGuard (Art of Defense)|DataPower (IBM)|Imunify360 (CloudLinux)|Incapsula (Imperva Inc.)|Instart DX (Instart Logic)|ISA Server (Microsoft)|Janusec Application Gateway (Janusec)|Jiasule (Jiasule)|KS-WAF (KnownSec)|Kona Site Defender (Akamai)|LiteSpeed Firewall (LiteSpeed Technologies)|Malcare (Inactiv)|Mission Control Application Shield (Mission Control)|ModSecurity (SpiderLabs)|NAXSI (NBS Systems)|Nemesida (PentestIt)|NetContinuum (Barracuda Networks)|NetScaler AppFirewall (Citrix Systems)|NevisProxy (AdNovum)|Newdefend (NewDefend)|NexusGuard Firewall (NexusGuard)|NinjaFirewall (NinTechNet)|NSFocus (NSFocus Global Inc.)|OnMessage Shield (BlackBaud)|Open-Resty Lua Nginx WAF|Palo Alto Next Gen Firewall (Palo Alto Networks)|PerimeterX (PerimeterX)|pkSecurity Intrusion Detection System|PowerCDN (PowerCDN)|Profense (ArmorLogic)|AppWall (Radware)|Reblaze (Reblaze)|RSFirewall (RSJoomla!)|ASP.NET RequestValidationMode (Microsoft)|Sabre Firewall (Sabre)|Safe3 Web Firewall (Safe3)|Safedog (SafeDog)|Safeline (Chaitin Tech.)|SecuPress WordPress Security (SecuPress)|Secure Entry (United Security Providers)|eEye SecureIIS (BeyondTrust)|SecureSphere (Imperva Inc.)|SEnginx (Neusoft)|Shield Security (One Dollar Plugin)|SiteGround (SiteGround)|SiteGuard (Sakura Inc.)|Sitelock (TrueShield)|SonicWall (Dell)|UTM Web Protection (Sophos)|Squarespace (Squarespace)|StackPath (StackPath)|Sucuri|Tencent Cloud Firewall (Tencent Technologies)|Teros (Citrix Systems)|TransIP Web Firewall (TransIP)|URLMaster SecurityCheck (iFinity/DotNetNuke)|URLScan (Microsoft)|Varnish (OWASP)|VirusDie (VirusDie LLC)|Wallarm (Wallarm Inc.)|WatchGuard (WatchGuard Technologies)|WebARX (WebARX Security Solutions)|WebKnight (AQTRONIX)|WebSEAL (IBM)|WebTotem (WebTotem)|West263 Content Delivery Network|Wordfence (Feedjit)|WTS-WAF (WTS)|360WangZhanBao (360 Technologies)|XLabs Security WAF (XLabs)|Xuanwudun |Yundun (Yundun)|Yunsuo (Yunsuo)|Zenedge (Zenedge)|ZScaler (Accenture)","X-Sucuri-Cache",re.IGNORECASE))
#print(wafs.waf_list_asString)