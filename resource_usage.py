#!/usr/bin/env python
import psutil
# gives a single float value
print(psutil.cpu_percent())
# gives an object with many fields
print(psutil.virtual_memory())
# you can convert that object to a dictionary 
dic = dict(psutil.virtual_memory()._asdict())
for key in dic:
	print(key," : ",dic[key])