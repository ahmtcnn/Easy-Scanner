from scapy.all import *

# url = "instra.com"

# with open("data/subdomains.dat","r") as fp:
# 	for line in fp:
# 		line = line.rstrip("\n")
# 		test = line + "." + url
# 		result = sr1(IP(dst=test)/ICMP(),timeout=1)
# 		if result != None:
# 			print(test)
# 		else:
# 			print("no")


# import subprocess




# ip="002.instra.com"
# 	# if(s.run(["ping","-c", "1",ip])==0):
# 	#     print ("your IP is alive")
# 	# else:
# 	#     print ("Check ur IP")

# devnull = open(os.devnull, 'w')
# print(devnull)
# cevap = subprocess.run(["ping","-c", "1",ip],stdout=devnull, stderr=devnull)


# if cevap.returncode == 0:
# 	print("okey")
# else:
# 	print("no")
#!/usr/bin/env python
from socket import * 

if __name__ == '__main__':
	target = "ahmetcankaraagacli.com"
	targetIP = gethostbyname(target)

	#scan reserved ports
	for i in range(20, 1025):
		s = socket(AF_INET, SOCK_STREAM)

		result = s.connect_ex((targetIP, i))

		if(result == 0) :
			print ('Port %d:' % (i,))
		s.close()