# import requests
# from bs4 import BeautifulSoup



# session = requests.session()
# response = session.get("https://dashboard.bekchy.com/login")
# source = BeautifulSoup(response.content,"lxml")
# _token = source.find("input",attrs={"name":"_token"}).get("value")

# user_info = {'email':'ahmetcankaraagacli@hotmail.com','password':'Tarih?1997','_token':_token}


# response2 = session.post("https://dashboard.bekchy.com/login",data=user_info)

# print(response2)
# # session = requests.session()
# # response3 = session.get("https://dashboard.bekchy.com/my-websites")
# # print(response3.content)



# # print(response.status_code)
# # # for i in response.headers:
# # # 	print(i,":",response.headers[i])

# # print(response2.request.headers)

# # for i in response2.request.headers
# import socket
# ip = socket.gethostbyname("bekchy.com")
# print(ip)
#!/usr/bin/env python

# import asyncio
# import websockets
# import socket

# async def check_port(target,port):
#     conn = asyncio.open_connection(target, port)
#     try:
#         reader, writer = await asyncio.wait_for(conn, timeout=3)
#         print(target)
#     except:
#         print("exception")
#     finally:
#         if 'writer' in locals():
#             writer.close()

# asyncio.get_event_loop().run_until_complete(check_port('art.instra.com','443'))
# from selenium import webdriver

# driver = webdriver.Firefox()
# driver.get("http://example.com")
# button = driver.find_element_by_id('buttonID')
# button.click()

 #!/usr/bin/python 

# import asyncio


# @asyncio.coroutine
# def ping(loop, target, dump=False):
#     create =  asyncio.create_subprocess_exec('ping', '-c', '10', target,
#                                           stdout=asyncio.subprocess.PIPE)
#     proc = yield from create
#     lines = []
#     while True:
#         line = yield from proc.stdout.readline()
#         if line == b'':
#             break
#         l = line.decode('utf8').rstrip()
#         if dump:
#             print(l)
#         lines.append(l)
#     transmited, received = [int(a.split(' ')[0]) for a
#                             in lines[-2].split(', ')[:2]]
#     stats, unit = lines[-1].split(' = ')[-1].split(' ')
#     min_, avg, max_, stddev = [float(a) for a in stats.split('/')]
#     return transmited, received, unit, min_, avg, max_, stddev


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     ping = loop.run_until_complete(ping(loop, 'free.fr'))
#     print(ping)

#     loop.close()

# from aio_ping import ping

# from aio_ping import Ping,VerbosePing


# async def ping(hostname, verbose=True, handle_signals=False, **kw):
#     """
#     Send @count ping to @hostname with the given @timeout
#     """
#     ping = (VerbosePing if verbose else Ping)(verbose=verbose, **kw)
#     if handle_signals: ping.add_signal_handler()
#     await ping.init(hostname)
#     res = await ping.looped()
#     if verbose:
#         ping.print_stats()
#     ping.close()
#     return res

# import re
# if 10 > 5: print("okey")

# string = r"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\r\n<html>\r\n<head>\r\n<title>add new user</title>\r\n<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">\r\n<link href="style.css" rel="stylesheet" type="text/css">\r\n</head>\r\n<body>\r\n<div id="masthead"> \r\n  <h1 id="siteName">ACUNETIX ART</h1> \r\n</div>\r\n<div id="content">\r\n\t<p>You have been introduced to our database with the above informations:</p><ul><li>Username: <script>alert(1)</script> </li><li>Password: </li><li>Name: <script>alert(1)</script></li><li>Address: <script>alert(1)</script></li><li>E-Mail: <script>alert(1)</script></li><li>Phone number: <script>alert(1)</script></li><li>Credit card: <script>alert(1)</script></li></ul><p>Now you can login from <a href=\'http://testphp.vulnweb.com/login.php\'>here.</p></div>\r\n</body>\r\n</html>\r\n"""


# XSS_PAYLOAD = "aeSecure|Airlock|Alert Logic|AliYunDun|Anquanbao|AnYu|Approach|Armor Defense|ASP.NET|Astra|AWS|Yunjiasu|Barikode|Barracuda|Bekchy|BinarySec|BitNinja|BlockDoS|Bluedon|CacheWall|CdnNS|WP Cerber Security|ChinaCache CDN Load Balancer|Chuang Yu Shield|ACE XML Gateway|Cloudbric|Cloudflare|Cloudfront|Comodo cWatch|CrawlProtect|DenyALL|Distil|DOSarrest|DotDefender|DynamicWeb|Edgecast|ExpressionEngine|EllisLab|BIG-IP|FirePass|Trafficshield|F5|FortiWeb|GoDaddy|Greywizard|HyperGuard|DataPower|Imunify360|Incapsula|Instart|ISA|Janusec|Jiasule|KS-WAF|Akamai|LiteSpeed|Malcare|Mission|ModSecurity|NAXSI|Nemesida|NetContinuum|NetScaler|NevisProxy|Newdefend|NexusGuard|NinjaFirewall|NSFocus|OnMessage|Open-Resty|Palo Alto|PerimeterX|pkSecurity|PowerCDN|Profense|AppWall|Reblaze|RSFirewall|Sabre|Safe3|Safedog|Safeline|SecuPress|Secure Entry|eEye SecureIIS|SecureSphere|SEngin|Shield Security|SiteGround|SiteGuard|Sitelock|SonicWall|UTM|Sophos|Squarespace|StackPath|Sucuri|Tencent|Teros|TransIP|URLMaster|URLScan|Varnish|VirusDie|Wallarm|WatchGuard|WebARX|WebKnight|WebSEAL|WebTotem|West263|Wordfence|WTS-WAF|360WangZhanBao|XLabs|Xuanwudun |Yundun|Yunsuo|Zenedge|ZScaler"

