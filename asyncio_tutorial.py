
# YOUTUBE TUTORIAL 1
# import asyncio


# async def find_divisibles(inrange, div_by):
#     print("finding nums in range {} divisible by {}".format(inrange, div_by))
#     located = []
#     for i in range(inrange):
#         if i % div_by == 0:
#             located.append(i)
#     print("Done w/ nums in range {} divisible by {}".format(inrange, div_by))
#     return located


# async def main():
#     divs1 = loop.create_task(find_divisibles(50800, 34113))
#     divs2 = loop.create_task(find_divisibles(100052, 3210))
#     divs3 = loop.create_task(find_divisibles(500, 3))
#     await asyncio.wait([divs1,divs2,divs3])

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()


#YOUTUBE TUTORIAL 2
# import asyncio
# import time


# async def myCoroutine():
# 	time.sleep(1)
# 	print("Simple Coroutine")

# # Another wat of define coroutine
# @asyncio.coroutine
# def myCoroutine2():
# 	print("Simple Coroutine2")


# def main():
# 	loop = asyncio.get_event_loop()
# 	loop.run_until_complete(myCoroutine())
# 	loop.close()


# main()


# import asyncio
# import random
# import socket

# async def myCoroutine(port):
# 	s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
# 	try:
# 		con = s.connect(("176.53.35.152", port))
# 		print(port,"open")
# 		s.close()
# 	except:
# 		s.close()
# 		print(port,"closed")

# async def main():
# 	tasks = []
# 	for i in range(100):
# 		tasks.append(asyncio.ensure_future(myCoroutine(i)))
		
# 	await asyncio.gather(*tasks)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

import time
import asyncio
import socket

def is_prime(x):
	return not any (x//i == x/i for i in range(x-1,1,-1))

async def port_scan(port):
	try:
		socket.setdefaulttimeout(0.25)
		#print("port scan %d" % port)
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect(("176.53.35.152", port))
		await asyncio.sleep(0.5)
		print(port,"open")
		s.close()
		return port
	except Exception as ex:
		#print("Error for port ",str(port),str(ex))
		s.close()
		


	

async def main():
	t1 = time.time()
	await asyncio.wait([port_scan(i) for i in range(100)])
	t2 = time.time()


	print("took %.2f seconds" % (t2-t1))

loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(main())
loop.close()




