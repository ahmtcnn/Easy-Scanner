# from builtwith import *

# import requests

# #response = requests.get("http://ktu.edu.tr")
# #print(response)
# info = builtwith("http://www.ktu.edu.tr")

# import requests_html

# s = requests_html.HTMLSession()
# r = s.get('http://ktu.edu.tr')
# print(r.html.encoding)
# #print(info)

# import chardet
# rawData=open('encoding.txt',"r").read()
# rawDataBytes = bytes(rawData, 'utf-8')
# print(chardet.detect(rawDataBytes)['encoding'])

# import socket
# from ip2geotools.databases.noncommercial import DbIpCity

# response = DbIpCity.get("95.216.180.154", api_key='free')
# print(response)

# print(dir(response))
# print(response.city +" / "+ response._region + " / " + response.country)
# print("https://maps.google.com/?q="+str(response.latitude)+","+str(response.longitude))

# # ip = socket.gethostbyname("bekchy.com")
# # liste = ip.split("\n")
# # print(liste)


# import psutil
# import time
# print(psutil.cpu_times())
# for x in range(3):
# 	print(psutil.cpu_percent(interval=3))


# def test(process):
#     while True:

#         print("status: "+str(process.status()))
#         print("cpu percent: "+str(process.cpu_percent(interval=2.0)))
#         print(process.cpu_num())
#         print("threads: " +str(process.num_threads()))
#         #time.sleep(2)

# def get_pid():
#     for i in psutil.pids():
#         if "test4.py" in psutil.Process(i).cmdline():
#             return psutil.Process(i).pid


# pid  = get_pid()
# process = psutil.Process(pid)
# test(process)

# import asyncio
# import time

# a = 0

# async def checkProxy(site):
#     try:
#         check = await asyncio.create_subprocess_exec(
#             'ping', '-c', '1', '-W', '2', site, stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.DEVNULL)
#         out, error = await check.communicate()

#         if out != b'':
#             print(site)
#         else:
#             pass

        	
#     except Exception as exp:
#         pass
#         #print(exp,"test61")

# async def run(sem,site):
#     async with sem:
#         return await checkProxy(site)

# def checkProxies(sites):
# 	sem = asyncio.Semaphore(200) #Change this value for concurrency limitation
# 	loop = asyncio.get_event_loop()
# 	tasks = [run_with_sem(sem,site) for site in sites]
# 	loop.run_until_complete(asyncio.gather(*tasks))
# 	loop.close()

# site = ".instra.com"
# sites =   [str(line.rstrip("\n"))+str(site) for line in open("data/subdomainstest.dat")]

# checkProxies(sites)
# # for site in sites:
# # 	print(site)
# # 	print("\n")
# # 	time.sleep(1)


import asyncio

from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import time

async def check_sub(target,signals):
    conn = asyncio.open_connection(target, '80')
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=3)
        print(target)
        signals.result_list.emit(str(target))
    except:
        pass
    finally:
        if 'writer' in locals():
            writer.close()


    # except Exception as exp:
    #     pass
    #     #print(exp,"test61")


async def check_sub_with_sem(site,signals):
    sem = asyncio.Semaphore(10)
    async with sem:
        await check_sub(site,signals)


async def run(sites,signals):
    
    tasks = []
    for site in sites:

        task = asyncio.ensure_future(check_sub_with_sem(site,signals))
        tasks.append(task)
    responses = await asyncio.gather(*tasks)
    return responses


class WorkerSignals(QObject):
    
    result_list     = pyqtSignal(str)
    info_box        = pyqtSignal(str)
    finish_control  = pyqtSignal()


class SubdomainScanner(QRunnable):
    def __init__(self,target):
        super(SubdomainScanner,self).__init__()
        self.target = "."+target
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        start_time = time.time()
        sites =   [str(line.rstrip("\n"))+str(self.target) for line in open("data/subdomains.dat")]
        loop = asyncio.new_event_loop()
        self.result = loop.run_until_complete(run(sites,self.signals))
        self.signals.finish_control.emit()
        finish_time = time.time()
        difference = finish_time - start_time
        self.signals.info_box.emit('[✔] Subdomain Scan finished!')
        self.signals.info_box.emit('Time Taken: '+ str(difference))
        self.signals.finish_control.emit()