# if re.search(XSS_PAYLOAD,"ns1.bekchydns.com.",re.IGNORECASE):
#     test = re.search("aeSecure|Airlock|Alert Logic|AliYunDun|Anquanbao|AnYu|Approach|Armor Defense|ASP.NET|Astra|AWS|Yunjiasu|Barikode|Barracuda|Bekchy|BinarySec|BitNinja|BlockDoS|Bluedon|CacheWall|CdnNS|WP Cerber Security|ChinaCache CDN Load Balancer|Chuang Yu Shield|ACE XML Gateway|Cloudbric|Cloudflare|Cloudfront|Comodo cWatch|CrawlProtect|DenyALL|Distil|DOSarrest|DotDefender|DynamicWeb|Edgecast|ExpressionEngine|EllisLab|BIG-IP|FirePass|Trafficshield|F5|FortiWeb|GoDaddy|Greywizard|HyperGuard|DataPower|Imunify360|Incapsula|Instart|ISA|Janusec|Jiasule|KS-WAF|Akamai|LiteSpeed|Malcare|Mission|ModSecurity|NAXSI|Nemesida|NetContinuum|NetScaler|NevisProxy|Newdefend|NexusGuard|NinjaFirewall|NSFocus|OnMessage|Open-Resty|Palo Alto|PerimeterX|pkSecurity|PowerCDN|Profense|AppWall|Reblaze|RSFirewall|Sabre|Safe3|Safedog|Safeline|SecuPress|Secure Entry|eEye SecureIIS|SecureSphere|SEngin|Shield Security|SiteGround|SiteGuard|Sitelock|SonicWall|UTM|Sophos|Squarespace|StackPath|Sucuri|Tencent|Teros|TransIP|URLMaster|URLScan|Varnish|VirusDie|Wallarm|WatchGuard|WebARX|WebKnight|WebSEAL|WebTotem|West263|Wordfence|WTS-WAF|360WangZhanBao|XLabs|Xuanwudun |Yundun|Yunsuo|Zenedge|ZScaler","ns1.bekchydns.com.",re.IGNORECASE)
#     print(test)
#     print("ok")


# for i in range(10):
#     for j in range(10):
#         print(i,j)
#         if i == 2:
#             break

# dic = None


# dic['test'] = 10

# print(dic)

# def login(session,headers):
#   response = session.get("http://testphp.vulnweb.com/login.php")
#   # soup = BeautifulSoup(response.content,features="html.parser")

#   # _token = soup.find("input",attrs={"name":"user_token"}).get("value")
#   # print(_token)
#   user = {
#       'uname':'test',
#       'pass':'test',
#       #'Login':'Login',
#   }
#   response = session.post("http://testphp.vulnweb.com/userinfo.php",data=user,headers=headers)
#   print(response.request.headers)


# import requests
# import re
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
# from urllib import parse

# user_agent = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 8.01"
# headers        = requests.utils.default_headers()
# headers['User-Agent'] = user_agent

# session = requests.session()
# login(session,headers)
# url = "http://testphp.vulnweb.com/userinfo.php"
# base_url ="http://testphp.vulnweb.com"
# for i in range(100):
#     response = session.get(url)
#     print(response.request.headers)



# print(session)
#soup.findAll('meta', name=re.compile("^description$", re.I))
# import requests

# response = requests.get("http://testphp.vulnweb.com")
# forms = soup.findAll("form",attrs={"method":re.compile("POST", re.IGNORECASE)})
# print(response)

# from urllib.parse import urlparse,parse_qs
# import re
# url = "http://can.com/test?hs=10&t=20"
# parsed = urlparse(url)
# print(parsed.path,parsed.query.split("="))

# a = "asdf=asdf=adsf=".split("=")
# print(a)
# # query = parsed.query
# test = parse_qs(query)
# for i in test.values():
#     print(i[0])

# a = []
# c = ('test','i')
# a.append(('test','i'))
# print(a)
# if c in a:
#     print("var")
# print(test)

# from test2 import Test

# a = Test()
# print(a.b)
# print(ABD)
# from core.crawler import Crawler

# crawler = Crawler()
# import requests

# resp = requests.request('GET','http://ahmetcankaraagacli.com')
# print(resp.status_code)

import socket 

connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

test = connection.connect(('176.53.35.152',21))
connection.send(("hello").encode("utf8"))
test = connection.recv(1024)
print(test)
# resp = connection.recv(1024)
# print(resp)






