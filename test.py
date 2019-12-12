# import aiohttp
# import asyncio


# async def get(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return response


# loop = asyncio.get_event_loop()

# coroutines = [get("http://ahmetcankaraagacli.com") for _ in range(8)]

# results = loop.run_until_complete(asyncio.gather(*coroutines))

# print("Results: %s" % results)

# for a in range(10):
# 	print(1)

#20 requests 20 second without session
#20 requests 9 second with session


#19 saniye 50 istek

#17 saniye 50 istel

#13 saniye furure ile

#8 saniye 10 thread ile

#6 saniye


# import requests
# from datetime import datetime

# session = requests.session()
# adapter = requests.adapters.HTTPAdapter(
#     pool_connections=50,
#     pool_maxsize=50)


# session.mount('http://', adapter)

# now = datetime.now()
# time1 = str(now.hour) + " : " + str(now.minute)  + " : " +str(now.second)
# print(time1)

# for i in range(50):
# 	response = session.get("https://ahmetcankaraagacli.com")
# 	print(response.status_code)

# now = datetime.now()
# time2 = str(now.hour) + " : " + str(now.minute)  + " : " +str(now.second)
# print(time2)
# session = requests.Session()
# adapter = requests.adapters.HTTPAdapter(
#     pool_connections=1,
#     pool_maxsize=1)
# session.mount('http://', adapter)
# response = session.get("http://example.org")
# print(response)

# from concurrent import futures

# import requests

# from datetime import datetime


# executor =  futures.ThreadPoolExecutor(max_workers=10)

# futures = [executor.submit(lambda: requests.get("https://ahmetcankaraagacli.com")) for _ in range(50)]

# results = [
#     f.result().status_code
#     for f in futures
# ]

# print("Results: %s" % results)

# now = datetime.now()
# time2 = str(now.hour) + " : " + str(now.minute)  + " : " +str(now.second)
# print(time2)


# from requests_futures import sessions
# from datetime import datetime

# now = datetime.now()
# time1 = str(now.hour) + " : " + str(now.minute)  + " : " +str(now.second)
# print(time1)
# session = sessions.FuturesSession(executor=ThreadPoolExecutor(max_workers=10))

# futures = [
#     session.get("https://ahmetcankaraagacli.com")
#     for _ in range(50)
# ]

# results = [
#     f.result().status_code
#     for f in futures
# ]

# print("Results: %s" % results)

# now = datetime.now()
# time2 = str(now.hour) + " : " + str(now.minute)  + " : " +str(now.second)
# print(time2)

#3


# import aiohttp
# import asyncio
# from datetime import datetime


# async def get(url):
#     async with aiohttp.ClientSession() as session:
# 	    async with session.get(url) as response:
# 	        return response.status


# now = datetime.now()
# time1 = str(now.hour) + " : " + str(now.minute)  + " : " +str(now.second)
# print(time1)


# loop = asyncio.get_event_loop()


# coroutines = [get("https://ahmetcankaraagacli.com") for _ in range(50)]

# results = loop.run_until_complete(asyncio.gather(*coroutines))

# print("Results: %s" % results)

# now = datetime.now()
# time2 = str(now.hour) + " : " + str(now.minute)  + " : " +str(now.second)
# print(time2)




# from aiohttp import ClientSession
# import asyncio

# async def fetch(url):
#     async with ClientSession() as s, s.get(url) as res:
#         ret = await res.read()
#         print(ret)
#         return ret

# asyncio.run(fetch("http://example.com") for _ in range(5))


# import asyncio
# import time
# import aiohttp


# async def download_site(session, url):
#     async with session.get(url) as response:
#         if response.status == 200: print("URL: {0}\t\t\t Status {1}".format(url, response.status))


# async def download_all_sites(sites):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for url in list(sites):
#         	urli = url[0]
#         	#	print(urli)
#         	task = asyncio.ensure_future(download_site(session, urli))
#         	#print(str(next(sites)))
#         	tasks.append(task)
#         await asyncio.gather(*tasks, return_exceptions=True)


# if __name__ == "__main__":
# 	url = "http://ahmetcankaraagacli.com/"
# 	sites =   ([url+line.rstrip("\n")] for line in open("data/directories.dat"))
# 	start_time = time.time()

# 	loop = asyncio.get_event_loop()
# 	loop.run_until_complete(download_all_sites(sites))
# 	duration = time.time() - start_time
# 	leng = len(list(sites))
# 	print(f"Tested dirs in {duration} seconds")


# from urllib.parse import urlparse,urljoin

# sub = "subdomain"
# url = "ahmetcankaraagacli.com"
# full_url = urljoin(url,sub)
# print(full_url)

dic = {'test':('test2','test3'),
		'ahmet':('vasdf','fdasf')}

print(dic.values())

for i in dic.values():
	for j in i:
		print(j)