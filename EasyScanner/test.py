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

from aio_ping import ping

from aio_ping import Ping,VerbosePing


async def ping(hostname, verbose=True, handle_signals=False, **kw):
    """
    Send @count ping to @hostname with the given @timeout
    """
    ping = (VerbosePing if verbose else Ping)(verbose=verbose, **kw)
    if handle_signals: ping.add_signal_handler()
    await ping.init(hostname)
    res = await ping.looped()
    if verbose:
        ping.print_stats()
    ping.close()
    return res


