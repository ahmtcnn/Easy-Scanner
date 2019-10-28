import socket
import threading
import time
from queue import Queue
import socket

from progress.bar import Bar
from tqdm import tqdm



"""By setting them as daemon threads, we can let them run and forget about them, and when our program quits, any daemon threads are killed automatically."""
class PortScanner():
	def __init__(self):
		socket.setdefaulttimeout(0.25)
		self.print_lock = threading.Lock()
		self.target = '176.53.35.152'
		self.progress = tqdm(total=65536)
		self.q = Queue()
		self.startTime = time.time()
		self.start_threads()
		self.queue_ports()
		self.q.join()
		print('Time taken:', time.time() - self.startTime)
	
	def start_threads(self):
		for _ in range(150):
			t = threading.Thread(target = self.threader)
			t.daemon = True
			t.start()
	
	def queue_ports(self):
		print("PORT\tSERVICE\tSTATE")	
		for port in range(0, 65536):
			self.q.put(port)
	
	def threader(self):
		while True:
			port  = self.q.get()
			self.portscan(port)
			self.q.task_done() # bu q.join i tetiklemek için.


	def portscan(self,port):
		s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
		try:
			con = s.connect((self.target, port))
			with self.print_lock:
				try:
					service = socket.getservbyport(port)
				except:
					service = "unknown"
				self.progress.write(f'{port}')
				con.close()
				self.progress.update(1)
		except:
			self.progress.update(1)


scanner = PortScanner()
