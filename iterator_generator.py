#!/usr/bin/env python

# simple_generator.py

def gen():
	f = open("data","r")
	while True:
		line = f.readline()
		yield line
   

g = gen()
while True:
	try:
		print(next(g))
	except StopIteration:
   		print("Iteration finished")